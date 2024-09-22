# Graphs2go: LanguaL Thesaurus

Convert the [LanguaL Thesaurus](https://www.langual.org/langual_Thesaurus.asp) to Cypher and SKOS RDF.

## Getting started

### Prerequisites

* [Python](https://www.python.org/)
* [Python Poetry](https://python-poetry.org/)

### Install Python dependencies

    script/bootstrap

### Download the LanguaL Thesaurus

[Download the LanguaL Thesaurus XML file](Click here to download) to `data/input`.

The resulting directory tree should resemble:

* `data/`
  * `input/`
    * `LanguaL2017.XML`

## Usage

Convert the LanguaL Thesaurus into Cypher and RDF and serialize them as files in `data/output`:

    jobs/files

Due to a limitation in Dagster, the script will not exit when all the files have been generated. You will have to terminate it with ^C after you see the message:

    Shutting down Dagster code server
