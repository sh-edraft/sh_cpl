.. Common Python Library documentation master file, created by
   sphinx-quickstart on Wed Apr 14 10:25:36 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction to the CPL Docs
============================

The Common Python Library (CPL) is a package for python and a development platform meant to help you create simple and efficient server and desktop applications.

This CPL docs help you learn, understand and use the package. From your first application to complex apps for enterprises.


Features
--------
- cpl-core
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
- cpl-cli
   - Expandle
   - Code generation
   - Package managing
   - Build & Publishing
- cpl-discord
   - Utils for discord.py
   - Connector between cpl-core and discord.py
   - Prepared services for dependency injection
- cpl-query
   - Python list extensions
   - Functions for sorting and filtering
   - Like linq from C# but in python xD
- cpl-translate
   - Generic translations
   - Prepared translation service and translate pipe
   - Get translation from JSON files key dot.key notation

Manuals
---------

These pages go into great detail about everything the Library can do.

.. toctree::
   :maxdepth: 1

   introduction
   getting_started
   contributing
   cpl_cli
   cpl_core
   cpl_query
