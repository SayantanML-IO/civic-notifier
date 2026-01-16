import yaml
import os                            # Added: To access system environment variables
from dotenv import load_dotenv       # Added: To read the .env file

# Load environment variables from .env file immediately
load_dotenv()

from scraper import get_links_from_url, download_pdf, extract_text_from_pdf, find_keywords_in_text
from notifier import send_email_alert

def load_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None

def load_processed_links(file_path='processed_links.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_processed_link(link, file_path='processed_links.txt'):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(link + '\n')

if __name__ == "__main__":
    config = load_config()
    if not config:
        exit("Could not load configuration. Exiting.")

    processed_links = load_processed_links()
    print(f"Loaded {len(processed_links)} previously processed links.")
    
    keywords = config.get('keywords', [])
    new_finds = []

    for site in config.get('sites_to_monitor', []):
        print("-" * 30)
        pdf_links = get_links_from_url(site['url'])
        
        new_links = [link for link in pdf_links if link not in processed_links]
        print(f"Found {len(pdf_links)} total links, {len(new_links)} are new.")

        for link in new_links:
            print(f"Processing new link: {link}")
            pdf_path = download_pdf(link)
            if pdf_path:
                text = extract_text_from_pdf(pdf_path)
                if text:
                    matching_keywords = find_keywords_in_text(text, keywords)
                    if matching_keywords:
                        print(f" KEYWORDS FOUND! ")
                        print(f"  Keywords: {', '.join(matching_keywords)}")
                        new_finds.append({'link': link, 'keywords': matching_keywords})
                    else:
                        print("  -> No relevant keywords found.")
            save_processed_link(link)

    print("\n" + "="*50)
    if new_finds:
        print(f"Found {len(new_finds)} new documents with keywords. Sending notification...")
        email_subject = "Civic Notifier Alert: New Documents Found!"
        email_body = "Hello,\n\nThe Civic Notifier found new documents matching your keywords:\n\n"
        for find in new_finds:
            email_body += f"- Link: {find['link']}\n"
            email_body += f"  Keywords: {', '.join(find['keywords'])}\n\n"
        send_email_alert(email_subject, email_body, config)
    else:
        print("No new documents with keywords found in this run.")