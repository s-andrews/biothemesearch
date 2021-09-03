#!/usr/bin/env python3
from pathlib import Path
from whoosh import index
from whoosh.qparser import QueryParser, MultifieldParser
import re

def main():
    index_folder = Path("../index/")

    leaders = list_group_leaders()

    ix = index.open_dir(index_folder)

    qp = QueryParser("person",schema=ix.schema)

    with open("../docs/key_terms.txt","w", encoding="utf-8") as kt:

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

                # Get expanded versions of the most important terms
                expanded_terms = expand_key_terms(key_terms, ix)

                # We might have duplicates in the expanded terms so we'll record what 
                # we've used
                used_terms = []

                for term in key_terms.keys():
                    eterm = expanded_terms[term]
                    if eterm.isdigit():
                        continue
                    if eterm in used_terms:
                        continue
                    if len(eterm)<3:
                        continue

                    used_terms.append(eterm)
                    print("\t".join([str(x) for x in [leader,len(used_terms),round(key_terms[term],2),eterm]]), file=kt)

                    if len(used_terms) == 20:
                        break

                print("",file=kt)

def expand_key_terms(short_terms, ix):
    # Some of the key terms are word stems rather than complete
    # words so we want to be able to put actual words in instead
    # Here we'll do a search with each key term and see what comes
    # back.

    expanded_terms = {}

    qp = MultifieldParser(["title","abstract"],schema=ix.schema)

    for short_term in short_terms:
        # We need to add the * because some short terms don't actually
        # produce any hits when entered without a suitable suffix
        query = qp.parse(short_term+"*")

        snippet_hits = {}

        with ix.searcher() as searcher:
            results = searcher.search(query, limit=None)

            for result in results:
                snippets = result.highlights("title").split("...")
                snippets.extend(result.highlights("abstract").split("..."))
                snippets = [x for x in snippets if x]

                for snippet in snippets:
                    hit = re.search(">(.*?)</b>", snippet)
                    if hit is not None:
                        snippet_hit = hit.groups()[0].lower()

                        if not snippet_hit in snippet_hits:
                            snippet_hits[snippet_hit] = 1
                        
                        else:
                            snippet_hits[snippet_hit] += 1

        # Find the most common term for the snippet
        if not snippet_hits:
            breakpoint()

        best_hit = sorted(list(snippet_hits.keys()), key=lambda x: snippet_hits[x], reverse=True)[0]

        expanded_terms[short_term] = best_hit

    return expanded_terms






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