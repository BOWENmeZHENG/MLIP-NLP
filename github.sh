#!/bin/sh

# ./github.sh to push to GitHub
git status
git commit -a -m "ner scratch over"
git push -u origin main
