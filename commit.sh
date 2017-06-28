#!/bin/bash
text="next commit"
# ...
if [[ $1 != '' ]]; then
    text=$1
fi
# ...
git add -A && git commit -a -m "$text" && git push -u origin master
