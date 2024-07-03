# LanguaL

LanguaL Thesaurus transformation pipelines.

## Prerequisites

* [Python](https://www.python.org/)
* [Python Poetry](https://python-poetry.org/)

## One-time setup

### Install Python dependencies

    script/bootstrap

## Running

### From an installed Poetry virtual environment (recommended for OS X)

#### Run a Dagster pipeline

The code includes multiple [Dagster](https://dagster.io/) pipelines. Each pipeline (a Dagster "job") has a corresponding shell script in `jobs/`.

For example, to transform the LanguaL thesaurus into multiple representations and serialize them as files in `data/output`, run:

    jobs/files

## Structure of this project

* `data/input/`: directory containing LanguaL thesaurus XML
* `data/output/`: transformed/output data such as RDF versions of the LanguaL thesaurus
* `mesh`: Python code
* `script`: scripts following the [Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all) normalized script pattern
* `tests`: unit tests
