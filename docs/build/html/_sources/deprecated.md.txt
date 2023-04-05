# Deprecated

## Table of Contents

1. [ConfigurationModelABC.from_dict](#ConfigurationModelABC-from_dict-method)

## ConfigurationModelABC from_dict method

We now process the configuration models directly in the configuration by recursive parameter parsing.

The JSONProcessor now goes through the JSON and the arguments of the __init__ and links the attributes by name from the
JSON and the name of the keyword argument.
Now, based on the type, either simply assigns the value. With a ``dict`` the processor is called recursively and so the
JSON is processed further. This way nested ConfigurationModels can be processed.

For this the code must be adapted as follows:

From this:

```sh
class VersionSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self.major: Optional[str] = "0"
        self.minor: Optional[str] = "0"
        self.micro: Optional[str] = "0"

    def from_dict(self, settings: dict):
        self.major = settings["Major"]
        self.minor = settings["Minor"]
        micro = settings["Micro"]
        if micro != '':
            self.micro = micro
```

To this:

```sh
class VersionSettings(ConfigurationModelABC):
    def __init__(self, major: str = None, minor: str = None, micro: str = None):
        ConfigurationModelABC.__init__(self)

        self.major: Optional[str] = major
        self.minor: Optional[str] = minor
        self.micro: Optional[str] = micro if micro != "" else None
```

This makes the [from_dict](#from_dict) function obsolete.

A few rules must be observed:

- Only simple types can be processed
  <br>
  Wrong: ```dict[str, str]```
  <br>
  Correct: ```dict```
  <br>
  <br>
  Incorrect: ```list[str]```
  <br>
  Correct: ```list```

- The arguments must be optional, i.e. created as kwargs
  <br>
  Incorrect: ```def __init__(self, x: int, y: int)```
  <br>
  Correct: ```def __init__(self, x: int = None, y: int = None)```