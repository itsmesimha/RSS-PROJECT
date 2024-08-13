import pandas as pd

# File paths
keywords_file = r'C:\Users\itsme\PycharmProjects\rssfeedcjp\keywords.xlsx'
compiled_file = r'C:\Users\itsme\PycharmProjects\rssfeedcjp\output_file_2024-08-08_14-28-38.xlsx'
output_file = 'matching_keywords.xlsx'

# Step 1: Read the keywords from the Excel file
keywords_df = pd.read_excel(keywords_file)
keywords = keywords_df['Keyword'].dropna().tolist()  # Drop NaNs and convert to list

# Step 2: Read the compiled RSS feed data
compiled_df = pd.read_excel(compiled_file)

# Function to check if any keyword is in the title or description
def contains_keyword(title, description, keywords):
    title = title if pd.notna(title) else ''
    description = description if pd.notna(description) else ''
    return any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords)

# Filter rows where the title or description contains any of the keywords
filtered_df = compiled_df[compiled_df.apply(lambda row: contains_keyword(row['Title'], row['Description'], keywords), axis=1)]

# Step 3: Save the filtered DataFrame to an Excel file without the Matching Keyword column
filtered_df.to_excel(output_file, index=False)

print(f'Filtered data has been successfully saved to {output_file}')
