####################_Header_####################
'''
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Marian Sopoliga
email: sopoligamarian@gmail.com
discord: Marian S.
'''

####################_Import requested libraries_####################

import os
import sys
import time
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Tuple, Dict


####################_Fetch and parse HTML content from a URL_####################

def fetch_and_parse_election_html_data(url: str) -> Optional[BeautifulSoup]:
    """Fetch and parse HTML content from a URL.

    Makes a GET request to the provided URL with custom headers and a timeout,
    then parses the HTML content using BeautifulSoup.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        Optional[BeautifulSoup]: Parsed HTML content as a BeautifulSoup object,
        or None if an error occurred.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.110 Safari/537.3'
        )
    }
    try:
        # Make a GET request to the URL with headers and timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # Return the parsed HTML content if no exceptions occur
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 404, 500 errors)
        print(f"HTTP error occurred while fetching URL {url}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        # Handle connection errors (e.g., DNS failure, refused connection)
        print(f"Connection error occurred while fetching URL {url}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        # Handle timeout errors (e.g., slow response)
        print(f"Timeout occurred while fetching URL {url}: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        # Catch any other request exceptions (e.g., invalid URL)
        print(f"Request error occurred while fetching URL {url}: {req_err}")
    except ValueError as val_err:
        # Handle value errors (e.g., content decoding issues)
        print(f"Value error occurred while parsing data from URL {url}: {val_err}")
    except Exception as err:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred while fetching URL {url}: {err}")
    # Return None if an exception occurred
    return None


####################_Fetch HTML tables from an election data page_####################

def fetch_voting_results_territorial_units_municipality_selection_tables(
        url: str, municipality_name: str, table_index: Optional[List[int]] = None) -> List[BeautifulSoup]:
    """Fetch HTML tables from an election data page based on the given table indices.

    Args:
        url (str): The URL of the election data page.
        municipality_name (str): The name of the municipality to search for.
        table_index (Optional[List[int]]): List of indices specifying which tables to fetch.

    Returns:
        List[BeautifulSoup]: List of parsed HTML tables.
    """
    try:
        # Fetching and parsing the HTML content of the page
        soup = fetch_and_parse_election_html_data(url)
        if soup is None:
            print(f"Failed to fetch and parse data from {url}")
            return []

        # Extracting all tables from the parsed HTML content
        tables = soup.find_all('table')
        if not tables:
            print(f"No tables found in the parsed data from {url}")
            return []

        # If no specific table indices are provided, return all tables
        if table_index is None:
            return tables

        # Return only the tables with specified indices
        return [tables[i] for i in table_index if 0 <= i < len(tables)]

    except Exception as err:
        # Catching any unexpected errors during the table fetching process
        print(f"An unexpected error occurred: {err}")
        return []


####################_Parse and return tables containing municipality selection data_####################

def parse_voting_results_territorial_units_municipality_selection_tables(url: str) -> List[BeautifulSoup]:
    """Parse and return tables containing municipality selection data.

    Args:
        url (str): The URL of the election data page.

    Returns:
        List[BeautifulSoup]: List of parsed HTML tables.
    """
    return fetch_voting_results_territorial_units_municipality_selection_tables(
        url, "all municipalities", table_index=[0, 1, 2]
    )


####################_Parse and return the table containing district election data_####################

def parse_voting_results_territorial_units_districts(
        municipality_detail_url: str, municipality_name: str) -> Optional[BeautifulSoup]:
    """Parse and return the table containing district election data.

    Args:
        municipality_detail_url (str): URL of the municipality's detail page.
        municipality_name (str): Name of the municipality.

    Returns:
        Optional[BeautifulSoup]: The parsed HTML table or None.
    """
    if municipality_name.lower() != "all municipalities":
        # Log downloading data for a specific district
        print(f"Downloading data from the selected district... {municipality_name}")

    # Retrieve tables from the municipality's detail page
    tables = fetch_voting_results_territorial_units_municipality_selection_tables(
        municipality_detail_url, municipality_name, table_index=[0]
    )
    return tables[0] if tables else None


####################_Parse and return tables containing political party election data_####################

def parse_voting_results_territorial_units_political_parties(
        url: str, municipality_name: str) -> List[BeautifulSoup]:
    """Parse and return tables containing political party election data.

    Args:
        url (str): The URL of the municipality's detail page.
        municipality_name (str): Name of the municipality.

    Returns:
        List[BeautifulSoup]: List of parsed HTML tables.
    """
    return fetch_voting_results_territorial_units_municipality_selection_tables(
        url, municipality_name, table_index=[1, 2]
    )


####################_Process and extract election data from the municipality selection tables_####################

def process_voting_results_territorial_units_municipality_selection_tables(
        municipality_tables: List[BeautifulSoup], base_url: str) -> Tuple[List[Tuple[str, str, str, str, str]], Dict[str, List[Tuple[str, str]]]]:
    """Process and extract election data from the municipality selection tables.

    Args:
        municipality_tables (List[BeautifulSoup]): List of HTML tables containing municipality data.
        base_url (str): Base URL to resolve relative links.

    Returns:
        Tuple[List[Tuple[str, str, str, str, str]], Dict[str, List[Tuple[str, str]]]]:
            Tuple containing two elements:
                - List of tuples representing municipality data.
                - Dictionary mapping municipality names to lists of tuples representing political party data.
    """
    # Initialize lists and dictionaries to hold processed data
    all_municipalities_data = []
    all_political_parties_data = {}

    for municipality_table in municipality_tables:
        # Skip the header row (first row)
        rows = municipality_table.find_all('tr')[1:]
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                municipality_number = columns[0].text.strip()
                municipality_name = columns[1].text.strip()
                anchor_tag = columns[0].find('a')
                if anchor_tag:
                    # Resolve the municipality's detail page URL
                    municipality_detail_url = urljoin(base_url, anchor_tag['href'])
                    try:
                        # Parse and process the election data for districts
                        municipality_number_and_name_table = parse_voting_results_territorial_units_districts(
                            municipality_detail_url, municipality_name
                        )
                        if municipality_number_and_name_table:
                            process_voting_results_territorial_units_districts(
                                municipality_number_and_name_table,
                                municipality_number,
                                municipality_name,
                                all_municipalities_data
                            )
                        # Parse and process the election data for political parties
                        political_party_tables = parse_voting_results_territorial_units_political_parties(
                            municipality_detail_url, municipality_name
                        )
                        process_voting_results_territorial_units_political_parties(
                            political_party_tables,
                            all_political_parties_data,
                            municipality_name
                        )
                        # Delay to avoid overwhelming the server
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error processing data for {municipality_name}: {e}")

    return all_municipalities_data, all_political_parties_data


####################_Process election results data specific to territorial units_####################

def process_voting_results_territorial_units_districts(
        voting_results_table: BeautifulSoup, municipality_number: str,
        municipality_name: str, all_municipalities_data: List[Tuple[str, str, str, str, str]]) -> None:
    """Process election results data specific to territorial units.

    Args:
        voting_results_table (BeautifulSoup): Parsed HTML table with election data.
        municipality_number (str): Municipality number.
        municipality_name (str): Municipality name.
        all_municipalities_data (List[Tuple[str, str, str, str, str]]): List to store processed data.
    """
    if not voting_results_table:
        return

    # Skip the header row (first row)
    rows = voting_results_table.find_all('tr')[1:]
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 8:
            voters_on_list = columns[3].text.strip()
            ballots_issued = columns[4].text.strip()
            valid_valid_votes = columns[7].text.strip()
            # Add processed data to the list
            all_municipalities_data.append(
                (municipality_number, municipality_name, voters_on_list,
                 ballots_issued, valid_valid_votes)
            )


####################_Extract and process data related to political parties_####################

def process_voting_results_territorial_units_political_parties(
        political_party_tables: List[BeautifulSoup], all_political_parties_data: Dict[str, List[Tuple[str, str]]], municipality_name: str) -> None:
    """Extract and process data related to political parties.

    Args:
        political_party_tables (List[BeautifulSoup]): List of HTML tables containing political party data.
        all_political_parties_data (Dict[str, List[Tuple[str, str]]]): Dictionary to store processed data.
        municipality_name (str): Name of the municipality.
    """
    if not political_party_tables:
        return

    for table in political_party_tables:
        # Skip the first two rows (headers)
        rows = table.find_all("tr")[2:]
        for row in rows:
            cells = row.find_all(["th", "td"])
            if len(cells) >= 2:
                party_name = cells[1].text.strip()
                valid_votes = cells[2].text.strip()

                # Initialize the municipality's political party data if not already initialized
                if municipality_name not in all_political_parties_data:
                    all_political_parties_data[municipality_name] = []

                # Add processed data to the dictionary
                all_political_parties_data[municipality_name].append((party_name, valid_votes))


####################_Write the collected election data to a CSV file_####################

def write_election_data_to_csv(
        all_political_parties_data: Dict[str, List[Tuple[str, str]]],
        all_municipalities_data: List[Tuple[str, str, str, str, str]], filename: str) -> None:
    """Write the collected election data to a CSV file.

    Args:
        all_political_parties_data (Dict[str, List[Tuple[str, str]]]): Dictionary of political party data.
        all_municipalities_data (List[Tuple[str, str, str, str, str]]): List of municipality data.
        filename (str): Output CSV filename.
    """
    if not all_political_parties_data or not all_municipalities_data:
        print("No data available")
        return

    # Create a DataFrame with the appropriate column headers
    df = pd.DataFrame(columns=["Municipality Number", "Municipality Name",
                               "Voters on List", "Ballots Issued", "Valid Votes"])
    # Extract party names from the first municipality's data
    create_header_row = next(iter(all_political_parties_data.values()))
    political_party_names = [party for party, _ in create_header_row]
    df = pd.concat([df, pd.DataFrame(columns=political_party_names)], axis=1)

    # Populate the DataFrame with processed data
    for (municipality_name, political_party_data), municipality_info in zip(
            all_political_parties_data.items(), all_municipalities_data):
        row_data = list(municipality_info)
        valid_votes_data = [valid_votes for _, valid_votes in political_party_data]
        row_data.extend(valid_votes_data)
        df = pd.concat([df, pd.DataFrame([row_data], columns=df.columns)], ignore_index=True)

    file_path = os.path.join(os.getcwd(), filename)
    try:
        # Write the DataFrame to a CSV file
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Data has been written to '{file_path}'")
    except Exception as e:
        print(f"Error writing to CSV file {file_path}: {e}")


####################_Check if a given URL is valid_####################

def is_valid_url(url: str) -> bool:
    """Check if a given URL is valid.

    Args:
        url (str): URL string to validate.

    Returns:
        bool: True if the URL is valid, otherwise False.
    """
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])


####################_Main function_####################

def main() -> None:
    """Main function to parse command-line arguments and call appropriate functions."""
    if len(sys.argv) != 3:
        # Print usage instructions if arguments are incorrect
        print("Example: python script_name.py 'https://example.com/data' 'output.csv'")
        print("Error: Missing or incorrect number of arguments.")
        return

    url = sys.argv[1]
    filename = sys.argv[2]

    if not is_valid_url(url):
        # Validate the provided URL
        print("Invalid URL format. Please provide a valid URL.")
        print("Example: 'https://example.com/data'")
        return

    if not filename.endswith('.csv'):
        # Validate the provided filename
        print("Invalid CSV file. Please provide a file ending with '.csv'")
        print("Example: 'output.csv'")
        return

    # Process the municipality selection tables and extract data
    all_municipalities_data, all_political_parties_data = process_voting_results_territorial_units_municipality_selection_tables(
        parse_voting_results_territorial_units_municipality_selection_tables(url), url
    )

    if all_municipalities_data and all_political_parties_data:
        # Write the extracted data to a CSV file
        write_election_data_to_csv(all_political_parties_data, all_municipalities_data, filename)
    else:
        # Print error messages if no data is found
        print(
            "No election data was found. Possible reasons:\n"
            "- The URL is invalid or inaccessible.\n"
            "- The data source is missing or incomplete.\n"
            "Please verify the URL and the availability of data, then try again."
        )

    print("Ending election_scraper")


if __name__ == "__main__":
    main()
