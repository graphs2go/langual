import pytest

from graphs2go.models import interchange
from langual.models import Release, Thesaurus
from langual.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)


def test_transform(release: Release) -> None:
    actual_interchange_model_class_set: set[type[interchange.Model]] = set()
    expected_interchange_model_class_set = {
        interchange.Label,
        interchange.Node,
        interchange.Property,
        interchange.Relationship,
    }
    for interchange_model in transform_thesaurus_to_interchange_models(
        Thesaurus(xml_file_path=release.xml_file_path)
    ):
        actual_interchange_model_class_set.add(interchange_model.__class__)
        if expected_interchange_model_class_set == actual_interchange_model_class_set:
            return
    pytest.fail("not all interchange models represented")
