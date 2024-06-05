# Election Scraper

A project for the Engeto Online Python Academy.

This project is used to extract and process the results of the 2017 parliamentary elections in the Czech Republic, parsing the data into a structured format and saving it as a CSV file.

[Link to view](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.x
- Pip (Python package installer)
- Virtual environment tool (optional but recommended)

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/election-scraper.git
    cd election-scraper
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the script with the necessary arguments**:
  
**Voting results for the district Prague**:

Use the command:
```sh
python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" prague.csv
```
- **1st argument**: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100`
- **2nd argument**: `prague.csv`

This command fetches the election data from the given URL and saves it to `prague.csv`.

### Download Progress

Downloading data from the selected district... Prague 1
Data has been written to 'Path\Election Scraper\prague.csv'
Ending election_scraper

### Partial Output

- Number of municipality | Name of municipality | Voters on the list | Ballots issued | Valid votes

- 500054 | Praha 1 | 21 556 | 14 167 | 14 036
- 500224 | Praha 10 | 79 964 | 52 277 | 51 895

### Monitor and Maintain

- Ensure the system where the script runs has network access to fetch the data.
- Regularly check output files to ensure the script runs successfully.

## Built With

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Used for parsing HTML
- [Pandas](https://pandas.pydata.org/) - Used for data manipulation and analysis
- [Requests](https://docs.python-requests.org/en/master/) - Used for making HTTP requests

## Authors

- **Marian Sopoliga**

