<h1 align="center">CPL - Common python library</h1>

<!-- Summary -->
<p align="center">
  <!-- <img src="" alt="cpl-logo" width="120px" height="120px"/> -->
  <br>
  <i>
  CPL is a development platform for python server applications
  <br>using Python.</i>
  <br>
</p>

## Table of Contents
<!-- TABLE OF CONTENTS -->
<ol>
   <li><a href="#Features">Features</a></li>
   <li>
     <a href="#getting-started">Getting Started</a>
     <ul>
       <li><a href="#prerequisites">Prerequisites</a></li>
       <li><a href="#installation">Installation</a></li>
     </ul>
   </li>
   <li><a href="#roadmap">Roadmap</a></li>
   <li><a href="#contributing">Contributing</a></li>
   <li><a href="#license">License</a></li>
   <li><a href="#contact">Contact</a></li>
</ol>

## Features
<!-- FEATURE OVERVIEW -->
- Expandle
- Application base
    - Standardized application classes
    - Application object builder
    - Application extension classes
    - Startup classes
    - Startup extension classes
- Configuration
    - Configure via object mapped JSON
    - Console argument handling
- Console class for in and output
    - Banner
    - Spinner
    - Options (menu)
    - Table
    - Write
    - Write_at
    - Write_line
    - Write_line_at
- Dependency injection
    - Service lifetimes: singleton, scoped and transient
- Providing of application environment
    - Environment (development, staging, testing, production)
    - Appname
    - Customer
    - Hostname
    - Runtime directory
    - Working directory
- Logging
    - Standardized logger
    - Log-level (FATAL, ERROR, WARN, INFO, DEBUG & TRACE)
- Mail handling
    - Send mails
- Pipe classes
    - Convert input
- Utils
    - Credential manager
        - Encryption via BASE64
    - PIP wrapper class based on subprocess
        - Run pip commands
    - String converter to different variants
        - to_lower_case
        - to_camel_case
        - ...

<!-- GETTING STARTED -->
## Getting Started

[Get started with CPL][quickstart].

### Prerequisites

- Install [python] which includes [Pip installs packages][pip]

### Installation

Install the CPL package
```sh
pip install cpl --extra-index-url https://pip.sh-edraft.de
```

Install the CPL CLI
```sh
pip install cpl-cli --extra-index-url https://pip.sh-edraft.de
```

Create workspace:
```sh
cpl new <console|library|unittest> <PROJECT NAME>
```

Run the application:
```sh
cd <PROJECT NAME>
cpl start
```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://git.sh-edraft.de/sh-edraft.de/sh_cpl/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

### Contributing Guidelines

Read through our [contributing guidelines][contributing] to learn about our submission process, coding rules and more.

### Want to Help?

Want to file a bug, contribute some code, or improve documentation? Excellent! Read up on our guidelines for [contributing][contributing].



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE] for more information.



<!-- CONTACT -->
## Contact

Sven Heidemann - sven.heidemann@sh-edraft.de

Project link: [https://git.sh-edraft.de/sh-edraft.de/sh_common_py_lib](https://git.sh-edraft.de/sh-edraft.de/sh_cpl)

<!-- External LINKS -->
[pip_url]: https://pip.sh-edraft.de
[python]: https://www.python.org/
[pip]: https://pypi.org/project/pip/

<!-- Internal LINKS -->
[project]: https://git.sh-edraft.de/sh-edraft.de/sh_cpl
[quickstart]: https://git.sh-edraft.de/sh-edraft.de/sh_cpl/wiki/quickstart
[contributing]: https://git.sh-edraft.de/sh-edraft.de/sh_cpl/wiki/contributing
[license]: LICENSE
