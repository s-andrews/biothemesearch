import csv
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from pathlib import Path
import xml.etree.ElementTree as ET

def main():
    csv_file = Path("../docs/content_export_publication_pubmed_1629963492.csv")
    index_folder = Path("../index/")

    if not index_folder.exists():
        index_folder.mkdir()

    group_leaders = list_group_leaders()

    create_index(csv_file,index_folder, group_leaders)

def list_group_leaders():
    # We do this based on the names on the mugshot files
    mugshot_dir = Path("../www/images/people/")

    people = {}

    for file in mugshot_dir.iterdir():
        name = file.stem
        surname = name.split(" ")[-1]
        short_name = surname+" "+name[0]
        if short_name in people:
            print ("Duplicate short name "+short_name)
        
        print(name,"is",short_name)
        
        people[short_name] = name

    return people


def create_index(csv_file, indexd, people):
    schema = Schema(
            person=TEXT(stored=True),
            title=TEXT(stored=True),
            pmid=ID(stored=True),
            abstract=TEXT(analyzer=StemmingAnalyzer(), stored=True)
            )

    index.create_in(indexd,schema)

    ix = index.open_dir(indexd)
    writer = ix.writer()

    with open(csv_file, newline='', encoding="UTF-8") as csvfh:
        docreader = csv.reader(csvfh)
        for row in docreader:
            title = row[7]
            abstract = row[9]
            if abstract == "n/a":
                continue
            authors = row[10]
            pmid = row[15]

            # Find which group leaders are likley on this paper
            for short_name in people.keys():
                if short_name in authors:
                    writer.add_document(pmid=pmid,person=people[short_name],title=title,abstract=abstract)

    writer.commit()



if __name__ == "__main__":
    main()