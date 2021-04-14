#!/bin/bash

cd ../docs/
sphinx-apidoc -o source/ ../src/cpl
make clean
make html;