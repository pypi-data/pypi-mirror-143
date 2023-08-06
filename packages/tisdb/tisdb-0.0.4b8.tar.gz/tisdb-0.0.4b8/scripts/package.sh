#! /bin/bash
MYPWD=$(cd $(dirname $0)/../; pwd)
rm ${MYPWD}/dist/*
cd ${MYPWD}
pip3 install --upgrade twine
python3 -m pip install --upgrade setuptools wheel twine
python3 setup.py sdist 
twine upload dist/* --verbose

