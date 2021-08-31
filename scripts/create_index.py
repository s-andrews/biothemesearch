from whoosh import index
from whoosh.fields import Schema, TEXT
from whoosh.analysis import StemmingAnalyzer
from pathlib import Path
import xml.etree.ElementTree as ET

def main():
    doc_folder = Path("../docs/")
    index_folder = Path("../index/")

    if not index_folder.exists():
        index_folder.mkdir()

    create_index(doc_folder,index_folder)


def create_index(docs, indexd):

    schema = Schema(
            person=TEXT(stored=True),
            title=TEXT(stored=True),
            abstract=TEXT(analyzer=StemmingAnalyzer(), stored=True)
            )

    index.create_in(indexd,schema)

    ix = index.open_dir(indexd)
    writer = ix.writer()

    doclist = docs.iterdir()

    for doc in doclist:
        docdata = parse_doc(doc)


def parse_doc(file):
    print(file)
    tree = ET.parse(file)
    root = tree.getroot().find("PubmedArticle").find("MedlineCitation")

    article = root.find("Article")
    title = article.find("ArticleTitle").text
    print(title)

    abstract = article.find("Abstract").find("AbstractText").text
    print(abstract)



if __name__ == "__main__":
    main()