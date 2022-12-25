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

You can define custom project types by creating templates in a ```.cpl``` folder.

If the command is running in a CPL workspace, it will add the new project to the workspace.

| Argument     |                                                                            Description                                                                             | Value type |
|--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------:|
| ```<type>``` |                                                        The type of the project, see [types](#project-types)                                                        | ```str```  |
| ```<name>``` |                                                                      The name of the project                                                                       | ```str```  |
| ```--base``` | First element of path will be used as base-path not 'src'. For example: 'cpl g c test/Test' will be created at ```src/test/``` with --base it would be ```test/``` | ```str```     |

## Project types

| Project type  |         Description          |
|---------------|:----------------------------:|
| ```console``` | A simple console application |
| ```library``` |          A package           |

## Flags

| Argument                  |                 Description                 |
|---------------------------|:-------------------------------------------:|
| ```--async```             |       Specifies whether async is used       |
| ```--application-base```  | Specifies whether application base is used  |
| ```--startup```           |      Specifies whether startup is used      |
| ```--service-providing``` | Specifies whether service-providing is used |
| ```--nothing```           |      Specifies whether nothing is used      |
| ```--venv```              |       Specifies whether venv is used        |
