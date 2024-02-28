#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'a jupyter notebook .ipynb file should be provided.'
    exit 0
fi

echo $1
jupyter nbconvert $1 --to html --output-dir='./dist'
