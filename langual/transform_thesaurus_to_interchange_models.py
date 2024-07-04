from collections.abc import Iterable

from rdflib import SKOS, Literal
from returns.maybe import Some
from returns.pipeline import is_successful

from graphs2go.models import interchange
from graphs2go.models.label_type import LabelType
from langual.models import Thesaurus, Descriptor


def __transform_descriptor_to_interchange_models(descriptor: Descriptor):
    yield interchange.Node.builder(descriptor.iri).set_created(
        descriptor.date_created
    ).set_modified(descriptor.date_updated).build()

    # Labels
    if is_successful(descriptor.term):
        yield interchange.Label.builder(
            literal_form=Literal(descriptor.term.unwrap()),
            subject=descriptor.iri,
            type_=Some(LabelType.PREFERRED),
        ).build()

    for synonym in descriptor.synonyms:
        yield interchange.Label.builder(
            literal_form=Literal(synonym),
            subject=descriptor.iri,
            type_=Some(LabelType.ALTERNATIVE),
        ).build()

    # Properties
    if is_successful(descriptor.additional_information):
        yield interchange.Property.builder(
            descriptor.iri,
            SKOS.definition,
            Literal(descriptor.additional_information.unwrap()),
        ).build()

    yield interchange.Property.builder(
        descriptor.iri, SKOS.notation, Literal(descriptor.ftc)
    ).build()

    if is_successful(descriptor.scope_note):
        yield interchange.Property.builder(
            descriptor.iri, SKOS.scopeNote, Literal(descriptor.scope_note.unwrap())
        ).build()

    # Relationships
    for broader_descriptor in descriptor.broader_descriptors():
        yield interchange.Relationship.builder(
            descriptor.iri, SKOS.broader, broader_descriptor.iri
        ).build()

    for narrower_descriptor in descriptor.narrower_descriptors():
        yield interchange.Relationship.builder(
            descriptor.iri, SKOS.narrower, narrower_descriptor.iri
        ).build()

    for related_term in descriptor.related_descriptors():
        yield interchange.Relationship.builder(
            descriptor.iri, SKOS.related, related_term.iri
        ).build()


def transform_thesaurus_to_interchange_models(
    thesaurus: Thesaurus,
) -> Iterable[interchange.Model]:
    yield from __transform_thesaurus_to_interchange_models(thesaurus)

    for descriptor in thesaurus.descriptors():
        yield from __transform_descriptor_to_interchange_models(descriptor)


def __transform_thesaurus_to_interchange_models(
    thesaurus: Thesaurus,
) -> Iterable[interchange.Model]:
    yield interchange.Node.builder(iri=thesaurus.iri).add_type(
        SKOS.ConceptScheme
    ).set_modified(thesaurus.header.export_date).build()

    yield interchange.Label.builder(
        literal_form=Literal(thesaurus.header.title),
        subject=thesaurus.iri,
    ).build()
