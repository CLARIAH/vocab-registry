import os
import elementpath
import unicodedata

from lxml import etree
from datetime import datetime, UTC
from lxml.etree import Element
from pydantic import BaseModel
from typing import Optional, List
from inspect import cleandoc

from registry.config import records_path

ns = {"cmd": "http://www.clarin.eu/cmd/"}
ns_prefix = '{http://www.clarin.eu/cmd/}'
voc_root = './cmd:Components/cmd:Vocabulary'

xpath_identifier = "./cmd:identifier"
xpath_code = "./cmd:code"
xpath_count = "./cmd:count"
xpath_name = "./cmd:name"
xpath_type = "./cmd:type"
xpath_recipe = "./cmd:recipe"
xpath_URI = "./cmd:URI"
xpath_uri = "./cmd:uri"
xpath_label = "./cmd:label"
xpath_title = "./cmd:title"
xpath_url = "./cmd:url"
xpath_landing_page = "./cmd:landingPage"
xpath_prefix = "./cmd:prefix"
xpath_version_no = "./cmd:version"
xpath_valid_from = "./cmd:validFrom"
xpath_body = "./cmd:body"
xpath_author = "./cmd:author"
xpath_published = "./cmd:published"
xpath_status = "./cmd:status"
xpath_rating = "./cmd:rating"
xpath_like = "./cmd:like"
xpath_dislike = "./cmd:dislike"

xpath_location = "./cmd:Location"
xpath_namespace = "./cmd:Namespace"
xpath_summary = "./cmd:Summary"
xpath_namespace_item = "./cmd:NamespaceItems/cmd:NamespaceItem"

xpath_summary_ns = "./cmd:Summary/cmd:Namespace"
xpath_summary_ns_uri = "./cmd:Summary/cmd:Namespace/cmd:URI"
xpath_summary_ns_prefix = "./cmd:Summary/cmd:Namespace/cmd:prefix"

xpath_summary_st = "./cmd:Summary/cmd:Statements"
xpath_summary_st_subj = "./cmd:Summary/cmd:Statements/cmd:Subjects"
xpath_summary_st_pred = "./cmd:Summary/cmd:Statements/cmd:Predicates"
xpath_summary_st_obj = "./cmd:Summary/cmd:Statements/cmd:Objects"
xpath_summary_st_obj_classes = "./cmd:Summary/cmd:Statements/cmd:Objects/cmd:Classes"
xpath_summary_st_obj_literals = "./cmd:Summary/cmd:Statements/cmd:Objects/cmd:Literals"
xpath_summary_st_obj_literals_lang = "./cmd:Summary/cmd:Statements/cmd:Objects/cmd:Literals/cmd:Languages/cmd:Language"

xpath_identification_identifier = f"{voc_root}/cmd:Identification/cmd:identifier"
xpath_identification_title = f"{voc_root}/cmd:Identification/cmd:title"
xpath_identification_namespace = f"{voc_root}/cmd:Identification/cmd:Namespace"
xpath_responsibility_creators = f"{voc_root}/cmd:Responsibility/cmd:Creator"
xpath_responsibility_maintainers = f"{voc_root}/cmd:Responsibility/cmd:Maintainer"
xpath_responsibility_contributors = f"{voc_root}/cmd:Responsibility/cmd:Contributor"
xpath_description_description = f"{voc_root}/cmd:Description/cmd:description"
xpath_description_date_issued = f"{voc_root}/cmd:Description/cmd:dateIssued"
xpath_description_languages = f"{voc_root}/cmd:Description/cmd:language"
xpath_description_topic_unesco = f"{voc_root}/cmd:Description/cmd:topicUnesco"
xpath_description_topic_nwo = f"{voc_root}/cmd:Description/cmd:topicNwo"
xpath_description_keywords = f"{voc_root}/cmd:Description/cmd:Keywords"
xpath_licenses = f"{voc_root}/cmd:License"
xpath_is_referenced_by_registries = f"{voc_root}/cmd:IsReferencedBy/cmd:Registry"
xpath_locations = f"{voc_root}/cmd:Location"
xpath_version = f"{voc_root}/cmd:Version"
xpath_review = f"{voc_root}/cmd:Review"
xpath_type_syntax = f"{voc_root}/cmd:Type/cmd:syntax"
xpath_type_kos = f"{voc_root}/cmd:Type/cmd:kos"
xpath_type_entity = f"{voc_root}/cmd:Type/cmd:entity"
xpath_license_uri = f"{voc_root}/cmd:License/cmd:uri"
xpath_license_label = f"{voc_root}/cmd:License/cmd:label"
xpath_topic_domain = f"{voc_root}/cmd:Topic/cmd:Domain"
xpath_topic_tag = f"{voc_root}/cmd:Topic/cmd:Tag"
xpath_publisher = f"{voc_root}/cmd:Publisher"


class Authority(BaseModel):
    uri: Optional[str] = None
    label: str


class Type(BaseModel):
    syntax: str
    kos: Optional[str] = None
    entity: Optional[str] = None


class Registry(BaseModel):
    title: str
    url: str
    landing_page: Optional[str] = None


class Topic(BaseModel):
    unesco: Optional[str] = None
    nwo: Optional[str] = None


class Location(BaseModel):
    location: str
    type: str
    recipe: Optional[str] = None


class Namespace(BaseModel):
    uri: str
    prefix: Optional[str] = None


class Review(BaseModel):
    id: int
    status: str
    author: str
    published: datetime
    body: str
    rating: int
    likes: List[str] = []
    dislikes: List[str] = []


class SummaryNamespaceStats(Namespace):
    count: Optional[int] = 0


class SummaryNamespaceNameStats(SummaryNamespaceStats):
    name: str


class SummaryStats(BaseModel):
    count: Optional[int] = 0
    stats: List[SummaryNamespaceStats]


class SummaryListStats(SummaryStats):
    list: List[SummaryNamespaceNameStats]


class SummaryListLanguageStats(SummaryListStats):
    languages: dict[str, int]


class SummaryObjectStats(SummaryStats):
    classes: SummaryListStats
    literals: SummaryListLanguageStats


class Summary(BaseModel):
    stats: Optional[SummaryStats] = None
    subjects: Optional[SummaryStats] = None
    predicates: Optional[SummaryStats] = None
    objects: Optional[SummaryObjectStats] = None


class Version(BaseModel):
    version: str
    validFrom: Optional[str] = None
    locations: List[Location] = []
    summary: Optional[Summary] = None


class Vocab(BaseModel):
    identifier: str
    title: str
    namespace: Optional[Namespace] = None
    creators: List[Authority] = []
    maintainers: List[Authority] = []
    contributors: List[Authority] = []
    description: str
    date_issued: Optional[datetime] = None
    languages: List[str] = []
    topic: Optional[Topic] = None
    keywords: List[Authority] = []
    type: Type
    licenses: List[Authority] = []
    registries: List[Registry] = []
    locations: List[Location]
    versions: List[Version]
    reviews: List[Review] = []


class ReviewsUserInteraction(BaseModel):
    authored: List[int]
    likes: List[int]
    dislikes: List[int]


def get_file_for_id(id: str) -> str:
    return os.path.join(records_path, id + '.cmdi')


def read_root(file: str) -> Element:
    parsed = etree.parse(file)
    return parsed.getroot()


def write_root(file: str, root: Element) -> None:
    tree = etree.ElementTree(root)
    etree.indent(tree, space='    ', level=0)
    tree.write(file, encoding='utf-8')


def grab_first(path: str, root: Element) -> Element:
    content = elementpath.select(root, path, ns)
    return content[0] if content else None


def grab_value(path, root, func=None):
    content = elementpath.select(root, path, ns)

    if content and type(content[0]) == str:
        content = unicodedata.normalize("NFKC", content[0]).strip()
    elif content and content[0].text is not None:
        content = unicodedata.normalize("NFKC", content[0].text).strip()
    else:
        content = None

    if content:
        content = cleandoc(content)

    if content and func:
        content = func(content)

    return content


def get_record(id: str) -> Vocab:
    def create_authority_for(elem: Element) -> Authority:
        return Authority(
            uri=grab_value(xpath_uri, elem),
            label=grab_value(xpath_label, elem),
        )

    def create_relaxing_authority_for(elem: Element) -> Authority:
        return Authority(
            uri=grab_value(xpath_uri, elem),
            label=grab_value(xpath_label, elem),
        )

    def create_registry_for(elem: Element) -> Registry:
        return Registry(
            title=grab_value(xpath_title, elem),
            url=grab_value(xpath_url, elem),
            landing_page=grab_value(xpath_landing_page, elem),
        )

    def create_summary_for(elem: Element) -> SummaryStats:
        return SummaryStats(
            count=grab_value(xpath_count, elem, int),
            stats=[SummaryNamespaceStats(
                uri=grab_value(xpath_URI, ns_elem),
                prefix=grab_value(xpath_prefix, ns_elem),
                count=grab_value(xpath_count, ns_elem, int),
            ) for ns_elem in elementpath.select(elem, xpath_namespace, ns)]
        )

    def create_list_for(elem: Element) -> List[SummaryNamespaceNameStats]:
        return [SummaryNamespaceNameStats(
            uri=grab_value(xpath_URI, list_item_elem),
            prefix=grab_value(xpath_prefix, list_item_elem),
            name=grab_value(xpath_name, list_item_elem),
            count=grab_value(xpath_count, list_item_elem, int),
        ) for list_item_elem in elementpath.select(elem, xpath_namespace_item, ns)]

    def create_location_for(elem: Element) -> Location:
        return Location(
            location=grab_value(xpath_uri, elem),
            type=grab_value(xpath_type, elem),
            recipe=grab_value(xpath_recipe, elem),
        )

    def create_version(elem: Element) -> Version:
        summary = Summary(
            stats=create_summary_for(grab_first(xpath_summary, elem)),
            subjects=create_summary_for(grab_first(xpath_summary_st_subj, elem)),
            predicates=create_summary_for(grab_first(xpath_summary_st_pred, elem)),
            objects=SummaryObjectStats(
                **create_summary_for(grab_first(xpath_summary_st_obj, elem)).model_dump(),
                classes=SummaryListStats(
                    **create_summary_for(grab_first(xpath_summary_st_obj_classes, elem)).model_dump(),
                    list=create_list_for(grab_first(xpath_summary_st_obj_classes, elem)),
                ),
                literals=SummaryListLanguageStats(
                    **create_summary_for(grab_first(xpath_summary_st_obj_literals, elem)).model_dump(),
                    list=create_list_for(grab_first(xpath_summary_st_obj_literals, elem)),
                    languages={
                        grab_value(xpath_code, lang_elem): grab_value(xpath_count, lang_elem, int)
                        for lang_elem in elementpath.select(elem, xpath_summary_st_obj_literals_lang, ns)
                    },
                ),
            )
        ) if grab_first(xpath_summary_st, elem) is not None else None

        return Version(
            version=grab_value(xpath_version_no, elem),
            validFrom=grab_value(xpath_valid_from, elem),
            locations=[create_location_for(loc_elem)
                       for loc_elem in elementpath.select(elem, xpath_location, ns)],
            summary=summary
        )

    def create_review_for(id: int, elem: Element) -> Review:
        return Review(
            id=id,
            status=grab_value(xpath_status, elem),
            author=grab_value(xpath_author, elem),
            published=grab_value(xpath_published, elem),
            body=grab_value(xpath_body, elem),
            rating=grab_value(xpath_rating, elem),
            likes=[grab_value('.', elem)
                   for elem in elementpath.select(root, xpath_like, ns)],
            dislikes=[grab_value('.', elem)
                      for elem in elementpath.select(root, xpath_dislike, ns)],
        )

    file = get_file_for_id(id)
    root = read_root(file)

    return Vocab(
        identifier=grab_value(xpath_identification_identifier, root),
        title=grab_value(xpath_identification_title, root),
        namespace=Namespace(
            uri=grab_value(xpath_uri, grab_first(xpath_identification_namespace, root)),
            prefix=grab_value(xpath_prefix, grab_first(xpath_identification_namespace, root))
        ) if grab_first(xpath_identification_namespace, root) is not None else None,
        creators=[create_authority_for(elem)
                  for elem in elementpath.select(root, xpath_responsibility_creators, ns)],
        maintainers=[create_authority_for(elem)
                     for elem in elementpath.select(root, xpath_responsibility_maintainers, ns)],
        contributors=[create_authority_for(elem)
                      for elem in elementpath.select(root, xpath_responsibility_contributors, ns)],
        description=grab_value(xpath_description_description, root),
        date_issued=grab_value(xpath_description_date_issued, root),
        languages=[grab_value('.', elem)
                   for elem in elementpath.select(root, xpath_description_languages, ns)],
        topic=Topic(
            unesco=grab_value(xpath_description_topic_unesco, root),
            nwo=grab_value(xpath_description_topic_nwo, root)
        ) if grab_first(xpath_description_topic_unesco, root) is not None or
             grab_first(xpath_description_topic_nwo, root) is not None else None,
        keywords=[create_relaxing_authority_for(elem)
                  for elem in elementpath.select(root, xpath_description_keywords, ns)],
        type=Type(
            syntax=grab_value(xpath_type_syntax, root),
            kos=grab_value(xpath_type_kos, root),
            entity=grab_value(xpath_type_entity, root)
        ),
        licenses=[create_relaxing_authority_for(elem)
                  for elem in elementpath.select(root, xpath_licenses, ns)],
        registries=[create_registry_for(elem)
                    for elem in elementpath.select(root, xpath_is_referenced_by_registries, ns)],
        locations=[create_location_for(elem)
                   for elem in elementpath.select(root, xpath_locations, ns)],
        versions=sorted([create_version(elem) for elem in elementpath.select(root, xpath_version, ns)],
                        key=lambda x: (x.validFrom is not None, x.version), reverse=True),
        reviews=[create_review_for(i + 1, elem)
                 for i, elem in enumerate(elementpath.select(root, xpath_review, ns))]
    )


def get_reviews_user_interaction(id: str, user: str) -> ReviewsUserInteraction:
    file = get_file_for_id(id)
    root = read_root(file)

    authored = [i + 1
                for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
                if user == grab_value(xpath_author, elem)]

    likes = [i + 1
             for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
             if user in [unicodedata.normalize("NFKC", like_elem.text)
                         for like_elem in elementpath.select(elem, xpath_like, ns)]]

    dislikes = [i + 1
                for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
                if user in [unicodedata.normalize("NFKC", dislike_elem.text)
                            for dislike_elem in elementpath.select(elem, xpath_dislike, ns)]]

    return ReviewsUserInteraction(authored=authored, likes=likes, dislikes=dislikes)


def add_review_to_cmdi(id: str, author: str, body: str, rating: int):
    file = get_file_for_id(id)
    root = read_root(file)

    review_elem = etree.SubElement(root, f"{ns_prefix}Review", nsmap=ns)

    status_elem = etree.SubElement(review_elem, f"{ns_prefix}status", nsmap=ns)
    status_elem.text = 'new'

    author_elem = etree.SubElement(review_elem, f"{ns_prefix}author", nsmap=ns)
    author_elem.text = author

    published_elem = etree.SubElement(review_elem, f"{ns_prefix}published", nsmap=ns)
    published_elem.text = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')

    body_elem = etree.SubElement(review_elem, f"{ns_prefix}body", nsmap=ns)
    body_elem.text = body

    rating_elem = etree.SubElement(review_elem, f"{ns_prefix}rating", nsmap=ns)
    rating_elem.text = str(rating)

    write_root(file, root)


def persist_review_like_to_cmdi(id: str, review_no: int, user: str, is_like: bool):
    file = get_file_for_id(id)
    root = read_root(file)

    found_review = False
    for i, elem in enumerate(elementpath.select(root, xpath_review, ns)):
        if i + 1 == review_no:
            found_review = True
            should_add_like = is_like
            should_add_dislike = not is_like

            for like_elem in elementpath.select(elem, xpath_like, ns):
                if unicodedata.normalize("NFKC", like_elem.text) == user:
                    elem.remove(like_elem)
                    if is_like:
                        should_add_like = False

            for dislike_elem in elementpath.select(elem, xpath_dislike, ns):
                if unicodedata.normalize("NFKC", dislike_elem.text) == user:
                    elem.remove(dislike_elem)
                    if not is_like:
                        should_add_dislike = False

            if should_add_like:
                like_elem = etree.SubElement(elem, f"{ns_prefix}like", nsmap=ns)
                like_elem.text = user
            elif should_add_dislike:
                dislike_elem = etree.SubElement(elem, f"{ns_prefix}dislike", nsmap=ns)
                dislike_elem.text = user

    if found_review:
        write_root(file, root)
    else:
        raise ValueError(f"Review {review_no} not found for {id}")
