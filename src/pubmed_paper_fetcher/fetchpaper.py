import requests
import xml.etree.ElementTree as ET
import csv
import sys
from typing import List, Tuple, Optional

# Define constants for PubMed API URLs
SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Keywords to identify non-academic affiliations
AFFILIATION_KEYWORDS = ["Pharma", "Biotech", "Genomics", "Diagnostics", "Therapeutics", "Life Sciences"]

def fetch_pubmed_papers(query: str, max_results: int = 20, debug: bool = False) -> List[str]:
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
            pmid = article.find(".//PMID").text
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
            pub_date = article.find(".//PubDate/Year")
            pub_date = pub_date.text if pub_date is not None else "Unknown"

            authors = []
            affiliations = []
            corresponding_email = ""

            for author in article.findall(".//Author"):
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                full_name = f"{fore_name.text} {last_name.text}" if fore_name is not None and last_name is not None else "Unknown"
                authors.append(full_name)

                affiliation = author.find(".//AffiliationInfo/Affiliation")
                if affiliation is not None:
                    affiliations.append(affiliation.text)
                    if "email" in affiliation.text.lower():
                        corresponding_email = affiliation.text

            # Filter non-academic authors
            pharma_affiliations = [aff for aff in affiliations if any(keyword in aff for keyword in AFFILIATION_KEYWORDS)]
            if pharma_affiliations:
                results.append((pmid, title, pub_date, ", ".join(authors), ", ".join(pharma_affiliations), corresponding_email))

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper details: {e}")
        sys.exit(1)


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


