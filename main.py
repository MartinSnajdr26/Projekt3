"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Martin Snajdr
email: martin.snajdr.japan@gmail.com
"""

import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def get_soup(url):
    """Fetches and parses an HTML page."""
    response = requests.get(url)
    response.encoding = "utf-8"
    if response.status_code != 200:
        print(f"Error loading page: {url}")
        sys.exit(1)
    soup = BeautifulSoup(response.text, 'html.parser')

    ##print("DEBUG: Soup has been retrieved for", url)  # Přidej debug info sem
    return soup

def get_municipality_links(base_url):
    """Scrapes all municipalities and their links from the main page."""
    soup = get_soup(base_url)
    municipalities = []

    tables = soup.find_all("table", class_="table")
    for table in tables:
        rows = table.find_all("tr")[2:]  # Skip headers
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            code = cols[0].text.strip()
            name = cols[1].text.strip()
            detail_link = cols[0].find("a")

            if detail_link:
                municipality_url = BASE_URL + detail_link["href"]
                municipalities.append((code, name, municipality_url))

    return municipalities

def scrape_municipality_results(url, all_parties):
    """Scrapes election results for a specific municipality."""
    soup = get_soup(url)
    ##print(f"DEBUG: Extracting tables from {url} - Found {len(tables)} tables")

    tables = soup.find_all("table")
    if len(tables) < 2:
        print(f"Error: Invalid structure at {url}")
        return [], {}

    # První tabulka obsahuje volební statistiky
    stats_table = tables[0]

    def get_stat_value(headers_value):
        """Najde hodnotu v tabulce podle headers atributu."""
        cell = stats_table.find("td", {"headers": headers_value})
        return cell.text.strip().replace("\xa0", "").replace(",", ".") if cell else "0"

    registered_voters = get_stat_value("sa2")  # Voliči v seznamu
    envelopes_issued = get_stat_value("sa3")  # Vydané obálky
    valid_votes_percentage = get_stat_value("sa7")  # % platných hlasů

    stats = [registered_voters, envelopes_issued, valid_votes_percentage]


    # Politické strany a jejich hlasy
    party_votes = {}
    for table in tables[1:]:  # Zbývající tabulky obsahují volební výsledky stran
        rows = table.find_all("tr")[2:]  # Přeskočit hlavičku
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:  # Ujistíme se, že jde o platný řádek
                continue
            party_name = cols[1].text.strip()
            vote_count = cols[2].text.strip().replace("\xa0", "").replace(",", ".")

            party_votes[party_name] = vote_count
            all_parties.add(party_name)  # Shromáždit všechny unikátní strany

    return stats, party_votes


def save_results_to_csv(data, all_parties, filename):
    """Saves election results to a CSV file with correct headers."""
    base_headers = ["code", "location", "registered", "envelopes", "valid"]
    sorted_parties = sorted(all_parties)  # Sort party names alphabetically
    full_headers = base_headers + sorted_parties  # Ensure headers match all possible parties

    print(f"Total unique parties found: {len(sorted_parties)}")  # Debugging info

    # Normalize all rows to have the same columns
    formatted_data = []
    for row in data:
        code, location, stats, votes = row
        row_dict = {party: votes.get(party, "0") for party in sorted_parties}  # Fill missing party data with "0"
        formatted_row = [code, location] + stats[:3] + [row_dict[party] for party in sorted_parties]
        
        if len(formatted_row) != len(full_headers):
            print(f"❌ ERROR: Mismatch detected in row: {formatted_row}")
            print(f"Expected columns: {len(full_headers)}, Got: {len(formatted_row)}")
            print(f"Fixing by adding missing columns...")
        
        while len(formatted_row) < len(full_headers):
            formatted_row.append("0")  # Fill missing values with "0"
        
        formatted_data.append(formatted_row)

    # Print sample row for debugging
    print(f"✅ Sample row (final): {formatted_data[0]}")  
    print(f"✅ Expected column count: {len(full_headers)}")  
    print(f"✅ Final dataset size: {len(formatted_data)} rows")

    df = pd.DataFrame(formatted_data, columns=full_headers)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ Results saved to: {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python projekt_3.py <URL of the region> <Output CSV file>")
        sys.exit(1)

    base_url = sys.argv[1]
    output_file = sys.argv[2]

    if not base_url.startswith(BASE_URL + "ps32"):
        print("Error: Invalid URL format. Ensure you're entering the correct election results page.")
        sys.exit(1)

    municipalities = get_municipality_links(base_url)
    results = []
    all_parties = set()  # Track all parties across municipalities

    for code, name, url in municipalities:
        stats, party_votes = scrape_municipality_results(url, all_parties)
        results.append((code, name, stats, party_votes))

    save_results_to_csv(results, all_parties, output_file)



