import lxml.etree as ET
import pandas as pd
import os

def process_tmx_to_excel(file_path, batch_size=1000000, output_path='ar-en LinguaTools-WikiTitles.xlsx'):
    # Use iterparse to process the file element by element
    context = ET.iterparse(file_path, events=('end',), tag='tu')

    en_texts = []
    ar_texts = []
    batch_counter = 0
    row_counter = 0  # Track the current row within the sheet

    # Use Pandas ExcelWriter to write in batches to XLSX
    with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
        for event, elem in context:
            en_text = None
            ar_text = None

            # Iterate over the translation units within each 'tu'
            for tuv in elem.findall('.//tuv'):
                lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                seg = tuv.find('.//seg')

                if seg is not None:  # Check if the 'seg' element exists
                    if lang == 'en':
                        en_text = seg.text
                    elif lang == 'ar':
                        ar_text = seg.text

            # Only add pairs where both translations are available
            if en_text and ar_text:
                en_texts.append(en_text)
                ar_texts.append(ar_text)
                row_counter += 1  # Increment row counter for each pair added

            # Write to Excel in batches or when the sheet is full
            if len(en_texts) >= batch_size or row_counter >= 1048576:  # Check for batch size or sheet limit
                batch_df = pd.DataFrame({'English': en_texts, 'Arabic': ar_texts})

                # Determine the sheet name
                sheet_name = f'Translations_{batch_counter}'

                # Write the batch to the Excel file in a new sheet
                batch_df.to_excel(writer, index=False, sheet_name=sheet_name, header=True)

                # Clear lists and reset counters
                en_texts.clear()
                ar_texts.clear()
                batch_counter += 1
                row_counter = 0  # Reset row counter for the new sheet

            # Clear the processed element to free memory
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        # Process any remaining data after the loop
        if en_texts and ar_texts:
            batch_df = pd.DataFrame({'English': en_texts, 'Arabic': ar_texts})
            sheet_name = f'Translations_{batch_counter}'
            batch_df.to_excel(writer, index=False, sheet_name=sheet_name, header=True)

    # Print the absolute path of the saved file
    absolute_path = os.path.abspath(output_path)
    print(f"Processing completed and saved to '{absolute_path}'.")


# Specify the file path and start processing
file_path = 'ar-en LinguaTools-WikiTitles.tmx'  # File path on Google Colab
output_path = 'ar-en LinguaTools-WikiTitles.xlsx'  # Output Excel file path

process_tmx_to_excel(file_path, output_path=output_path)