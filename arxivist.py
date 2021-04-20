#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download a paper from arxiv.org."""

import os
import re
import unicodedata

import arxiv
import click

__version__ = "1.0.0"


@click.command()
@click.argument("resource", type=click.STRING, nargs=1)
@click.option(
    "-d",
    "--dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    nargs=1,
    default=os.getcwd(),
    show_default=False,
    help="Directory to store the downloaded paper in. Defaults to the current "
    "working directory.",
)
@click.option(
    "-u",
    "--unicode",
    "unicode_",
    is_flag=True,
    help="Do not convert Unicode characters in the file name to ASCII.",
)
@click.version_option(version=__version__, message="%(version)s")
def main(resource, dir, unicode_):
    """
    Download the paper from RESOURCE, which should be a link to an arXiv paper
    or its abstract or the arXiv ID of the paper, and name it according to a
    fixed naming convention.
    """
    if is_arxiv_link(resource):
        arxiv_id = extract_arxiv_id(resource)
    else:
        arxiv_id = resource
    download_paper(arxiv_id, dir, unicode_)


def is_arxiv_link(resource):
    """Check if the given resource is an arXiv link or not."""
    if resource.startswith("http"):
        return True
    else:
        return False


def extract_arxiv_id(link):
    """Extract arXiv ID from the given resource."""
    p = re.compile(r"http(?:s|)://arxiv.org/(?:abs/(.+\d)$|pdf/(.+\d)\.pdf$)")
    match = p.fullmatch(link)
    if match is not None:
        arxiv_id = p.group(0) if p.group(0) is not None else p.group(1)
    else:
        raise click.ClickException(f"Not a valid arXiv link: '{link}'.")
    return arxiv_id


def download_paper(id, dir, unicode_):
    """Download a paper from arXiv to a given directory."""
    try:
        paper = next(arxiv.Search(id_list=[id]).get())
        title = paper.title
        year_published = paper.published.year
        authors = [str(a).split(" ")[-1] for a in paper.authors]
        pdf_title = f"{title} - {', '.join(authors)} ({year_published}).pdf"

        # Convert the PDF title to ASCII
        if not unicode_:
            pdf_title = (
                unicodedata.normalize("NFKD", pdf_title)
                .encode("ascii", "ignore")
                .decode("ascii")
            )

        # Prompt to overwrite an existing file
        if os.path.exists(os.path.join(dir, pdf_title)):
            click.confirm(
                text=f"File '{pdf_title}' exists in '{dir}'. Do you want to "
                "overwrite it?",
                default=False,
                show_default=True,
                abort=True,
            )
        paper.download_pdf(filename=pdf_title, dirpath=dir)
    except arxiv.HTTPError as err:
        if err.status == 400:
            raise click.ClickException(f"Not a valid arXiv ID: '{id}'.")
    except Exception:
        raise click.ClickException("Unknown error while downloading.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
