#!/bin/bash

cd ../docs/
sphinx-apidoc -o source/ ../src/cpl_core
make clean
make html;