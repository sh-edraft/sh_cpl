# CLI Overview and Command Reference

## Table of Contents

1. [Install CPL](setup#install-the-package)
2. [Install CPL CLI](setup#install-the-cli)
3. [Basic workflow](#basic-workflow)
4. [CLI command-language syntax](#cli-command-language-syntax)
5. [Command overview](#command-overview)

## Basic workflow

To create, build, and serve a new, basic CPL project on a development server, go to the parent directory of your new workspace use the following commands:

```sh
cpl new console my-first-project
cd my-first-project
cpl start
```

In the terminal you will the output of the app.

## CLI command-language syntax

```cpl``` commandNameOrAlias requiredArg ```[optionalsArgs]```

- Most commands, and some options, have aliases. Aliases are shown in the syntax statement for each command.
- Arguments are not prefixed.

### Relative paths

Options that specify files can be given as absolute paths, or as paths relative to the current working directory, which is generally either the workspace or project root.

### Schematics

The cpl generate command takes as an argument the artifact to be generated.  In addition to any general options, each artifact defines its own options in a schematic. Schematic options are supplied to the command in the same format as immediate command options.

## Command overview

| Command                       | Alias         | Description      |
| ----------------------------- |:-------------:|:----------------:|
| [add](cpl_cli.add)               | a or a        | Adds a project reference to given project.
| [build](cpl_cli.build)            | b or B        | Prepares files for publish into an output directory named dist/ at the given output path. Must be executed from within a workspace directory.
| [generate](cpl_cli.generate)      | g or G        | Generate a new file.
| [help](cpl_cli.help)              | h or H        | Lists available command and their short descriptions.
| [install](cpl_cli.install)        | i or I        | With argument installs packages to project, without argument installs project dependencies.
| [new](cpl_cli.new)                | n or N        | Creates new CPL project.
| [publish](cpl_cli.publish)        | p or P        | Prepares files for publish into an output directory named dist/ at the given output path and executes ```setup.py```. Must be executed from within a library workspace directory.
| [remove](cpl_cli.remove)          | r or R        | Removes a project from workspace.
| [start](cpl_cli.start)            | s or S        | Starts CPL project, restarting on file changes.
| [uninstall](cpl_cli.uninstall)    | ui or UI      | Uninstalls packages from project.
| [update](cpl_cli.update)          | u or U        | Update CPL and project dependencies.
| [version](cpl_cli.version)        | v or V        | Outputs CPL CLI version.
