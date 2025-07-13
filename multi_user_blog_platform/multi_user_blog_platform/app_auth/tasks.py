from celery import shared_task
import base64
from google.oauth2.credentials import Credentials
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from django.urls import reverse_lazy


@shared_task
def send_confirmation_email(uid, token, user_email, from_email='svetoslavbaykov55@gmail.com'):
    try:
        creds = Credentials.from_authorized_user_file(filename='token.json')

        activation_link = f'{settings.SITE_URL}{reverse_lazy('activate_account', kwargs={'uidb64': uid, 'token': token})}'

        subject = 'Activate account'

        message = EmailMessage()

        message.set_content(f'Please click the following link to activate your account: {activation_link}')
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = user_email

        encrypted_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {'raw': encrypted_message}

        service = build(serviceName='gmail', version='v1', credentials=creds)

        send_message = service.users().messages().send(userId='me', body=create_message)
    
    except HttpError as e:
        print(f'An errpr occured: {e}')
        send_message = None
    
    return send_message