import os
import glob
import pandas as pd

# Define the directory where the files are stored
directory = r'C:\Users\itsme\PycharmProjects\ex'

# Step 1: Identify the most recent and second most recent files based on timestamps
files = glob.glob(os.path.join(directory, 'output_file_*.xlsx'))

if len(files) < 2:
    raise ValueError("Not enough files to perform the comparison.")

# Sort the files by modification time (most recent first)
files.sort(key=os.path.getmtime, reverse=True)

# The most recent file is the new file, and the second most recent is the old file
new_file = files[0]
old_file = files[1]

output_file = os.path.join(directory, 'filtered_matching_keywords.xlsx')

# Step 2: Read the keywords from the Excel file
keywords_file = os.path.join(directory, 'keywords.xlsx')
try:
    keywords_df = pd.read_excel(keywords_file)
    keywords = keywords_df['Keyword'].dropna().tolist()  # Drop NaNs and convert to list

    # Step 3: Read the old and new data
    old_df = pd.read_excel(old_file)
    new_df = pd.read_excel(new_file)

    print("Old DataFrame:")
    print(old_df.head())

    print("New DataFrame:")
    print(new_df.head())

    # Compare the old and new data
    old_df.columns = old_df.columns.str.strip()
    new_df.columns = new_df.columns.str.strip()

    # Find new entries in the new file that are not in the old file
    comparison_df = pd.merge(new_df, old_df, how='left', on=['Title', 'Description'], indicator=True)
    new_entries_df = comparison_df[comparison_df['_merge'] == 'left_only'].drop(columns='_merge')

    print("Comparison DataFrame:")
    print(comparison_df.head())

    # Remove the old file after successfully processing
    os.remove(old_file)
    print(f"Old file {old_file} has been removed.")

    # Step 4: Filter the new entries based on keywords
    def contains_keyword(title, description, keywords):
        title = title if pd.notna(title) else ''
        description = description if pd.notna(description) else ''
        return any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords)

    filtered_df = new_entries_df[new_entries_df.apply(lambda row: contains_keyword(row['Title'], row['Description'], keywords), axis=1)]

    print("Filtered DataFrame:")
    print(filtered_df.head())

    # Save the filtered DataFrame to an Excel file
    if filtered_df.empty:
        print("No matching data found. Output file will not be created.")
    else:
        filtered_df.to_excel(output_file, index=False)
        print(f'Filtered data has been successfully saved to {output_file}')

except FileNotFoundError as e:
    print(f"Error: {e}")

except pd.errors.EmptyDataError as e:
    print(f"Error reading Excel file: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
