import uuid
import sys

from django.shortcuts import render
from django.core.mail import send_mail

from accounts.models import Token


def send_login_mail(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for superlistss',
        f'Use this link to login:\n\n{url}',
        'noreply@superlists',
        [email])
    return render(request, 'login_email_sent.html')


