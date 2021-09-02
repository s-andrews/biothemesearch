#!/usr/bin/env python3
from pathlib import Path
from whoosh import index
from whoosh.qparser import QueryParser

def main():
    index_folder = Path("../index/")

    leaders = list_group_leaders()

    ix = index.open_dir(index_folder)

    qp = QueryParser("person",schema=ix.schema)

    with open("key_terms.txt","w", encoding="utf-8") as kt:

        for leader in leaders:
            print("Searching for",leader)
            query = qp.parse(leader)

            with ix.searcher() as searcher:
                results = searcher.search(query, limit=None)
                key_terms = {}

                for term in results.key_terms("title",docs=20, numterms=20):
                    if term[0] in key_terms and key_terms[term[0]] > term[1]:
                        continue
                    key_terms[term[0]] = term[1]

                try:
                    for term in results.key_terms("abstract",docs=20, numterms=20):
                        if term[0] in key_terms and key_terms[term[0]] > term[1]:
                            continue
                        key_terms[term[0]] = term[1]
                except ValueError:
                    print("Problem with getting terms from abstract")

                key_terms = {k: v for k, v in sorted(key_terms.items(), reverse=True, key=lambda item: item[1])}

                for i,term in enumerate(key_terms.keys()):
                    if i == 20:
                        break

                    print("\t".join([str(x) for x in [leader,i+1,round(key_terms[term],2),term]]), file=kt)

                print("",file=kt)



def list_group_leaders():
    # We do this based on the names on the mugshot files
    mugshot_dir = Path("../www/images/people/")

    people = []

    for file in mugshot_dir.iterdir():
        name = file.stem        
        people.append(name)

    return people


if __name__ == "__main__":
    main()