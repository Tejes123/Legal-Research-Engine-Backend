import os
import requests
from bs4 import BeautifulSoup

# Function to fetch the section content from a given document URL
def fetch_section_content(section_url, save_path):
    response = requests.get(section_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting title (from h1 tag)
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = 'No Title Found'
        
        # Extracting section content (typically inside div with class 'judgments')
        content_div = soup.find('div', class_='judgments')
        if content_div:
            content = content_div.get_text(separator='\n').strip()
        else:
            content = 'No Content Found'

        # Extracting section metadata (section numbers, document references, etc.)
        metadata = ''
        for meta in soup.find_all('table'):
            metadata += meta.get_text(separator='\n').strip() + "\n"
        
        # File naming and cleaning for file system compatibility
        safe_title = title[:50].replace(' ', '_').replace('/', '_').replace('\\', '_')
        file_path = os.path.join(save_path, f"{safe_title}.txt")
        
        # Save the section content and metadata to a text file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write(f"Metadata: \n{metadata}\n\n")
            f.write(f"Content: \n{content}")
        
        print(f"Saved: {file_path}")
    else:
        print(f"Failed to retrieve section content from {section_url}")

# Ensure the save path exists
save_path = 'data/constitution/'
os.makedirs(save_path, exist_ok=True)

# Example usage with the link you provided
fetch_section_content('https://indiankanoon.org/doc/237570/', save_path)
