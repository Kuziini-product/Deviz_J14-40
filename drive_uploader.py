
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def init_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def upload_to_drive(drive, file_path, folder_name):
    file_name = file_path.split("/")[-1]
    gfile = drive.CreateFile({'title': file_name})
    gfile.SetContentFile(file_path)
    gfile.Upload()
