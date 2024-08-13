import pandas as pd
import feedparser
from dateutil import parser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Read the RSS feed URLs and feed names from the input Excel
input_file = r'C:\Users\itsme\PycharmProjects\rssfeedcjp\RSS_Feed_Tracker.xlsx'
df = pd.read_excel(input_file, header=None)  # Read without headers
rss_feed_urls = df[0]  # Get URLs from the first column
feed_names = df[1]  # Get feed names from the second column

# Function to parse RSS feeds and extract content
def parse_rss_feed(url):
    feed = feedparser.parse(url)
    # Feed name now comes from the input Excel file
    feed_name = 'No Title'  # Default value in case of issues
    entries = []

    for item in feed.entries:
        title = item.get('title', 'No Title')
        description = item.get('description', 'No Description')
        link = item.get('link', 'No Link')
        published = item.get('published', 'No Publish Date')

        if published != 'No Publish Date':
            published = parser.parse(published).replace(tzinfo=None)  # Make timezone unaware

        # Extract content from the URL
        content = extract_content_from_url(link)

        entries.append({
            'Title': title,
            'Description': description,
            'Link': link,
            'Published Date': published,
            'Content': content  # Add content to entries
        })

    return feed_name, entries

def extract_content_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text(separator=' ', strip=True)
        return content
    except Exception as e:
        return 'Error: ' + str(e)

# Collect the data
data = []
for url, name in zip(rss_feed_urls, feed_names):
    feed_name, entries = parse_rss_feed(url)
    for entry in entries:
        data.append({
            'RSS Feed URL': url,
            'Feed Name': name,  # Use feed name from Excel
            'Title': entry['Title'],
            'Description': entry['Description'],
            'Link': entry['Link'],
            'Published Date': entry['Published Date'],
            'Content': entry['Content']  # Add content to data
        })

# Create a DataFrame and write to Excel with date and time
output_df = pd.DataFrame(data)

# Generate filename with current date and time
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_file = fr"C:\Users\itsme\PycharmProjects\rssfeedcjp\output_file_{timestamp}.xlsx"

output_df.to_excel(output_file, index=False)