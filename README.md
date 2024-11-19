Generate COA form for NSF proposals
===================================

Problem
-------
NSF proposals require a collaborators and other
affiliations (COA) form for each senior personnel.
Table 4 of the COA form requires listing all
co-authors and collaborators from the past 48
months. The general understanding is that every single
author of a paper should be listed in the COA form
without discretion. This is a tedious and error-prone
task, especially for large collaborations.

Solution
--------
This Python package implements an automated author
extractor from PubMed entries. One or more PubMed IDs
can be provided, and the package returns a table
which can be saved as an xlsx file. The table
has the same header as the official template and uses
the same format and conventions.

Installation
------------
The package can be installed locally as:

```bash
pip install .
```

Usage
-----
The package can be used as:

```bash
python -m nsf_coa.coa 32365103 34664389 34860157
```
which dumps `coa.xlsx` in the current directory.

Web application
---------------
There is also a simple web application that can be
used to generate the COA form. It can be run
locally as:

```bash
python -m nsf_coa.app
```

Then go to `http://localhost:5000` in a web browser
and enter PMIDs into the text box.