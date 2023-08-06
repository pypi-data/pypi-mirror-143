#! /bin/bash
MYPWD=$(cd $(dirname $0)/../; pwd)
cd ${MYPWD}
pip3 install pytest
pip3 install pytest-xdist
pytest -n 10
