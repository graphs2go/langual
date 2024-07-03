from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import cache
from typing import TYPE_CHECKING
from xml.etree import ElementTree

from rdflib import URIRef

from langual.models.descriptor import Descriptor

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path


class Thesaurus:
    @dataclass(frozen=True)
    class Header:
        definition: str
        export_date: date
        note: str
        title: str
        uri: str

    @dataclass(frozen=True)
    class _Descriptors:
        by_bt: dict[str | None, list[Descriptor]]
        by_ftc: dict[str, Descriptor]
        by_iri: dict[URIRef, Descriptor]

    def __init__(self, *, xml_file_path: Path):
        element_tree = ElementTree.parse(xml_file_path)  # noqa: S314

        root_element = element_tree.getroot()
        if root_element.tag != "LANGUALSCHEME":
            raise ValueError(f"expected LANGUALSCHEME root tag, got {root_element.tag}")

        header_element = root_element.find("HEADER")
        if header_element is None:
            raise ValueError("missing HEADER element")

        def header_child_text(key: str) -> str:
            child_element = header_element.find(key)
            assert child_element is not None
            child_text = child_element.text
            assert child_text
            return child_text

        self.__header = Thesaurus.Header(
            definition=header_child_text("DEFINITION"),
            export_date=date.fromisoformat(header_child_text("EXPORTDATE")),
            note=header_child_text("NOTE"),
            title=header_child_text("TITLE"),
            uri=header_child_text("URI"),
        )

        self.__iri = URIRef(self.__header.uri)

        descriptors_element = root_element.find("DESCRIPTORS")
        if descriptors_element is None:
            raise ValueError("missing DESCRIPTORS element")
        self.__descriptors_element = descriptors_element

    def descriptor_by_ftc(self, ftc: str) -> Descriptor:
        return self.__descriptors.by_ftc[ftc]

    def descriptor_by_iri(self, iri: URIRef) -> Descriptor:
        return self.__descriptors.by_iri[iri]

    def descriptors(self) -> Iterable[Descriptor]:
        return self.__descriptors.by_ftc.values()

    @property
    @cache
    def __descriptors(self) -> _Descriptors:
        by_bt: dict[str | None, list[Descriptor]] = {}
        by_ftc: dict[str, Descriptor] = {}
        by_iri: dict[URIRef, Descriptor] = {}
        for descriptor_element in self.__descriptors_element:
            ftc_element = descriptor_element.find("FTC")
            assert ftc_element is not None
            ftc = ftc_element.text
            assert ftc
            descriptor = Descriptor(
                element=descriptor_element,
                ftc=ftc,
                thesaurus=self,
            )
            by_bt.setdefault(descriptor.broader_ftc.value_or(None), []).append(
                descriptor
            )
            by_ftc[descriptor.ftc] = descriptor
            by_iri[descriptor.iri] = descriptor
        return Thesaurus._Descriptors(by_bt=by_bt, by_ftc=by_ftc, by_iri=by_iri)

    @property
    def header(self) -> Header:
        return self.__header

    @property
    def iri(self) -> URIRef:
        return self.__iri

    # @classmethod
    # def from_settings(cls, settings: Settings) -> Thesaurus:
    #     return cls(
    #         xml_file_path=settings.paths.data_directory_path
    #         / "langual"
    #         / "LanguaL2017.XML"
    #     )
    #
    def narrower_descriptors(self, descriptor: Descriptor) -> Iterable[Descriptor]:
        """
        Method used by Descriptor.narrower_concepts()
        """
        return self.__descriptors.by_bt.get(descriptor.ftc, [])

    @property
    @cache
    def root_descriptor(self) -> Descriptor:
        root_descriptors = self.__descriptors.by_bt[None]
        # There's a mistake in LanguaL 2017 where the descriptor H0573 has no BT
        # assert len(root_descriptors) == 1
        return root_descriptors[0]
