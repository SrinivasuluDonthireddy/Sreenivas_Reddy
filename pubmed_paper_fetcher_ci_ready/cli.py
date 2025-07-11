import argparse
import pandas as pd
from pubmed_client import get_pubmed_results

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.debug:
        print(f"Query: {args.query}")

    try:
        data = get_pubmed_results(args.query)
        df = pd.DataFrame(data)

        if args.file:
            df.to_csv(args.file, index=False)
            print(f"Results saved to {args.file}")
        else:
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
