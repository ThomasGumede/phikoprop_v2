from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.conf import settings
from accounts.forms import RegistrationForm, UserLoginForm, UserForm
from accounts.utils.custom_emails import send_email_confirmation_email, send_verification_email
from accounts.utils.decorators import user_not_authenticated
from accounts.utils.tokens import account_activation_token
import logging, jwt

logger = logging.getLogger("accounts")
User = get_user_model()

@login_required
def get_account(request, username):
    user = get_object_or_404(User, id=request.user.id, username=username)
    return render(request, "accounts/account.html", {"user": user})

@login_required
def user_applications(request, username):
    user = get_object_or_404(User, id=request.user.id, username=username)
    return render(request, "accounts/manage/user-applications.html", {"user": user})

@login_required
def update_profile(request, username):
    user = get_object_or_404(User, id=request.user.id, username=username)
    form = UserForm(instance=user)
    if request.method == "POST":
        
        form = UserForm(instance=user, data=request.POST, files=request.FILES)
        
        if form.is_valid() and form.is_multipart():
            user_updated = form.save(commit=False)
            user_updated.save()
            messages.success(request, "Details Updated")
        else:
            messages.error(request, "Something is missing, fix error below")
    return render(request, "accounts/manage/update-profile.html", {"user": user, "form": form})

@user_not_authenticated
def custom_login(request):
    next_page = request.GET.get("next", None)
    template_name = "accounts/login.html"
    success_url = "npi_home:npi-home"
    if next_page:
        success_url = next_page

    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None and user.is_active:
                login(request, user)
                messages.success(
                    request, f"Hello <b>{user.username}</b>! You have been logged in"
                )
                return redirect(success_url)
        else:
            account = User.objects.filter(username=form.cleaned_data["username"]).first()
            if account != None and not account.is_active:
                messages.error(request, f"Sorry your account is not active. We have sent account activation email to your email {account.email}")
                sent = send_verification_email(account, request)
                if not sent:
                    pass
                return redirect("accounts:login")
            
            return render(
                request=request, template_name=template_name, context={"form": form}
            )

    form = UserLoginForm()
    return render(request=request, template_name=template_name, context={"form": form})

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("npi_home:npi-home")

@user_not_authenticated
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        payload = jwt.decode(uidb64, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(pk=payload["user_id"], username=payload["username"])
    except User.DoesNotExist:
        user = None
    
    if user and account_activation_token.check_token(user, token):
        if user.is_active == True:
            messages.success(
                request,
                "Thank you for your email confirmation. Now you can login your account.",
            )
            return redirect("accounts:login")
        
        user.is_active = True
        user.is_email_activated = True
        user.save(update_fields=["is_active", "is_email_activated"])

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("accounts:login")
    else:
        messages.error(request, f"Activation link is expired! New activation link was sent to {user.email}")
        sent = send_verification_email(user, request)
        if not sent:
            logger.error(f"Something went wrong trying to send email to {user.username}")

    return redirect("home:home")

def confirm_email(request, uidb64, token):
    logout(request)
    User = get_user_model()
    try:
        payload = jwt.decode(uidb64, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(pk=payload["user_id"], username=payload["username"])
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_activated = True
        user.save(update_fields=["is_active", "is_email_activated"])

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login to your account with your new email.",
        )

        return redirect("accounts:login")
    
    else:
        messages.error(request, f"Email confirmation link is expired! New email confirmation link was sent to {user.email}")
        sent = send_email_confirmation_email(user, user.email, request)

        if not sent:
            logger.error(f"Something went wrong trying to send email to {user.username}")

    return redirect("home:home")

@user_not_authenticated
def register(request):
    template_name = "accounts/register.html"
    success_url = "accounts:login"
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # send_verification_email(user, request)
            messages.success(
                request,
                f"You have successfully registered, please login",
            )
            return redirect(success_url)
        else:
            messages.error(request, "Something went wrong while signing up")
            return render(
                request=request, template_name=template_name, context={"form": form}
            )
    
    form = RegistrationForm()
    return render(request=request, template_name=template_name, context={"form": form})

@user_not_authenticated
def activation_sent(request):
    return render(request, "accounts/activation_sent.html")
