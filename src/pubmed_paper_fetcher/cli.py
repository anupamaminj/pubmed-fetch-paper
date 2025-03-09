import argparse
from pydoc import pager
from pubmed_paper_fetcher.fetchpaper import fetch_pubmed_papers, fetch_paper_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with pharma/biotech affiliations.")
    parser.add_argument("query", type=str, help="PubMed search query (supports full syntax)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename (default: console output)")
    args = parser.parse_args()

    article_ids = fetch_pubmed_papers(args.query, debug=args.debug)
    results = fetch_paper_details(article_ids, debug=args.debug)

    if args.file:
        save_to_csv(results, args.file)
    else:
        print("\nResults:")
        for row in results:   
            print(row)

if __name__ == "__main__":
    main()
