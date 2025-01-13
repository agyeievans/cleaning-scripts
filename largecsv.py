import lxml.etree as ET
import pandas as pd
import os

def process_tmx_to_csv(file_path, batch_size=1000000, output_dir='/ar-fr NLLB', base_filename='ar-fr NLLB'):
    # Use iterparse to process the file element by element
    context = ET.iterparse(file_path, events=('end',), tag='tu')

    fr_texts = []
    ar_texts = []
    batch_counter = 0
    row_counter = 0  # Track the current row within the file

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process translation units in the TMX file
    for event, elem in context:
        fr_text = None
        ar_text = None

        # Iterate over the translation units within each 'tu'
        for tuv in elem.findall('.//tuv'):
            lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            seg = tuv.find('.//seg')

            if seg is not None:  # Check if the 'seg' element exists
                if lang == 'fr':
                    fr_text = seg.text
                elif lang == 'ar':
                    ar_text = seg.text

        # Only add pairs where both translations are available
        if fr_text and ar_text:
            fr_texts.append(fr_text)
            ar_texts.append(ar_text)
            row_counter += 1  # Increment row counter for each pair added

        # Write to CSV in batches or when the file is full
        if len(fr_texts) >= batch_size or row_counter >= 1048576:  # Check for batch size or file limit
            batch_df = pd.DataFrame({'French': fr_texts, 'Arabic': ar_texts})

            # Determine the output file name
            output_file = os.path.join(output_dir, f'{base_filename}_batch_{batch_counter}.csv')

            # Write the batch to the CSV file with the correct encoding for Arabic characters
            batch_df.to_csv(output_file, index=False, header=True, mode='w', encoding='utf-8-sig')

            # Clear lists and reset counters
            fr_texts.clear()
            ar_texts.clear()
            batch_counter += 1
            row_counter = 0  # Reset row counter for the new file

        # Clear the processed element to free memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    # Process any remaining data after the loop
    if fr_texts and ar_texts:
        batch_df = pd.DataFrame({'French': fr_texts, 'Arabic': ar_texts})
        output_file = os.path.join(output_dir, f'{base_filename}_batch_{batch_counter}.csv')
        batch_df.to_csv(output_file, index=False, header=True, mode='w', encoding='utf-8-sig')

    # Print the output directory where the CSV files are saved
    absolute_path = os.path.abspath(output_dir)
    print(f"Processing completed and files saved to '{absolute_path}'.")


# Specify the file path and start processing
file_path = 'ar-fr NLLB.tmx'  # File path on Google Colab
output_dir = '/ar-fr NLLB'  # Output directory for the CSV files

process_tmx_to_csv(file_path, output_dir=output_dir)