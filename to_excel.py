import os
import pandas as pd
import json

# Set the path to the folder containing the JSON files
folder_path = 'jsonFiles'

# Create a folder named "sheets" in the current directory
sheets_folder = os.path.join(os.getcwd(), 'sheets')
os.makedirs(sheets_folder, exist_ok=True)

# Iterate over the directories in the folder
for country_dir in os.listdir(folder_path):
    country_dir_path = os.path.join(folder_path, country_dir)

    # Check if the item in the folder is a directory
    if os.path.isdir(country_dir_path):
        # Create an empty list to store the DataFrames for the country
        dfs = []

        # Iterate over the JSON files in the country directory
        for filename in os.listdir(country_dir_path):
            if filename.endswith('.json'):
                file_path = os.path.join(country_dir_path, filename)

                # Read the JSON file into a dictionary
                with open(file_path, 'r') as file:
                    data = json.load(file)

                # Convert the dictionary into a DataFrame
                temp_df = pd.DataFrame.from_records([data])

                # Append the temporary DataFrame to the list
                dfs.append(temp_df)

        # Concatenate all DataFrames in the list into a single DataFrame
        df = pd.concat(dfs, ignore_index=True)

        # Create a new Excel file and save the DataFrame in the sheets folder
        output_path = os.path.join(sheets_folder, f'{country_dir}.xlsx')
        df.to_excel(output_path, index=False)
