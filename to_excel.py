import os
import pandas as pd
import json

# Set the path to the folder containing the JSON files
folder_path = 'jsonFiles/.'

# Create an empty list to store the DataFrames
dfs = []

# Iterate over the JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)

        # Read the JSON file into a dictionary
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Convert the dictionary into a DataFrame
        temp_df = pd.DataFrame.from_records([data])

        # Append the temporary DataFrame to the list
        dfs.append(temp_df)

# Concatenate all DataFrames in the list into a single DataFrame
df = pd.concat(dfs, ignore_index=True)

# Create a new Excel file and save the DataFrame
output_path = 'file.xlsx'
df.to_excel(output_path, index=False)
