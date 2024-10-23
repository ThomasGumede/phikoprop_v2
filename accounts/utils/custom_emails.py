import logging, base64
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from accounts.utils.tokens import account_activation_token, generate_activation_token
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings
logger = logging.getLogger("emails")

def send_html_email(subject, to_email, template_name, context):
    try:
        
        html_content = render_to_string(template_name, context)

        # Create the email message
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.content_subtype = 'html' 

        # Send the email
        email.send()
        logger.info(f"Email sent to {to_email} without attachment.")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {e}")  

# def send_html_email_with_attachments(to_email:str, subject: str, html_content, from_email:str, pdf_attachments:list):

#     message = Mail(
#         from_email=from_email,
#         to_emails=to_email,
#         subject=subject,
#         html_content=html_content,
#     )


#     for pdf_attachment in pdf_attachments:
        

#         attachment = Attachment(
#             FileContent(pdf_attachment["file_content"]),
#             FileName(pdf_attachment['name']),
#             FileType('application/pdf'),
#             Disposition('attachment')
#         )

#         message.add_attachment(attachment)

#     try:
#         sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
#         response = sg.send(message)
#         return True
    
#     except Exception as e:
#         return False

def send_email_confirmation_email(user, new_email, request):
    try:
        mail_subject = "BBGI | New Email Confirmation"
        message = render_to_string("emails/account/email_activation.html",
                {
                    "user": user.get_full_name(),
                    "email": new_email,
                    "uid": generate_activation_token(user),
                    "token": account_activation_token.make_token(user),
                }, request
            )
        # sent = custom_send_email(new_email, mail_subject, message)

        # if not sent:
        #     logger.error("User did not receive email")
        #     return False
        # return True

        email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
        email.content_subtype = 'html' 

            # Send the email
        email.send()
        logger.info(f"Email sent to {user.email} without attachment.")
            
        return True
    except Exception as err:
        logger.error(f"Failed to send send_email_confirmation_email to {user.email}. Error: {err}")
        return False
    
def send_verification_email(user, request):
        
        try:
            mail_subject = "BBGI | Activate Account"
            message = render_to_string("emails/account/account_activate_email.html",
                {
                    "user": user.get_full_name(),
                    "uid": generate_activation_token(user),
                    "token": account_activation_token.make_token(user),
                }, request
            )
            
            # sent = custom_send_email(user.email, mail_subject, message)

            # if not sent:
            #     logger.error("User did not receive email")
            #     return False

            email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = 'html' 

            # Send the email
            email.send()
            logger.info(f"Email sent to {user.email} without attachment.")
            
            return True
        except Exception as err:
             logger.error(f"Failed to send send_verification_email to {user.email}. Error: {err}")
             return False

def send_password_reset_email(user, request):
    try:
        mail_subject = "BBGI | Password Reset request"
        message = render_to_string("emails/password/reset_password_email.html", {
            'user': user.get_full_name(),     
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }, request)
            
            
        # sent = custom_send_email(user.email, subject, message)
        # if not sent:
        #     return False
           
        email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
        email.content_subtype = 'html' 

            # Send the email
        email.send()
        logger.info(f"Email sent to {user.email} without attachment.")
            
        return True
    except Exception as err:
        logger.error(f"Failed to send send_password_reset_email to {user.email}. Error: {err}")
        return False

def send_html_email_with_attachments(to_email: str, subject: str, html_content: str, from_email: str, attachments: list = None) -> bool:
    """
    Sends an HTML email with optional attachments.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The email subject.
        html_content (str): The HTML content of the email.
        from_email (str): The sender's email address.
        attachments (list): A list of attachments where each is a dictionary with 'file_content' and 'filename'.

    Returns:
        bool: True if the email is sent successfully, False otherwise.
    """
    try:
        email = EmailMessage(subject=subject, body=html_content, from_email=from_email, to=[to_email])
        email.content_subtype = 'html'

        # Attach files if provided
        if attachments:
            for attachment in attachments:
                email.attach(attachment['filename'], base64.b64decode(attachment['file_content']), 'application/pdf')

        email.send()
        logger.info(f"Email sent to {to_email} with attachments.")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {e}")
        return False

 

