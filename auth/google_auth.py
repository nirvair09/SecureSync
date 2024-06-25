import os
import json
import webbrowser
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

class GoogleAuth:
    def __init__(self,credentials_file,token_file):
        self.credentials_file=credentials_file
        self.token_files=token_file
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.creds = None


    def login(self):
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())
        return self.creds

    def logout(self):
        if os.path.exists(self.token_files):
            os.remove(self.token_files)
            self.creds=None