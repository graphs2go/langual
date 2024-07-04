from urllib.parse import quote

from dagster import (
    AssetExecutionContext,
    StaticPartitionsDefinition,
    asset,
)
from rdflib import URIRef
from returns.maybe import Some
from tqdm import tqdm

from graphs2go.assets import (
    build_skos_file_asset,
    build_skos_graph_asset,
)
from graphs2go.models import interchange
from graphs2go.resources import DirectoryInputConfig, RdfStoreConfig
from langual.find_releases import find_releases
from langual.models import Release, Thesaurus
from langual.paths import INPUT_DIRECTORY_PATH
from langual.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)

# Static partitions: scan the release directory once at startup
releases_partitions_definition = StaticPartitionsDefinition(
    [
        release.to_partition_key()
        for release in find_releases(
            DirectoryInputConfig.from_env_vars(
                directory_path_default=INPUT_DIRECTORY_PATH
            )
        )
    ]
)


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph(
    rdf_store_config: RdfStoreConfig, release: Release
) -> interchange.Graph.Descriptor:
    with interchange.Graph.create(
        rdf_store_config=rdf_store_config,
        identifier=URIRef("urn:interchange:" + quote(release.identifier)),
    ) as open_interchange_graph:
        return open_interchange_graph.add_all_if_empty(
            lambda: tqdm(
                transform_thesaurus_to_interchange_models(
                    Thesaurus(xml_file_path=release.xml_file_path)
                ),
                desc="interchange graph models",
            )
        ).descriptor


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release(context: AssetExecutionContext) -> Release:
    return Release.from_partition_key(context.partition_key)


skos_file = build_skos_file_asset(partitions_def=Some(releases_partitions_definition))

skos_graph = build_skos_graph_asset(partitions_def=Some(releases_partitions_definition))
