from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def init_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def upload_to_drive(drive, file_path, folder_name="Kuziini_Devize"):
    file = drive.CreateFile({'title': file_path.split("/")[-1]})
    file.SetContentFile(file_path)
    file.Upload()