from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# TODO change this to read/write once I'm actually testing sending
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

# TODO make it possible to pass this in via CLI
CLIENT_SECRET_FILE = 'batch_send_secret.json'
APPLICATION_NAME = 'batch_send'

# NOTE this code was adapted from https://developers.google.com/gmail/api/quickstart/python
def get_credentials():
    """Gets valid user credentials from local storage if it exists. Otherwise, runs the OAuth2 flow to store
    credentials.

    Credentials are stored in the current working directory under the .credentials subdirectory.
    """
    current_dir = os.getcwd()
    credential_dir = os.path.join(current_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir, 'batch_send.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])


if __name__ == '__main__':
    main()
