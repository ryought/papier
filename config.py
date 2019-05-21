#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import os

default_config = {
        'dbDir': '~/papier_tmp/',  # 保管場所
        'renameStyle': '{category}/{author_short}_{year}_{title_short}_{doi_for_filename}.pdf',  # pdfの保管のファイル名のスタイル
        'listStyle': '{title} | {year} | {publisher} | {author} | {doi}'  # fzfで表示する時のスタイル
}

def load_config():
    with open(os.path.expanduser('~/.papierrc'), 'r') as f:
        yaml_config = yaml.load(f)
    config = {}
    for key in default_config.keys():
        if key in yaml_config:
            config[key] = yaml_config[key]
        else:
            config[key] = default_config[key]
    return config

if __name__ == '__main__':
    print(load_config())
