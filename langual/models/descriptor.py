from __future__ import annotations

from datetime import date
from functools import cache
from typing import TYPE_CHECKING
from xml.etree.ElementTree import Element

from rdflib import Literal, URIRef
from returns.maybe import Maybe, Nothing, Some
from returns.pipeline import is_successful

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langual.models.thesaurus import Thesaurus


def _children_texts(element: Element | None, child_tag: str) -> tuple[str, ...]:
    if element is None:
        return ()
    children_texts: list[str] = []
    for child_element in element.findall(child_tag):
        child_text = _non_blank_text(child_element)
        if is_successful(child_text):
            children_texts.append(child_text.unwrap())
    return tuple(children_texts)


def _non_blank_text(text: Element | str | None) -> Maybe[str]:
    if text is None:
        return Nothing
    if isinstance(text, Element):
        text_str = text.text
        if text_str is None:
            return Nothing
    else:
        text_str = text
    text_stripped = text_str.strip()
    if not text_stripped:
        return Nothing
    return Some(text_stripped)


class Descriptor:
    """
    A LanguaL thesaurus descriptor.

    Getters lazily parse the underlying ElementTree Element.
    """

    def __init__(self, *, element: Element, ftc: str, thesaurus: Thesaurus):
        self.__element = element
        self.__ftc = ftc
        self.__thesaurus = thesaurus
        self.__iri = URIRef(thesaurus.iri + "#" + ftc)

    @property
    @cache
    def active(self) -> bool:
        return self.__child_text("ACTIVE").unwrap() == "True"

    @property
    @cache
    def additional_information(self) -> Maybe[str]:
        return self.__child_text("AI")

    def broader_descriptors(self) -> Iterable[Descriptor]:
        broader_ftc = self.broader_ftc
        if is_successful(broader_ftc):
            yield self.__thesaurus.descriptor_by_ftc(broader_ftc.unwrap())

    @property
    @cache
    def broader_ftc(self) -> Maybe[str]:
        return self.__child_text("BT")

    def __child_text(self, child_tag: str) -> Maybe[str]:
        return _non_blank_text(self.__element.find(child_tag))

    @property
    @cache
    def classification(self) -> bool:
        return self.__child_text("CLASSIFICATION").unwrap() == "True"

    @property
    @cache
    def date_created(self) -> date:
        return date.fromisoformat(self.__child_text("DATECREATED").unwrap())

    @property
    @cache
    def date_updated(self) -> date:
        return date.fromisoformat(self.__child_text("DATEUPDATED").unwrap())

    @property
    def ftc(self) -> str:
        return self.__ftc

    @property
    def iri(self) -> URIRef:
        return self.__iri

    def narrower_descriptors(self) -> Iterable[Descriptor]:
        yield from self.__thesaurus.narrower_descriptors(self)

    def related_descriptors(self) -> Iterable[Descriptor]:
        for ftc in _children_texts(self.__element.find("RELATEDTERMS"), "RELATEDTERM"):
            yield self.__thesaurus.descriptor_by_ftc(ftc)

    @property
    @cache
    def term(self) -> Maybe[Literal]:  # type: ignore
        term_element = self.__element.find("TERM")
        if term_element is None:
            return Nothing
        return Some(
            Literal(
                term_element.text,
                lang=term_element.attrib["lang"].split()[0],
            )
        )

    @property
    @cache
    def scope_note(self) -> Maybe[str]:
        return self.__child_text("SN")

    @property
    @cache
    def single(self) -> bool:
        return self.__child_text("SINGLE") == "True"

    @property
    @cache
    def synonyms(self) -> tuple[str, ...]:  # type: ignore
        return tuple(_children_texts(self.__element.find("SYNONYMS"), "SYNONYM"))
