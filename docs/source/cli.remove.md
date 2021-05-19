# cpl remove

## Contents

- [Description](#description)
- [Arguments](#arguments)

Removes a project from workspace.

cpl **remove** *&lt;project&gt;* <br>
cpl **r** *&lt;project&gt;* <br>
cpl **R** *&lt;project&gt;*

## Description

The command can be used to publish a project of type "console" or "library".

The publish command builds the source files and then creates an ```setup.py``` with data from ```cpl.json```.
The command executes the ```setup.py``` and removes all source files with the ```setup.py``` from the 'publish/' directory.

Generated files of ```setup.py``` are in the 'publish/setup/' directory.

## Arguments

| Argument                  | Description                           | Value type      |
| ------------------------- |:-------------------------------------:|:----------------:|
| ```<project>```           | The name of the project to delete     | ```str```
