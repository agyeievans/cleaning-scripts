from google.oauth2 import service_account
from googleapiclient.discovery import build
import concurrent.futures

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_service():
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

def get_folder_size(service, folder_id, indent=""):
    total_size = 0
    page_token = None
    
    while True:
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            files = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, size, mimeType)',
                pageToken=page_token
            ).execute()
            
            for file in files.get('files', []):
                if file.get('mimeType') == 'application/vnd.google-apps.folder':
                    size = get_folder_size(service, file['id'], indent + "  ")
                    print(f"{indent}Folder: {file['name']} - {format_size(size)}")
                    total_size += size
                else:
                    size = int(file.get('size', 0))
                    total_size += size
                    print(f"{indent}File: {file['name']} - {format_size(size)}")
            
            page_token = files.get('nextPageToken')
            if not page_token:
                break
                
        except Exception as e:
            print(f'Error processing folder: {str(e)}')
            return 0
            
    return total_size

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

if __name__ == '__main__':
    try:
        folder_id = input("Enter the Google Drive folder ID: ")
        service = get_service()
        total_size = get_folder_size(service, folder_id)
        print(f"\nTotal folder size: {format_size(total_size)}")
    except Exception as e:
        print(f"Error: {str(e)}")