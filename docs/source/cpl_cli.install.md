# cpl install

## Contents

- [Description](#description)
- [Arguments](#arguments)

Installs given package via pip

cpl **install** *&lt;package&gt;* <br>
cpl **i** *&lt;package&gt;* <br>
cpl **I** *&lt;package&gt;*

## Description

Install given package to project via pip.
Without given package it will install the depedencies of the CPL project your in.

## Arguments

| Argument        |      Description       | Value type |
|-----------------|:----------------------:|:----------:|
| ```<package>``` | The package to install | ```str```  |

## Flags

| Argument         |                     Description                      |
|------------------|:----------------------------------------------------:|
| ```--dev```      | Specifies whether the command is in development mode |
| ```--virtual```  |    Specifies whether the command is virtual mode     |
| ```--simulate``` |      Specifies whether the command is simulated      |
