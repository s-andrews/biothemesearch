#!/usr/bin/env python3
import json
import sys
from pathlib import Path
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