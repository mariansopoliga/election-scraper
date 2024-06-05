# election-scraper

A project for the Engeto Online Python Academy.

This project is used to extract and process the results of the 2017 parliamentary elections in Czech republic, 
parsing the data into a structured format and saving it as a CSV file.

Link to view: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ <br><br>

**Getting Started**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.<br><br>

**Prerequisites**

What things you need to install the software and how to install them:

Python 3.x<br>
Pip (Python package installer)<br>
Virtual environment tool (optional but recommended)<br><br>

**Installing**

1.A step-by-step series of examples that tell you how to get a development environment running:

git clone https://github.com/mariansopoliga/election-scraper.git
cd election-scraper<br>
2.Create and activate a virtual environment (optional but recommended):
python -m venv venv<br><br>

### On Windows
venv\Scripts\activate
### On macOS/Linux
source venv/bin/activate

3.Install the required packages:

pip install -r requirements.txt<br><br>

**Deployment**

To deploy this project on a live system, follow these steps:
Ensure all dependencies are installed and the environment is correctly set up:

Follow the steps in the Installing section to set up the environment and install dependencies.
Run the script to generate the CSV file:

**Voting results for the district Prague**

Use the command:
python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" prague.csv

1. argument:https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100
2. argument:prague.csv

This command fetches the election data from the given URL and saves it to prague.csv.<br><br>

**Download progress:**

Downloading data from the selected district... Prague 1
Data has been written to 'Path\Election Scraper\prague.csv'
Ending election_scraper<br><br>

**Partial output**

Number of municipality | Name of municipality | Voters on the list | Ballots issued | Valid valid_votes 
500054 | Praha 1 | 21 556 | 14 167 | 14 036 
500224 | Praha 10 | 79 964 | 52 277 | 51 895 <br><br>

**Monitor and maintain:**

Ensure the system where the script runs has network access to fetch the data.
Regularly check output files to ensure the script runs successfully.<br><br>

**Built With**

BeautifulSoup - Used for parsing HTML
Pandas - Used for data manipulation and analysis
Requests - Used for making HTTP requests<br><br>

**Authors: Marian Sopoliga**





