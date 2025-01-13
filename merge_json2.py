import json
import csv
import codecs

def extract_translations(input_file, output_file):
   try:
       with codecs.open(input_file, 'r', encoding='utf-8') as json_file, \
            codecs.open(output_file, 'w', encoding='utf-8-sig') as csv_file:
           
           csv_writer = csv.writer(csv_file)
           csv_writer.writerow(['French', 'Mossi'])
           
           for line in json_file:
               try:
                   data = json.loads(line)
                   french = data['translation'].get('fr', '')
                   mossi = data['translation'].get('mos', '')
                   csv_writer.writerow([french, mossi])
               except json.JSONDecodeError:
                   print(f"Skipping invalid JSON line: {line.strip()}")
       
       print(f"CSV file '{output_file}' created successfully with UTF-8-SIG encoding.")
   
   except FileNotFoundError:
       print(f"Error: File {input_file} not found")

# Example usage
input_file = 'dev.json'
output_file = 'dev.csv'

extract_translations(input_file, output_file)