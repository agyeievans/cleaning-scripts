import os
import zipfile
import rarfile
import gzip
import tarfile
import shutil
import lzma

def extract_file(file_path, output_dir):
    try:
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
                print(f"Extracted: {file_path} -> {output_dir}")

        elif file_path.endswith(".rar"):
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(output_dir)
                print(f"Extracted: {file_path} -> {output_dir}")

        elif file_path.endswith(".gz"):
            output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".gz", ""))
            with gzip.open(file_path, 'rb') as gz_ref, open(output_file, 'wb') as out_f:
                shutil.copyfileobj(gz_ref, out_f)
                print(f"Extracted: {file_path} -> {output_file}")

        elif file_path.endswith(".xz"):
            output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".xz", ""))
            with open(output_file, 'wb') as out_f:
                shutil.copyfileobj(lzma.open(file_path, 'rb'), out_f)
                print(f"Extracted: {file_path} -> {output_file}")

        elif file_path.endswith(".tgz") or file_path.endswith(".tar.gz"):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(output_dir)
                print(f"Extracted: {file_path} -> {output_dir}")

        else:
            print(f"Unsupported file format: {file_path}")
    
    except (zipfile.BadZipFile, rarfile.BadRarFile, gzip.BadGzipFile, tarfile.TarError, FileNotFoundError, OSError) as e:
        print(f"Error extracting {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    test_files = ["articles-sports.zip"]
    output_directory = "articles-sports"
    os.makedirs(output_directory, exist_ok=True)
    
    for file in test_files:
        extract_file(file, output_directory)



# test_files = ["example.zip", "example.rar", "example.gz", "example.xz", "example.tgz"]