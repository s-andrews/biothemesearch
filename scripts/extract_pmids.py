#!python
import re
import requests
from pathlib import Path

def main():
    url_text = """
https://www.babraham.ac.uk/our-research/epigenetics/gavin-kelsey
https://www.babraham.ac.uk/our-research/epigenetics/olivia-casanueva
https://www.babraham.ac.uk/our-research/epigenetics/maria-christophorou
https://www.babraham.ac.uk/our-research/epigenetics/jon-houseley
https://www.babraham.ac.uk/our-research/epigenetics/martin-howard
https://www.babraham.ac.uk/our-research/epigenetics/wolf-reik
https://www.babraham.ac.uk/our-research/epigenetics/peter-rugg-gunn
https://www.babraham.ac.uk/our-research/epigenetics/stefan-schoenfelder
https://www.babraham.ac.uk/our-research/immunology/martin-turner
https://www.babraham.ac.uk/our-research/immunology/anne-corcoran
https://www.babraham.ac.uk/our-research/immunology/michelle-linterman
https://www.babraham.ac.uk/our-research/immunology/claudia-ribeiro-de-almeida
https://www.babraham.ac.uk/our-research/immunology/sarah-ross
https://www.babraham.ac.uk/our-research/signalling/simon-cook
https://www.babraham.ac.uk/our-research/signalling/oliver-florey
https://www.babraham.ac.uk/our-research/signalling/phillip-hawkins
https://www.babraham.ac.uk/our-research/signalling/nicholas-ktistakis
https://www.babraham.ac.uk/our-research/signalling/ian-mcgough
https://www.babraham.ac.uk/our-research/signalling/valerie-odonnell
https://www.babraham.ac.uk/our-research/signalling/rahul-samant
https://www.babraham.ac.uk/our-research/signalling/hayley-sharpe    
https://www.babraham.ac.uk/our-research/signalling/len-stephens
https://www.babraham.ac.uk/our-research/signalling/heidi-welch
https://www.babraham.ac.uk/our-research/affiliated-scientists/michael-coleman
https://www.babraham.ac.uk/our-research/affiliated-scientists/myriam-hemberger
https://www.babraham.ac.uk/our-research/affiliated-scientists/patrick-varga-weisz    
"""
    url_list = [x.strip() for x in url_text.split("\n")]

    for url in url_list:
        if not url:
            continue

        process_url(url)


def process_url(url):

    name = url.split("/")[-1]

    html = requests.get(url).content.decode("UTF-8")
    matches = re.finditer("www.ncbi.nlm.nih.gov/pubmed/(\d+)",html)

    for match in matches:
        print(f"{name} {match.group(1)}")
        outfile = Path(f"docs/{name}_{match.group(1)}.txt")
        if outfile.exists():
            continue

        with open(f"docs/{name}_{match.group(1)}.txt","w") as out:
            print(get_pubmed(match.group(1)),file=out)


def get_pubmed(pmid):
    return requests.get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&tool=themesearch&email=simon.andrews@babraham.ac.uk)").content.decode("UTF-8")



if __name__ == "__main__":
    main()