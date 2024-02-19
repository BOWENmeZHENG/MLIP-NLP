#!/bin/sh

# ./github.sh to push to GitHub
git status
git commit -a -m "add llm"
git push -u origin main