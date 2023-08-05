#! /bin/bash
MYPWD=$(cd $(dirname $0)/../; pwd)
cd ${MYPWD}
rm -r docs
pip3 install --upgrade sphinx
pip3 install sphinxcontrib-apidoc
pip3 install sphinx-rtd-theme
sphinx-apidoc -f -o pages/api src tests
sphinx-build -b html pages pages/_build/html
mv pages/_build/html/ docs/
touch docs/.nojekyll
