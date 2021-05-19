# cpl add

## Contents

- [Description](#description)
- [Arguments](#arguments)

Removes a project from workspace.

cpl **add** *&lt;source-project&gt;* *&lt;target-project&gt;* <br>
cpl **a** *&lt;source-project&gt;* *&lt;target-project&gt;* <br>
cpl **A** *&lt;source-project&gt;* *&lt;target-project&gt;*

## Description

Adds a project reference to given project.

If you call the command in a CPL workspace, you can use the project names. Otherwise the paths of the projects must be specified.

## Arguments

| Argument                  | Description                                                     | Value type      |
| ------------------------- |:---------------------------------------------------------------:|:----------------:|
| ```<source-project>```    | Name of the project to which the reference has to be added      | ```str```
| ```<target-project>```    | Name of the project to be referenced                            | ```str```
