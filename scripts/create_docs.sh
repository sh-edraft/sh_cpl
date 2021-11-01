#!/bin/bash

cd ../docs/
sphinx-apidoc -o source/ ../src/cpl_core
sphinx-apidoc -o source/ ../src/cpl_query
make clean
make html;
rm source/cpl_query.tests.rst