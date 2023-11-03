import csv
import sys
from datetime import datetime

# Define the source and destination file names
source_file = sys.argv[1]
destination_file = 'destination.csv'

# Define the encoding used in your source CSV (e.g., UTF-16)
source_encoding = 'utf-16'

# Define the delimiter used in the source CSV (assuming it's a tab character)
source_delimiter = ','

# Define a mapping of column names from the source CSV to the destination CSV
column_mapping = {
    'Date': 'date',
    'Title': 'name',
    'Category': 'categoryName',
    'Account': 'accountName',
    'Amount': 'amount',
    'Currency': 'currency',
    'Description': 'note',
    # Add more column mappings as needed
}

# Open the source CSV file for reading with the specified encoding
with open(source_file, 'r', encoding=source_encoding) as source_csv_file:
    # Create a CSV reader object with the specified delimiter
    csv_reader = csv.DictReader(source_csv_file, delimiter=source_delimiter)

    # Read and process the data from the source CSV file
    processed_data = []
    for row in csv_reader:
        # Remove non string keys
        del row[None]

        # Replace the old csv columns with new columns using the abova map
        row = {x.strip():y.strip() for x,y in row.items()}
        new_row = {column_mapping[x]:row[x] for x in column_mapping.keys()}

        new_row['colour'] = ''
        new_row['iconName'] = ''

        # Some rows had empty dates ignoring them
        if row['Date'] == '':
            continue

        # Convert string to datetime object
        new_row['date'] = datetime.strptime(new_row['date'], '%d/%m/%Y %H:%M')

        if row['Type'] == 'TRANSFER':
            # Add Cashew specific columns
            new_row['categoryName'] = 'Balance Correction'
            new_row['note'] = f'Transferred Balance\n{row["Account"]} → {row["To Account"]}'
            new_row['amount'] = row['Transfer Amount']
            new_row['income'] = 'TRUE'
            new_row['colour'] = '0xff607d8b'
            new_row['iconName'] = 'charts.png'
            new_row['accountName'] = row['To Account']
            processed_data.append(new_row)

            # Cashew treats transfer as expense and income
            #Duplicating the rows and changing values accordingly
            temp_row = new_row.copy()
            temp_row['amount'] = '-' + row['Transfer Amount']
            temp_row['income'] = 'FALSE'
            temp_row['accountName'] = row['Account'] 
            processed_data.append(temp_row)

        elif row['Type'] == 'INCOME':
            new_row['income'] = 'TRUE'
            processed_data.append(new_row)

        elif row['Type'] == 'EXPENSE':
            new_row['income'] = 'FALSE'
            processed_data.append(new_row)

# Open the destination CSV file for writing
with open(destination_file, 'w+') as destination_csv_file:
    # Create a CSV writer object
    csv_writer = csv.DictWriter(destination_csv_file, fieldnames=processed_data[0].keys())
    csv_writer.writeheader()

    # Write the processed data to the destination CSV file
    csv_writer.writerows(processed_data)

print(f"Conversion completed. Data written to {destination_file}")
