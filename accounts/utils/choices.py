from django.db import models

PROVINCES = [
    ("kzn", "KwaZulu-Natal"),
    ("mp", "Mpumalanga"),
    ("nw", "North-West"),
    ("fs", "Free-State"),
    ("wc", "Western Cape"),
    ("lp", "Limpopo"),
    ("gp", "Gauteng"),
    ("ec", "Eastern Cape"),
    ("nc", "Northern Cape"),
]

TITLE_CHOICES = (
    ("Mr", "Mr"),
    ("Mrs", "Mrs"),
    ("Ms", "Ms"),
    ("Dr", "Dr"),
    ("Prof", "Prof.")
)

class StatusChoices(models.TextChoices):
    NOT_ACCEPTED = ("NOT ACCEPTED", "Not accepted")
    PENDING = ("PENDING", "Pending")
    ACCEPTED = ("ACCEPTED", "Accepted")
    HOLD = ("HOLD", "On Hold")
    BLOCKED = ("Blocked", "Blocked")

class Gender(models.TextChoices):
    MALE = ("MALE", "Male")
    FEMALE = ("FEMALE", "Female")
    OTHER = ("OTHER", "Other")


class HomeLanguage(models.TextChoices):
    AFRIKAANS = 'AF', 'Afrikaans'
    ENGLISH = 'EN', 'English'
    ISINDEBELE = 'ND', 'isiNdebele'
    ISIXHOSA = 'XH', 'isiXhosa'
    ISIZULU = 'ZU', 'isiZulu'
    SEPEDI = 'NS', 'Sepedi'
    SESOTHO = 'ST', 'Sesotho'
    SETSWANA = 'TN', 'Setswana'
    SISWATI = 'SS', 'siSwati'
    TSHIVENDA = 'VE', 'Tshivenda'
    XITSONGA = 'TS', 'Xitsonga'
    SASL = 'SL', 'South African Sign Language'


class RelationShip(models.TextChoices):
    OTHER = ("OTHER", "Other")
    WIFE = ("WIFE", "Wife")
    HUSBAND = ("HUSBAND", "Husband")
    DAUGHTER = ("DAUGHTER", "Daughter")
    SON = ("SON", "Son")
    MOTHER = ("MOTHER", "Mother")
    FATHER = ("FATHER", "Father")
    STEPMOTHER = ("STEPMOTHER", "Step-mother")
    STEPFATHER = ("STEPFATHER", "Step-father")
    STEPBROTHER = ("STEPBROTHER", "Step-Brother")
    STEPSISTER = ("STEPSISTER", "Step-Sister")
    GRANDMOTHER = ("GRANDMOTHER", "Grandmother")
    GRANDFATHER = ("GRANDFATHER", "Grandfather")
    GREATGRANDMOTHER = ("GREATGRANDMOTHER", "Great Grandmother")
    GREATGRANDFATHER = ("GREATGRANDFATHER", "Great Grandfather")
    GREATGREATGRANDMOTHER = ("GREATGREATGRANDMOTHER", "Great Great Grandmother")
    GREATGREATGRANDFATHER = ("GREATGREATGRANDFATHER", "Great Great Grandfather")
    BROTHER = ("BROTHER", "Brother")
    SISTER = ("SISTER", "Sister")
    COUSIN = ("COUSIN", "Cousin")
    AUNT = ("AUNT", "Aunt")
    UNCLE = ("UNCLE", "Uncle")
    NEPHEW = ("NEPHEW", "Nephew")
    NIECE = ("NIECE", "Niece")

class EmployementStatus(models.TextChoices):
    EMPLOYEED = ("EMPLOYEED", "Employeed")
    UNEMPLOYEED = ("UNEMPLOYEED", "Unemployeed")
    SELF_EMPLOYEED = ("SELF_EMPLOYEED", "Self-employeed")
    OTHER = ("OTHER", "Other")