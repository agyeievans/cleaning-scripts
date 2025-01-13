import requests
import os

# GitHub repo details
owner = "Nandutu"
repo = "luganda_dataset"
path = "text"  # Path to the directory within the repo

# Base URL for the API
base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

# Folder to save the .txt files
save_folder = "downloaded_txt_files"
os.makedirs(save_folder, exist_ok=True)

# Function to download .txt files
def download_txt_files(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        files = response.json()
        
        for file in files:
            if file['type'] == 'file' and file['name'].endswith('.txt'):
                file_url = file['download_url']
                download_file(file_url, file['name'])
    else:
        print(f"Failed to retrieve contents from {url}")

def download_file(file_url, file_name):
    response = requests.get(file_url)
    if response.status_code == 200:
        file_path = os.path.join(save_folder, file_name)
        # Use 'utf-8' encoding to avoid UnicodeEncodeError
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name} from {file_url}")

# Start downloading .txt files
download_txt_files(base_url)
