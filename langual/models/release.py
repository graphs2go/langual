from __future__ import annotations

from base64 import b64decode, b64encode
from pathlib import Path

from rdflib import URIRef


class Release:
    """
    Picklable descriptor of a MeSH release.
    """

    def __init__(self, file_path: Path):
        file_stem_prefix = "LanguaL"
        if file_path.stem.startswith(file_stem_prefix):
            raise ValueError(
                f"{file_path} file name does not start with {file_stem_prefix}"
            )
        if file_path.suffix.lower() != ".xml":
            raise ValueError(f"{file_path} does not have .xml extension")
        self.__xml_file_path = file_path

        self.__version = int(file_path.stem[len(file_stem_prefix) :])

    @classmethod
    def from_partition_key(cls, partition_key: str) -> Release:
        return Release(Path(b64decode(partition_key).decode("utf-8")))

    @property
    def identifier(self) -> URIRef:
        return URIRef("urn:langual:" + str(self.version))

    def to_partition_key(self) -> str:
        # Getting around https://github.com/dagster-io/dagster/issues/16064
        return b64encode(str(self.__xml_file_path).encode("utf-8")).decode("ascii")

    @property
    def xml_file_path(self) -> Path:
        return self.__xml_file_path

    @property
    def version(self) -> int:
        return self.__version
