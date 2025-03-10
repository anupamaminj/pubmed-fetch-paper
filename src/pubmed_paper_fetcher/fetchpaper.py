import requests
import xml.etree.ElementTree as ET
import csv
import sys
from typing import List, Tuple, Optional
import re

# Define constants for PubMed API URLs
SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


# Keywords to identify company affiliations
COMPANY_KEYWORDS = [
    "Pharmaceuticals", "Pharma", "Biotech", "Genomics", "Diagnostics",
    "Therapeutics", "Life Sciences", "Biosciences", "BioPharma", 
    "Biologics", "Biomedical", "Vaccines", "Drug", "Healthcare", "MedTech",
    "Molecular", "Immunology", "Cell Therapy", "Gene Therapy", "Neuroscience"
]


# Keywords to exclude academic institutions
ACADEMIC_KEYWORDS = [
    "University", "Institute", "Research Center", "College", "School of Medicine", 
    "Medical Center", "Academic Hospital", "Teaching Hospital", "Education", "VA Medical", 
    "Geriatric Research", "Clinical Center", "National Institute", "Academy", "University", "Institute", "School", "College", "Academy", "Department", "Hospital", "Medical Center"
]


def fetch_pubmed_papers(query: str, max_results: int = 100, debug: bool = False) -> List[str]:
    """
    Fetch PubMed article IDs based on a user query.
    
    :param query: PubMed search query
    :param max_results: Maximum number of results to fetch
    :param debug: If True, prints debug messages
    :return: List of article IDs
    """
    if debug:
        print(f"Searching PubMed for: {query}")

    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }

    try:
        response = requests.get(SEARCH_URL, params=search_params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        search_data = response.json()
        article_ids = search_data.get("esearchresult", {}).get("idlist", [])

        if not article_ids:
            print("No papers found.")
            sys.exit(1)

        if debug:
            print(f"Found {len(article_ids)} papers: {article_ids}")

        return article_ids

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from PubMed: {e}")
        sys.exit(1)



def extract_company_name(affiliation: str) -> str:
    """ Extracts only the company name from an affiliation string. """
    # Remove email and address details
    company_name = re.sub(r",? *\d+.*$", "", affiliation)  # Remove address details
    company_name = re.sub(r"\. Electronic address:.*", "", company_name)  # Remove email
    
    return company_name.strip()

def fetch_paper_details(article_ids: List[str], debug: bool = False) -> List[Tuple[str, str, str, str, str, str]]:
    """
    Fetches detailed information about PubMed articles using EFetch API.
    
    :param article_ids: List of PubMed article IDs
    :param debug: If True, prints debug messages
    :return: List of tuples containing article details
    """
    if not article_ids:
        return []

    fetch_params = {
        "db": "pubmed",
        "id": ",".join(article_ids),
        "retmode": "xml"
    }

    try:
        response = requests.get(FETCH_URL, params=fetch_params)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        results = []
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID", default="Unknown")
            title = article.findtext(".//ArticleTitle", default="N/A")
            pub_date = article.findtext(".//PubDate/Year", default="Unknown")

            non_academic_authors = []  # Stores only author names
            company_affiliations = set()  # Stores unique company names
            emails = []  # Stores corresponding emails
            
            for author in article.findall(".//Author"):
                last_name = author.findtext("LastName", default="")
                fore_name = author.findtext("ForeName", default="")
                full_name = f"{fore_name} {last_name}".strip() if fore_name or last_name else "Unknown"
                
                for aff_info in author.findall(".//AffiliationInfo"):
                    affiliation = aff_info.findtext("Affiliation", default="")

                    # Check if affiliation belongs to a company
                    is_company = any(keyword.lower() in affiliation.lower() for keyword in COMPANY_KEYWORDS)
                    is_academic = any(keyword.lower() in affiliation.lower() for keyword in ACADEMIC_KEYWORDS)

                    if is_company and not is_academic:
                        # Extract email if present
                        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
                        email = email_match.group(0) if email_match else ""

                        # Add non-academic author name only
                        non_academic_authors.append(full_name)

                        # Extract and store company name (cleaned)
                        company_name = extract_company_name(affiliation)
                        company_affiliations.add(company_name)

                        # Store emails
                        if email and email not in emails:
                            emails.append(email)

            if non_academic_authors:
                results.append((
                    pmid, title, pub_date,
                    "; ".join(non_academic_authors),  # Only names
                    "; ".join(company_affiliations),  # Only company names
                    "; ".join(emails)  # Only emails
                ))

        return results

    except requests.RequestException as e:
        if debug:
            print(f"Error fetching data: {e}")
        return []



def save_to_csv(results: List[Tuple[str, str, str, str, str, str]], filename: str) -> None:
    """
    Saves research paper details to a CSV file.

    :param results: List of tuples containing paper details
    :param filename: Output CSV filename
    """
    if not results:
        print("No pharmaceutical/biotech-affiliated papers found.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writerows(results)

    print(f"Results saved to {filename}")


