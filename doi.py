#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import json
import re

def doi2bibtex(doi):
    url = 'https://doi.org/' + doi
    headers = {
        'Accept': 'application/x-bibtex; charset=utf-8'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        bibtex = res.read().decode('utf-8')
    return bibtex

def doi2apacite(doi):
    url = 'https://doi.org/' + doi
    headers = {
        'Accept': 'text/x-bibliography; style=apa; charset=utf-8'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        citation = res.read().decode('utf-8')
    return citation

def doi2json(doi):
    url = 'https://doi.org/' + doi
    headers = {
        'Accept': 'application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
    return data

def fuzzy2doi(fuzzy_doi):
    if 'doi.org/' in fuzzy_doi:
        return re.match(r'.*doi.org/(.+)', fuzzy_doi).group(1)
    else:
        return fuzzy_doi

def get_doi_for_filename(doi):
    return re.sub(r'[\\|/|:|?|.|"|<|>|\|\*|]', '_', doi)

if __name__ == '__main__':
    doi = '10.1038/nature12593'
    # bibtex = doi2bibtex(doi)
    # print(bibtex)

    # print(doi2apacite(doi))
    # print(doi2json(doi))

    print(fuzzy2doi(doi))
    print(fuzzy2doi('https://doi.org/10.1186/s12864-018-4551-y'))
    print(get_doi_for_filename('https://doi.org/10.1186/s12864-018-4551-y'))

