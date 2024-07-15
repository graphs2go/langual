from dagster import build_asset_context
from graphs2go.models import interchange
from graphs2go.resources import RdfStoreConfig

from langual import assets
from langual.models import Release


def test_interchange_graph(rdf_store_config: RdfStoreConfig, release: Release) -> None:
    asset = assets.interchange_graph(rdf_store_config=rdf_store_config, release=release)
    assert isinstance(asset, interchange.Graph.Descriptor)
    with interchange.Graph.open(descriptor=asset, read_only=True) as interchange_graph_:
        assert not interchange_graph_.is_empty


def test_release() -> None:
    assert len(assets.releases_partitions_definition.get_partition_keys()) > 0
    assets.release(
        build_asset_context(
            partition_key=assets.releases_partitions_definition.get_first_partition_key()
        )
    )


def test_skos_graph(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    rdf_store_config: RdfStoreConfig,
) -> None:
    assets.skos_graph(
        interchange_graph=interchange_graph_descriptor,
        rdf_store_config=rdf_store_config,
    )  # type: ignore
