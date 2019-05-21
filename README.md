## install
`pip install -e .`


## usage

```
add new entry:
$ papier add <doi> hoge.pdf
$ papier add <doi> hoge.pdf --category Hi-C --note 'my first paper' 

add another document:
$ papier add <doi> hoge.pdf --append

view infos:
$ papier info
-> select doi in fzf
$ papier info <doi>
$ papier info -c <category-name>
-> only show entrys in given category
or you can omit 'info'
$ papier
$ papier -c <category-name>

get citation or bibtex
$ papier info --cite <doi>
$ papier info --bibtex <doi>

edit note
$ papier edit --note
-> select doi in fzf
$ papier edit <doi> --note
-> then launch $EDITOR

edit category
$ papier edit --category <new-category>
$ papier edit <doi> --category <new-category>

open pdf
$ papier open 
$ papier open <doi>

search # TODO
$ papier search --author 'fuga'

```
