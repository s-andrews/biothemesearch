# Biological Research Theme Search

This is the code for a web tool which uses text mining of publications to assemble a set of keywords to define the research interests of different groups, and then provides a search engine to explore these.

## Installation

You should be able to check out the codebase here and set the ```www``` directory as a document root.  The ```cgi-bin``` directory will need script execute permissions.

You will need a recent version of python (>3.7), and the whoosh package installed.


## Data Preparation
To generate the search index and group specific keywords you need to follow a few steps.

### Mugshot Installation
The names of group leaders are defined based on the names on the mugshot images in ```www/images/people```.  Make sure each group leader has an image file in that directory named with their display name.

### Index Creation
The search index is created from a CSV file of the publications to use.  This was dumped from our website database and you can see and example file in the ```docs``` folder.

To process this you need to use the ```create_index_from_csv.py``` script which is in the ```scripts``` directory.  Move into the scripts directory and run the ```create_index_from_csv.py``` script, passing the location of the CSV file as the only argument.  This will create an index in the ```index``` folder.

### Key Term Extraction
Once the index is created you can run the ```main_themes.py``` script to generate group leader specific search terms.  These will be summarised in the ```docs/key_terms.txt``` file.

Once this preparation is complete the tool should be functional.

