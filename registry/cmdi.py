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

xpath_code = "./cmd:code"
xpath_count = "./cmd:count"
xpath_name = "./cmd:name"
xpath_type = "./cmd:type"
xpath_recipe = "./cmd:recipe"
xpath_URI = "./cmd:URI"
xpath_uri = "./cmd:uri"
xpath_prefix = "./cmd:prefix"
xpath_version_no = "./cmd:version"
xpath_valid_from = "./cmd:validFrom"

xpath_location_elem = "./cmd:Location"
xpath_review_elem = "./cmd:body"
xpath_review_author_elem = "./cmd:author"
xpath_review_status_elem = "./cmd:status"
xpath_rating_elem = "./cmd:rating"
xpath_like_elem = "./cmd:like"
xpath_dislike_elem = "./cmd:dislike"
xpath_namespace_elem = "./cmd:Namespaces/cmd:Namespace"
xpath_namespace_item_elem = "./cmd:NamespaceItems/cmd:NamespaceItem"
xpath_summary_elem = "./cmd:Summary"

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

xpath_vocab_type = f"{voc_root}/cmd:type"
xpath_title = f"({voc_root}/cmd:title[@xml:lang='en'][normalize-space(.)!=''],base-uri(/cmd:CMD)[normalize-space(.)!=''])[1]"
xpath_description = f"{voc_root}/cmd:Description/cmd:description"
xpath_license = f"{voc_root}/cmd:License/cmd:url"
xpath_publisher = f"{voc_root}/cmd:Assessement/cmd:Recommendation/cmd:Publisher"
xpath_review = f"{voc_root}/cmd:Assessement/cmd:Review"
xpath_location = f"{voc_root}/cmd:Location"
xpath_version = f"{voc_root}/cmd:Version"
xpath_assessment = f"{voc_root}/cmd:Assessement"


class Location(BaseModel):
    location: str
    type: str
    recipe: Optional[str] = None


class Usage(BaseModel):
    count: int
    outOf: int


class Recommendation(BaseModel):
    publisher: str
    rating: Optional[str] = None


class Review(BaseModel):
    id: int
    review: str
    rating: int
    likes: int
    dislikes: int


class Namespace(BaseModel):
    uri: str
    prefix: Optional[str] = None


class SummaryNamespaceStats(Namespace):
    count: Optional[int] = None


class SummaryNamespaceNameStats(SummaryNamespaceStats):
    name: str


class SummaryStats(BaseModel):
    count: Optional[int] = None
    stats: List[SummaryNamespaceStats]


class SummaryListStats(SummaryStats):
    list: List[SummaryNamespaceNameStats]


class SummaryListLanguageStats(SummaryListStats):
    languages: dict[str, int]


class SummaryObjectStats(SummaryStats):
    classes: SummaryListStats
    literals: SummaryListLanguageStats


class Summary(BaseModel):
    namespace: Optional[Namespace] = None
    stats: Optional[SummaryStats] = None
    subjects: Optional[SummaryStats] = None
    predicates: Optional[SummaryStats] = None
    objects: Optional[SummaryObjectStats] = None


class Version(BaseModel):
    version: str
    validFrom: Optional[str] = None
    locations: List[Location]
    summary: Optional[Summary] = None


class Vocab(BaseModel):
    id: str
    type: str
    title: str
    description: str
    license: str
    versioningPolicy: Optional[str] = None
    sustainabilityPolicy: Optional[str] = None
    created: datetime
    modified: datetime
    locations: List[Location]
    reviews: List[Review] = []
    usage: Usage
    recommendations: List[Recommendation]
    versions: List[Version]


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
    def create_summary_for(elem: Element) -> SummaryStats:
        return SummaryStats(
            count=grab_value(xpath_count, elem, int),
            stats=[SummaryNamespaceStats(
                uri=grab_value(xpath_URI, ns_elem),
                prefix=grab_value(xpath_prefix, ns_elem),
                count=grab_value(xpath_count, ns_elem, int),
            ) for ns_elem in elementpath.select(elem, xpath_namespace_elem, ns)]
        )

    def create_list_for(elem: Element) -> List[SummaryNamespaceNameStats]:
        return [SummaryNamespaceNameStats(
            uri=grab_value(xpath_URI, list_item_elem),
            prefix=grab_value(xpath_prefix, list_item_elem),
            name=grab_value(xpath_name, list_item_elem),
            count=grab_value(xpath_count, list_item_elem, int),
        ) for list_item_elem in elementpath.select(elem, xpath_namespace_item_elem, ns)]

    def create_location_for(elem: Element) -> Location:
        return Location(
            location=grab_value(xpath_uri, elem),
            type=grab_value(xpath_type, elem),
            recipe=grab_value(xpath_recipe, elem),
        )

    def create_review_for(id: int, elem: Element) -> Review:
        return Review(
            id=id,
            review=grab_value(xpath_review_elem, elem),
            rating=grab_value(xpath_rating_elem, elem),
            likes=len(elementpath.select(elem, xpath_like_elem, ns)),
            dislikes=len(elementpath.select(elem, xpath_dislike_elem, ns))
        )

    def create_version(elem: Element) -> Version:
        summary_namespace = Namespace(
            uri=grab_value(xpath_summary_ns_uri, elem),
            prefix=grab_value(xpath_summary_ns_prefix, elem)
        ) if grab_first(xpath_summary_ns, elem) is not None else None

        summary = Summary(
            namespace=summary_namespace,
            stats=create_summary_for(grab_first(xpath_summary_elem, elem)),
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
        ) if grab_first(xpath_summary_st, elem) is not None else (
            Summary(namespace=summary_namespace)) if summary_namespace is not None else None

        return Version(
            version=grab_value(xpath_version_no, elem),
            validFrom=grab_value(xpath_valid_from, elem),
            locations=[create_location_for(loc_elem)
                       for loc_elem in elementpath.select(elem, xpath_location_elem, ns)],
            summary=summary
        )

    file = get_file_for_id(id)
    root = read_root(file)

    return Vocab(
        id=id,
        type=grab_value(xpath_vocab_type, root),
        title=grab_value(xpath_title, root),
        description=grab_value(xpath_description, root),
        license=grab_value(xpath_license, root) or 'http://rightsstatements.org/vocab/UND/1.0/',
        versioningPolicy=None,
        sustainabilityPolicy=None,
        created=datetime.fromtimestamp(os.path.getctime(file), UTC).isoformat(),
        modified=datetime.fromtimestamp(os.path.getmtime(file), UTC).isoformat(),
        locations=[create_location_for(elem)
                   for elem in elementpath.select(root, xpath_location, ns)],
        reviews=[create_review_for(i+1, elem)
                 for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
                 if grab_value(xpath_review_status_elem, elem) == 'published'],
        usage=Usage(count=0, outOf=0),
        recommendations=[Recommendation(publisher=grab_value(xpath_name, elem), rating=None)
                         for elem in elementpath.select(root, xpath_publisher, ns)],
        versions=sorted([create_version(elem) for elem in elementpath.select(root, xpath_version, ns)],
                        key=lambda x: (x.validFrom is not None, x.version), reverse=True)
    )


def get_reviews_user_interaction(id: str, user: str) -> ReviewsUserInteraction:
    file = get_file_for_id(id)
    root = read_root(file)

    authored = [i + 1
                for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
                if user == grab_value(xpath_review_author_elem, elem)]

    likes = [i + 1
             for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
             if user in [unicodedata.normalize("NFKC", like_elem.text)
                         for like_elem in elementpath.select(elem, xpath_like_elem, ns)]]

    dislikes = [i + 1
                for i, elem in enumerate(elementpath.select(root, xpath_review, ns))
                if user in [unicodedata.normalize("NFKC", dislike_elem.text)
                            for dislike_elem in elementpath.select(elem, xpath_dislike_elem, ns)]]

    return ReviewsUserInteraction(authored=authored, likes=likes, dislikes=dislikes)


def create_basic_cmdi(title: str, homepage: str, description: str):
    return True


def add_review_to_cmdi(id: str, author: str, body: str, rating: int):
    file = get_file_for_id(id)
    root = read_root(file)

    assessment_elem = grab_first(xpath_assessment, root)
    review_elem = etree.SubElement(assessment_elem, f"{ns_prefix}Review", nsmap=ns)

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

            for like_elem in elementpath.select(elem, xpath_like_elem, ns):
                if unicodedata.normalize("NFKC", like_elem.text) == user:
                    elem.remove(like_elem)
                    if is_like:
                        should_add_like = False

            for dislike_elem in elementpath.select(elem, xpath_dislike_elem, ns):
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
