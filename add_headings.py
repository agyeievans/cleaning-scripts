# import csv

# def add_headings_to_existing_csv(file_name):
#     # Define the column headings
#     headings = ["English", "Arabic"]

#     try:
#         # Read the existing data from the CSV file
#         with open(file_name, mode='r', newline='', encoding='utf-8') as csv_file:
#             existing_data = list(csv.reader(csv_file))

#         # Insert the headings as the first row
#         existing_data.insert(0, headings)

#         # Write the updated data back to the CSV file
#         with open(file_name, mode='w', newline='', encoding='utf-8-sig') as csv_file:
#             writer = csv.writer(csv_file)
#             writer.writerows(existing_data)

#         print(f"Headings added successfully to '{file_name}' without removing existing data.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Specify the CSV file name
# csv_file_name = "flores dev Egyptian Arabic.csv"

# # Call the function to add headings
# add_headings_to_existing_csv(csv_file_name)

import csv

def delete_first_row(file_name):
    try:
        # Read the existing data from the CSV file
        with open(file_name, mode='r', newline='', encoding='utf-8') as csv_file:
            data = list(csv.reader(csv_file))

        # Remove the first row
        if data:
            data = data[1:]

        # Write the updated data back to the CSV file
        with open(file_name, mode='w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

        print(f"The first row has been successfully deleted from '{file_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the CSV file name
csv_file_name = "flores dev Egyptian Arabic.csv"

# Call the function to delete the first row
delete_first_row(csv_file_name)
