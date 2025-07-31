from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def init_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def upload_to_drive(drive, filepath, folder_name):
    f = drive.CreateFile({'title': filepath.split("/")[-1]})
    f.SetContentFile(filepath)
    f.Upload()
