#!/usr/bin/env python3
from pathlib import Path
from whoosh import index
from whoosh.qparser import MultifieldParser

def main():
    index_folder = Path("../index/")
    ix = index.open_dir(index_folder)

    qp = MultifieldParser(["title","abstract"],schema=ix.schema)

    while True:
        query_text = input("Query: ")
        if not query_text:
            break

        query = qp.parse(query_text)

        with ix.searcher() as searcher:
            results = searcher.search(query, limit=None)

            print(results)
            for result in results:
                print(result.rank, round(result.score,2), result["person"],result["title"])

                print(result.highlights("title"))
                print(result.highlights("abstract"))
                break


if __name__ == "__main__":
    main()