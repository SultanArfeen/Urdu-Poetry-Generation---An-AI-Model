import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define junk phrases to filter out unwanted lines
JUNK_PHRASES = {
    "Share this", "Critique", "Comments", "Download", "See Ghazal",
    "Tags", "and 3 more", "Amjad Islam Amjad", "Shakeb Jalali", 
    "Obaidullah Aleem", "Abbas Tabish", "Zeb Ghauri"
}

def clean_line(line: str) -> str:
    """Clean each line (e.g., strip whitespace)."""
    return line.strip()

def scrape_rekhta_page(url: str, label: str, csv_path: str, session: requests.Session):
    """
    Scrapes a Rekhta page for shers and appends them to csv_path.
    Inserts a label row before the shers to indicate the source page.
    """
    print(f"Scraping page: {url}")
    try:
        response = session.get(url, timeout=10)
        response.encoding = "utf-8"  # Ensure proper encoding
        if response.status_code != 200:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
            return
    except Exception as e:
        print(f"Error occurred while fetching {url}: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all div elements with class 'sherSection'
    poetry_elements = soup.find_all("div", class_="sherSection")
    
    poems = []
    poems.append(f"### {label} ###")  # Label header
    
    # Process each sherSection
    for element in poetry_elements:
        # Extract text, split by newline, and filter junk lines
        raw_lines = element.get_text(separator="\n", strip=True).split("\n")
        filtered_lines = [
            clean_line(ln)
            for ln in raw_lines
            if ln and not any(junk in ln for junk in JUNK_PHRASES)
        ]
        poem_text = " ".join(filtered_lines)
        if poem_text:
            poems.append(poem_text)
    
    # Convert list of poems into a DataFrame
    df_new = pd.DataFrame(poems, columns=["poetry"])
    
    # Append to CSV (create new file if needed)
    if os.path.exists(csv_path):
        df_new.to_csv(csv_path, mode="a", index=False, header=False, encoding="utf-8")
    else:
        df_new.to_csv(csv_path, index=False, encoding="utf-8")
    
    print(f"Appended {len(poems) - 1} shers under '{label}' to {csv_path}.\n")

if __name__ == "__main__":
    # Define CSV file path (saved in the same directory as this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "urdu_poetry.csv")
    
    # List of pages to scrape with labels
    pages = [
        ("https://rekhta.org/poets/amjad-islam-amjad/t20", "Amjad Islam Amjad (t20)"),
        ("https://rekhta.org/poets/shakeb-jalali/t20", "Shakeb Jalali (t20)"),
        ("https://rekhta.org/poets/obaidullah-aleem/t20", "Obaidullah Aleem (t20)"),
        ("https://rekhta.org/poets/abbas-tabish/t20", "Abbas Tabish (t20)"),
        ("https://rekhta.org/poets/zeb-ghauri/t20", "Zeb Ghauri (t20)")
    ]
    
    with requests.Session() as session:
        for url, label in pages:
            scrape_rekhta_page(url, label, csv_file, session)
            # Optional: small delay between requests
            time.sleep(1)
    
    print("Scraping complete. Data saved in 'urdu_poetry.csv'.")
