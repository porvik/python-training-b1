#!/bin/bash

cd $( dirname "${BASH_SOURCE[0]}" )

if [[ ! -f version ]]; then echo "0" > version; fi
old_version=$(cat version)
new_version=$((old_version+1))
echo "${new_version}" > version
sed -Ei "s/^version = .*/version = 0.0.${new_version}/" setup.cfg

rm -rf src
cp -r ../module_1/src src

# python3 -m venv env
# source env/bin/activate
pip install -U setuptools build
python -m build .
# rm -rf env