import requests
from typing import List, Dict
from xml.etree import ElementTree as ET
import re

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def is_non_academic_affiliation(affiliation: str) -> bool:
    academic_keywords = [
        "university", "college", "school", "institute", "hospital", "center",
        "centre", "department", "faculty", "clinic", "nhs", "children's", "laboratory"
    ]
    return not any(kw in affiliation.lower() for kw in academic_keywords)

def extract_authors_info(article: ET.Element) -> List[Dict[str, str]]:
    authors_info = []
    for author in article.findall(".//Author"):
        name_parts = []
        lastname = author.findtext("LastName")
        forename = author.findtext("ForeName")
        if lastname: name_parts.append(lastname)
        if forename: name_parts.append(forename)
        fullname = " ".join(name_parts)

        affil_info = author.find("AffiliationInfo")
        affiliation = affil_info.findtext("Affiliation") if affil_info is not None else ""

        email_match = re.search(r'[\w\.-]+@[\w\.-]+', affiliation)
        email = email_match.group(0) if email_match else ""

        if is_non_academic_affiliation(affiliation):
            authors_info.append({
                "name": fullname,
                "affiliation": affiliation,
                "email": email
            })

    return authors_info

def search_pubmed(query: str, retmax: int = 20) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(ESEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_articles(pubmed_ids: List[str]) -> List[Dict[str, str]]:
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(EFETCH_URL, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.text)

    articles_data = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date_elem = article.find(".//PubDate")
        if pub_date_elem is not None:
            year = pub_date_elem.findtext("Year")
            month = pub_date_elem.findtext("Month") or "01"
            day = pub_date_elem.findtext("Day") or "01"
            pub_date = f"{year}-{month}-{day}"
        else:
            pub_date = ""

        non_academic_authors = extract_authors_info(article)
        if not non_academic_authors:
            continue

        names = "; ".join([a["name"] for a in non_academic_authors])
        affiliations = "; ".join([a["affiliation"] for a in non_academic_authors])
        emails = "; ".join(filter(None, [a["email"] for a in non_academic_authors]))

        articles_data.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": names,
            "Company Affiliation(s)": affiliations,
            "Corresponding Author Email": emails
        })

    return articles_data

def get_pubmed_results(query: str, retmax: int = 20) -> List[Dict[str, str]]:
    ids = search_pubmed(query, retmax)
    return fetch_articles(ids)
