import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(filename='token.json', scopes=SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file='credentials.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0, redirect_uri_trailing_slash=False)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())


if __name__ == '__main__':
    main()