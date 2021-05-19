# cpl new

## Contents

- [Description](#description)
- [Arguments](#arguments)
- [Project types](#project-types)

Generates a workspace and initial project or add a project to workspace.

cpl **new** *&lt;type&gt;* *&lt;name&gt;*<br>
cpl **n** *&lt;type&gt;* *&lt;name&gt;* <br>
cpl **N** *&lt;type&gt;* *&lt;name&gt;*

## Description

Generates a workspace and initial project or add a project to workspace.

If the command is running in a CPL workspace, it will add the new project to the workspace.

| Argument          | Description                                           | Value type    |
| ----------------- |:-----------------------------------------------------:|:-------------:|
| ```<type>```      | The type of the project, see [types](#project-types)  | ```str```     |
| ```<name>```      | The name of the project                               | ```str```     |

## Project types

| Project type      | Description                   |
| ----------------- |:-----------------------------:|
| ```console```     | A simple console application  |
| ```library```     | A package                     |
