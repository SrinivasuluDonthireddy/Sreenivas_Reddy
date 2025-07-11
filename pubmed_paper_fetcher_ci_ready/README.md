
# PubMed Paper Fetcher

A CLI tool to query PubMed for papers with non-academic authors affiliated with pharmaceutical or biotech companies.

## Features

- Search PubMed using full query syntax
- Detect non-academic authors using affiliation heuristics
- Export results as CSV

## Setup

```bash
git clone <your-repo-url>
cd pubmed-paper-fetcher
poetry install
```

## Usage

```bash
poetry run get-papers-list "cancer AND drug discovery" -f results.csv
```

Optional flags:
- `-d` / `--debug`: Show debug info
- `-f` / `--file`: Output CSV filename

## Dependencies

- Python 3.9+
- requests
- pandas

## Notes

Built with help from ChatGPT. Feel free to extend heuristics for better author filtering.
