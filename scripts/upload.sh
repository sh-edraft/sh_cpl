#!/bin/bash

if [ $1 == "-prod" ]; then
  twine upload -r pip.sh-edraft.de dist/cpl-cli/publish/setup/*
  twine upload -r pip.sh-edraft.de dist/cpl-core/publish/setup/*
  twine upload -r pip.sh-edraft.de dist/cpl-query/publish/setup/*
elif [ $1 == "-exp" ]; then
  twine upload -r pip-exp.sh-edraft.de dist/cpl-cli/publish/setup/*
  twine upload -r pip-exp.sh-edraft.de dist/cpl-core/publish/setup/*
  twine upload -r pip-.sh-edraft.de dist/cpl-query/publish/setup/*

else
  twine upload -r pip-dev.sh-edraft.de dist/cpl-cli/publish/setup/*
  twine upload -r pip-dev.sh-edraft.de dist/cpl-core/publish/setup/*
  twine upload -r pip-dev.sh-edraft.de dist/cpl-query/publish/setup/*
fi
