# PubMed Paper Fetcher

This project allows users to fetch research papers from PubMed, filter authors based on their affiliations, and export the results into a CSV file.

## Project Structure

```
├── fetchpaper.py   # Core logic for fetching and parsing PubMed articles
├── cli.py          # Command-line interface script
├── requirements.txt # List of dependencies
├── README.md       # Project documentation
├── pyproject.toml  # Poetry project configuration
└── pubmed_papers.csv  # Output file containing fetched results
```

## Installation

### Prerequisites
- Python 3.8+
- Poetry package manager

### Steps to Install and Run
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/pubmed-paper-fetcher.git
   cd pubmed-paper-fetcher
   ```

2. **Install Poetry (if not already installed)**
   ```sh
   pip install poetry
   ```

3. **Install Dependencies**
   ```sh
   poetry install
   ```

4. **Run the CLI Command**
   ```sh
   poetry run get_papers "covid-19 vaccine" -f results.csv
   ```
   This will fetch papers related to "covid-19 vaccine" and save them in `results.csv`.

### Making the Script Globally Executable
Ensure that the Poetry virtual environment’s `bin` or `Scripts` directory is added to your `PATH`.
```sh
   get_papers "covid-19 vaccine" -f results.csv
```


## Tools & Libraries Used
- **Python**: The programming language used for development.
- **Poetry**: Dependency management tool ([Poetry Docs](https://python-poetry.org/))
- **Requests**: HTTP library for fetching data from PubMed API ([Requests Docs](https://docs.python-requests.org/en/latest/))
- **XML Parsing (ElementTree)**: Extracting relevant data from PubMed XML responses ([ElementTree Docs](https://docs.python.org/3/library/xml.etree.elementtree.html))
- **NCBI E-utilities API**: Used to search and fetch PubMed articles ([NCBI API Docs](https://www.ncbi.nlm.nih.gov/books/NBK25497/))

## Author
Developed by Anupama Minj

## License
This project is licensed under the MIT License.

