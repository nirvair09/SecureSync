from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import os

class GoogleDrive:
    def __init__(self, creds):
        self.service = build('drive', 'v3', credentials=creds)

    def upload_file(self, file_path, mime_type='application/zip'):
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')

    def download_file(self, file_id, dest_path):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(dest_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.close()
        return dest_path

    def list_files(self):
        results = self.service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items

    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    def get_storage_info(self):
        about = self.service.about().get(fields="storageQuota").execute()
        used = int(about['storageQuota']['usage']) / (1024 * 1024 * 1024)
        total = int(about['storageQuota']['limit']) / (1024 * 1024 * 1024)
        return used, total
