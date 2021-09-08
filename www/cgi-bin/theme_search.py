#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from whoosh import index
from whoosh.qparser import MultifieldParser

import cgi
import cgitb
cgitb.enable()

def main():

    # Find the action and dispatch to the correct function
    form = cgi.FieldStorage()

    if not "action" in form:
        raise ValueError("No action")

    action = form["action"].value

    dispatch_action(action,form)


def dispatch_action(action,form):

    if action == "mugshots":
        list_group_leaders()
    
    elif action == "keyterms":
        list_key_terms()

    elif action == "descriptions":
        list_descriptions()

    elif action == "search":
        run_search(form["term"].value)



def run_search(term):
    index_folder = Path(__file__).parent.parent.parent / "index"
    ix = index.open_dir(index_folder)

    qp = MultifieldParser(["title","abstract"],schema=ix.schema)

    query = qp.parse(term)

    with ix.searcher() as searcher:
        results = searcher.search(query, limit=None)

        json_data = {}
        for result in results:

            if not result["person"] in json_data:
                json_data[result["person"]] = []

            snippets = result.highlights("title").split("...")
            snippets.extend(result.highlights("abstract").split("..."))

            snippets = [x for x in snippets if x]

            json_data[result["person"]].append({
                "title":result["title"],
                "snippets":snippets,
                "pmid":result["pmid"]
            })

    send_json(json_data)


def list_key_terms():
    # Get the list of key terms
    key_terms_file = Path(__file__).parent.parent.parent / "docs/key_terms.txt"

    key_terms = {}

    with open(key_terms_file) as kf:
        for line in kf:
            if not line.strip():
                continue

            sections = line.strip().split("\t")
            person = sections[0]
            person = person.replace(" ","_")
            person = person.replace("'","")
            person = person.lower()
            term = sections[3]

            if not term in key_terms:
                key_terms[term] = [person]
            else:
                key_terms[term].append(person)

    send_json(key_terms)

def list_descriptions():
    # Get the list of descriptions
    descriptions_file = Path(__file__).parent.parent.parent / "docs/person_descriptions.json"

    with open(descriptions_file) as df:
        raw_descriptions = json.load(df)

        # We need to change the names to be the short versions
        fixed_descriptions = {}

        for name,description in raw_descriptions.items():
            name = name.strip().lower()
            name = name.replace(" ","_")
            name = name.replace("'","")

            fixed_descriptions[name] = description

        send_json(fixed_descriptions)

def list_group_leaders():
    # Get a list of the group leaders from the set of
    # mugshots and return it
    mugshot_dir = Path(__file__).parent.parent / "images/people"

    people = []

    for image in mugshot_dir.iterdir():
        file = str(image)
        file = file[file.index("www")+3:].replace("\\","/")
        name = image.stem
        people.append({"name":name, "url":file})
    
    send_json(people)


def send_json(data):
    print("Content-type: text/json\n")
    print(json.dumps(data))

def send_error(message):
    print("Status: 500 Internal Server Error")
    print("Content-Type: text/plain\n")
    print(message, end="")
    sys.exit(0)

def send_success(message):
    print("Content-Type: text/plain\n")
    print(message, end="")
    sys.exit(0)

if __name__ == "__main__":
    main()