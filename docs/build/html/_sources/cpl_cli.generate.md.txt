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

You can define custom schematics by creating templates in a ```.cpl``` folder.

## Arguments

| Argument          |                                                                             Description                                                                             | Value type    |
|-------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-------------:|
| ```<schematic>``` |                                                                     The schematic to generate.                                                                      | ```str```     |
| ```<name>```      |                                                                   The name of the generated file.                                                                   | ```str```     |
| ```--base```      | First element of path will be used as base-path not 'src'. For example: 'cpl g c test/Test' will be created at ```src/test/``` with --base it would be ```test/```  | ```str```     |

## Schematics

| Schematic       |              Description               |  Arguments   |
|-----------------|:--------------------------------------:|:------------:|
| ```abc```       |          Abstract base class           | ```<name>``` |
| ```class```     |                 Class                  | ```<name>``` |
| ```enum```      |               Enum class               | ```<name>``` |
| ```pipe```      |               Pipe class               | ```<name>``` |
| ```service```   |             Service class              | ```<name>``` |
| ```settings```  | [Configmodel](cpl_core.configuration)  | ```<name>``` |
| ```test```      |               Test class               | ```<name>``` |
| ```thread```    |              Thread class              | ```<name>``` |
| ```validator``` |            Validator class             | ```<name>``` |
| ```command```   |       Discord bot command class        | ```<name>``` |
| ```event```     |        Discord bot event class         | ```<name>``` |
