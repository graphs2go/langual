import logging
from collections.abc import Iterable
from pathlib import Path

import pytest
from graphs2go.models import interchange, skos
from graphs2go.resources import DirectoryInputConfig, OutputConfig, RdfStoreConfig
from graphs2go.utils import configure_markus, load_dotenv
from returns.maybe import Nothing

from langual import assets
from langual.find_releases import find_releases
from langual.models import Release
from langual.paths import INPUT_DIRECTORY_PATH

load_dotenv()
configure_markus()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def input_config() -> DirectoryInputConfig:
    return DirectoryInputConfig.default(directory_path_default=INPUT_DIRECTORY_PATH)


@pytest.fixture(scope="session")
def interchange_graph(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
) -> Iterable[interchange.Graph]:
    with interchange.Graph.open(
        descriptor=interchange_graph_descriptor, read_only=True
    ) as interchange_graph:
        yield interchange_graph


@pytest.fixture(scope="session")
def interchange_graph_descriptor(
    rdf_store_config: RdfStoreConfig, release: Release
) -> interchange.Graph.Descriptor:
    return assets.interchange_graph(rdf_store_config=rdf_store_config, release=release)  # type: ignore


@pytest.fixture()
def output_config(tmp_path: Path) -> OutputConfig:
    return OutputConfig(directory_path=str(tmp_path))


@pytest.fixture(scope="session")
def rdf_store_config() -> RdfStoreConfig:
    return RdfStoreConfig.default(directory_path_default=Nothing)


@pytest.fixture(scope="session")
def release(input_config: DirectoryInputConfig) -> Release:
    return find_releases(input_config=input_config)[0]


@pytest.fixture(scope="session")
def skos_graph_descriptor(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    rdf_store_config: RdfStoreConfig,
) -> skos.Graph.Descriptor:
    return assets.skos_graph(
        interchange_graph=interchange_graph_descriptor,
        rdf_store_config=rdf_store_config,
    )  # type: ignore
