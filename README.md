# PubMed Paper Fetcher

This project allows users to fetch research papers from PubMed, filter authors based on their affiliations, and export the results into a CSV file.

## Project Structure

- `src/` - Contains the main source code.
  - `fetchpaper.py` - Fetches PubMed papers and extracts relevant details.
  - `cli.py` - Command-line interface for fetching papers.
- `tests/` - Contains test cases.
- `pyproject.toml` - Project configuration for Poetry.
- `poetry.lock` - Dependency lock file.
- `README.md` - Documentation.

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
   poetry run get_papers "query" -f results.csv
   ```
   This will fetch papers related to "query" and save them in `results.csv`.

### Making the Script Globally Executable
To run the script without `poetry run`, install it globally:
```bash
poetry install
poetry run pip install --editable .
get_papers "query" -f results.csv
```
#### Or

Ensure that the Poetry virtual environment’s `bin` or `Scripts` directory is added to your `PATH`.
```sh
   get_papers "query" -f results.csv
```
eg. get_papers "gene therapy" --debug --file output.csv
This will fetch PubMed articles related to "gene therapy" and save them in `results.csv`.

### Command-line Options
- `-h` or `--help` : Display usage instructions.
- `-d` or `--debug` : Print debug information during execution.
- `-f` or `--file` : Specify the filename to save the results. If not provided, the output is printed to the console.


## Tools & Libraries Used
- **Python**: The programming language used for development.
- **Poetry**: Dependency management tool ([Poetry Docs](https://python-poetry.org/))
- **Requests**: HTTP library for fetching data from PubMed API ([Requests Docs](https://docs.python-requests.org/en/latest/))
- **XML Parsing (ElementTree)**: Extracting relevant data from PubMed XML responses ([ElementTree Docs](https://docs.python.org/3/library/xml.etree.elementtree.html))
- **NCBI E-utilities API**: Used to search and fetch PubMed articles ([NCBI API Docs](https://www.ncbi.nlm.nih.gov/books/NBK25497/))