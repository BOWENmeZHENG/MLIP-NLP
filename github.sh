#!/bin/sh

# ./github.sh to push to GitHub
git status
git commit -a -m "train ner"
git push -u origin main
