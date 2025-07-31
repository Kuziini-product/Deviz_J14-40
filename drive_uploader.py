
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'client_secrets.json'

def init_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(service, file_path, client_name):
    file_name = os.path.basename(file_path)
    folder_id = get_or_create_folder(service, client_name)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def get_or_create_folder(service, folder_name, parent_name='2025'):
    parent_id = get_or_create_year_folder(service, parent_name)
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

def get_or_create_year_folder(service, year_folder):
    query = f"name='{year_folder}' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']
    else:
        metadata = {
            'name': year_folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [get_or_create_root_folder(service)]
        }
        folder = service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')

def get_or_create_root_folder(service):
    query = "name='Kuziini_Devize' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']
    else:
        metadata = {
            'name': 'Kuziini_Devize',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')
