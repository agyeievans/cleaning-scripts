import csv

def clean_text(text):
    # Remove extra quotes and clean the text
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text

# Read the input file with UTF-8 encoding
with open('WordProject_ Luganda_English_Corpus - verses.txt', 'r', encoding='utf-8') as file:
    # Skip header line
    next(file)  
    next(file)

    # Process and write to new CSV file with UTF-8-SIG encoding
    with open('WordProject_ Luganda_English_Corpus - verses.csv', 'w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['id', 'english', 'luganda'])

        for line in file:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            # Split by first comma to get ID
            parts = line.split(',', 1)
            if len(parts) != 2:
                continue

            id_part, rest = parts

            # Find the English part (between first and second set of quotes)
            start = rest.find('"') + 1
            if start > 0:
                end = rest.find('"', start)
                if end > 0:
                    english = rest[start:end]
                    # Everything after the english part (after the quotes and comma) is Luganda
                    luganda = rest[end+2:].strip()
                    if luganda.startswith('"'):
                        luganda = luganda[1:]
                    if luganda.endswith('"'):
                        luganda = luganda[:-1]
                    
                    writer.writerow([id_part, english, luganda])