from whoosh import index
from whoosh.fields import Schema, TEXT, ID
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
            pmid=ID(stored=True),
            abstract=TEXT(analyzer=StemmingAnalyzer(), stored=True)
            )

    index.create_in(indexd,schema)

    ix = index.open_dir(indexd)
    writer = ix.writer()

    doclist = docs.iterdir()

    for doc in doclist:
        filename = doc.stem

        name,pmid = filename.split("_")

        name = name.replace("-"," ").title()

        docdata = parse_doc(doc)
        writer.add_document(pmid=pmid,person=name,title=docdata["title"],abstract=docdata["abstract"])


def parse_doc(file):
    tree = ET.parse(file)
    root = tree.getroot().find("PubmedArticle").find("MedlineCitation")

    article = root.find("Article")
    title = article.find("ArticleTitle").text

    abstract_node = article.find("Abstract")
    abstract_text = ""

    if abstract_node is not None:
        abstract_text = abstract_node.find("AbstractText").text

    return {"title": title, "abstract":abstract_text}



if __name__ == "__main__":
    main()