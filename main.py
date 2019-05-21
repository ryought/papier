#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import shutil

# 3rd party
from iterfzf import iterfzf
import editor

# package
from doi import doi2apacite, doi2bibtex, fuzzy2doi
from config import load_config
from db import DB

def fn_add(db, config, doi, filename):
    doi = fuzzy2doi(doi)
    # add entry
    if doi in db.db:
        print('Error: The article is already registered.')
    else:
        db.add(doi)
        # move file and rename it
        store_filename = os.path.expanduser(config['dbDir']) + config['renameStyle'].format(**db.get_info(doi))
        input_filename = os.path.abspath(os.path.expanduser(filename))
        if not os.path.isfile(input_filename):
            print('Error: Cannot read the given document')
            return
        if os.path.isfile(store_filename):
            print('Error: There is the same name document, so skip file registering.')
            return

        if not os.path.isdir(os.path.split(store_filename)[0]):
            os.makedirs(os.path.split(store_filename)[0])

        # copy file
        shutil.copyfile(input_filename, store_filename)
        print('Info: copied', input_filename, 'to', store_filename)
        # add new file to database
        db.add_file(doi, store_filename)

        db.dump()

def fn_search(db, config):
    # show all text
    article_list = [(config['listStyle']+' {doi}').format(**db.get_info(doi)) for doi in db.db.keys()]
    ret = iterfzf(article_list, multi=False, encoding='utf-8')
    if ret:
        doi = ret.split()[-1]
        print(doi)
        # show info of selected doi
        fn_info(db, config, doi)

def fn_open(db, config, doi):
    entry = db.get(doi)
    files = entry['filename']
    for f in files:
        if os.path.isfile(f):
            # TODO this will works only on macos
            ret = subprocess.call('open {}'.format(f), shell=True)
        else:
            print(f, 'does not exist')

def fn_info(db, config, doi):
    import pprint
    print('doi: {}'.format(doi))
    pprint.pprint(db.get_info(doi))
    print('note: {}'.format(db.get_note(doi)))

def fn_note(db, config, doi):
    text = db.get_note(doi)
    new_text = editor.edit(contents=text).decode('utf-8')
    db.set_note(doi, new_text)
    db.dump()

def fn_cite(db, config, doi):
    print(doi2apacite(doi))

def fn_bibtex(db, config, doi):
    print(doi2bibtex(doi))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='paper Description')
    subparsers = parser.add_subparsers(dest="subcommand")

    parser_add = subparsers.add_parser('add', help='see add -h')
    parser_add.add_argument('doi', type=str, help='')
    parser_add.add_argument('filename', type=str, help='')
    parser_add.add_argument('--category', type=str, help='')
    parser_add.add_argument('--note', type=str, help='')
    parser_add.set_defaults(fn=fn_add)

    parser_search = subparsers.add_parser('search')
    parser_search.add_argument('tag', help='optional argument')
    parser_search.add_argument('-a', '--author', dest='hoge', help='optional argument')
    parser_search.add_argument('-p', '--publisher', dest='hoge', help='optional argument')
    parser_search.add_argument('-t', '--title', dest='hoge', help='optional argument')
    parser_search.add_argument('-y', '--year', dest='hoge', help='optional argument')
    parser_search.set_defaults(fn=fn_search)

    parser_open = subparsers.add_parser('open')
    parser_open.add_argument('doi', type=str, help='')
    parser_open.set_defaults(fn=fn_open)

    parser_info = subparsers.add_parser('info')
    parser_info.add_argument('doi', type=str, help='')
    parser_info.add_argument('--cite', action='store_true', help='optional argument')
    parser_info.add_argument('--note', action='store_true', help='optional argument')
    parser_info.add_argument('--bibtex', action='store_true', help='optional argument')
    parser_info.set_defaults(fn=fn_info)

    config = load_config()

    db = DB(config['dbDir'])

    args = parser.parse_args()
    if not hasattr(args, 'fn'):
        fn_search(db, config)
    elif args.fn == fn_add:
        fn_add(db, config, args.doi, args.filename)
    elif args.fn == fn_search:
        fn_search(db, config)
    elif args.fn == fn_open:
        fn_open(db, config, args.doi)
    elif args.fn == fn_info:
        if args.cite:
            # show citation
            fn_cite(db, config, args.doi)
        elif args.bibtex:
            fn_bibtex(db, config, args.doi)
        elif args.note:
            # note
            fn_note(db, config, args.doi)
        else:
            fn_info(db, config, args.doi)

if __name__ == '__main__':
    main()
