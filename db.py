import json
from doi import doi2json, get_doi_for_filename
import os

class DB:
    def __init__(self, dbpath):
        """
        self.db : database
        each entry is formatted as below.
        doi: {
            json: {}, # retrieved from doi
            filename: ['~.pdf', '~~.pdf'],
            note: ''
        }
        """
        self.db = {}
        self.path = os.path.expanduser(dbpath)
        self.load()

    def __repr__(self):
        return "{}".format(list(self.db.keys()))

    def load(self):
        if os.path.isfile(self.path + 'db.json'):
            with open(self.path + 'db.json', 'r') as f:
                self.db = json.load(f)

    def dump(self):
        with open(self.path + 'db.json', 'w') as f:
            json.dump(self.db, f, indent=4)

    def add(self, doi):
        entry = {
                'info': doi2json(doi),
                'filename': [],
                'category': 'inbox',
                'note': ''
        }
        self.db[doi] = entry

    def add_file(self, doi, filename):
        self.db[doi]['filename'].append(filename)

    def remove(self, doi):
        del self.db[doi]

    def get(self, doi):
        return self.db[doi]

    def get_note(self, doi):
        return self.db[doi]['note']
    def set_note(self, doi, note):
        self.db[doi]['note'] = note

    def get_info(self, doi):
        entry = self.db[doi]
        return {
                'title': entry['info']['title'],
                'author': get_author_text(entry),
                'author_short': get_author_short(entry),
                'year': get_issued_year(entry),
                'publisher': get_publisher(entry),
                'category': entry['category'],
                'doi': doi,
                'doi_for_filename': get_doi_for_filename(doi)
                }

# functions for entry
def get_author_short(entry):
    authors = entry['info']['author']
    if 'family' in authors[0]:
        return authors[0]['family']
    elif 'name' in authors[0]:
        return authors[0]['name']
    else:
        raise KeyError('no authors')

def get_author_text(entry):
    authors = entry['info']['author']
    def get_name_string(author):
        if 'given' in author and 'family' in author:
            return author['given'] + ' ' + author['family']
        elif 'name' in author:
            return author['name']
        else:
            return 'error'
    return ', '.join([get_name_string(author) for author in authors])

def get_issued_year(entry):
    try:
        return entry['info']['issued']['date-parts'][0][0]
    except KeyError:
        return 'unknown'

def get_publisher(entry):
    try:
        return entry['info']['container-title']
    except KeyError:
        return 'unknown'

if __name__ == '__main__':
    doi = '10.1038/nature12593'
    db = DB('/Users/ryought/papier_tmp/')
    db.add(doi, 'hoge.pdf')
    entry = db.get(doi)
    print(entry['info']['title'])
    print(entry['info']['author'])

    db.dump()
