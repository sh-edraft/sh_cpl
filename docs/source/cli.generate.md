# cpl generate

## Contents

- [Description](#description)
- [Arguments](#arguments)
- [Schematics](#schematics)

Generate a file based on schematic.

cpl **generate** *&lt;schematic&gt;* *&lt;name&gt;* <br>
cpl **g** *&lt;schematic&gt;* *&lt;name&gt;* <br>
cpl **G** *&lt;schematic&gt;* *&lt;name&gt;*

## Description

Generates files based on a schematic.

## Arguments

| Argument          | Description                       | Value type    |
| ----------------- |:---------------------------------:|:-------------:|
| ```<schematic>``` | The schematic to generate.        | ```str```     |
| ```<name>```      | The name of the generated file.   | ```str```     |

## Schematics

| Schematic         | Description         | Arguments      |
| ----------------- |:-------------------:|:----------------:|
| ```abc```         | Abstract base class | ```<name>```
| ```class```       | Class               | ```<name>```
| ```enum```        | Enum class          | ```<name>```
| ```service```     | Service class       | ```<name>```
| ```settings```    | [Configmodel](cpl.configuration) | ```<name>```
| ```thread```      | Thread class        | ```<name>```
