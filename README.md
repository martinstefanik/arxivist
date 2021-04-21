# Arxivist

A simple command line tool for downloading papers from [arXiv](https://arxiv.org) and naming them with a chosen naming convention. The naming convention is currently fixed to be: '{title} - {family name of author 1}, {family name of author 2} ({year of publication}).pdf'.

# Installation

The tool can be installed manually using `pip` by downloading/cloning the repo and by running

```bash
pip install --user .
```

inside the directory. The directory can be removed after the installation is complete.

Alternatively, if `git` is installed on the system, `arxivist` can also be installed by running

```bash
pip install --user git+https://github.com/martinstefanik/arxivist
```

In order to remove `arxivist`, simply run

```bash
pip uninstall arxivist
```

# Usage

Details about the usage of the tool can be obtained by running `arxivist --help`.

Examples of a call are given by

```bash
arxivist --dir ~/Downloads 2102.00021
arxivist --dir ~/Downloads https://arxiv.org/pdf/2102.00021.pdf
```

Both of these calls download a paper with arXiv ID of 2102.00021 to ~/Downloads and name it Security in Quantum Cryptography - Portmann, Renner (2021).pdf.
