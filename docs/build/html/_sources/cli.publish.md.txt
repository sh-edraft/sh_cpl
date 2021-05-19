# cpl publish

## Contents

- [Description](#description)
<!-- - [Arguments](#arguments) -->

Prepares files for publish into an output directory named dist/ at the given output path and executes ```setup.py```.

cpl **publish** <br>
cpl **p** <br>
cpl **P**

## Description

The command can be used to publish a project of type "console" or "library".

The publish command builds the source files and then creates an ```setup.py``` with data from ```cpl.json```.
The command executes the ```setup.py``` and removes all source files with the ```setup.py``` from the 'publish/' directory.

Generated files of ```setup.py``` are in the 'publish/setup/' directory.

<!-- ## Arguments

| Argument      | Description   | Value type      |
| ------------- |:-------------:|:----------------:|
| ```<project>```     | The name of the project to build. Can be an console or a library. | ```str``` -->