import datetime
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


