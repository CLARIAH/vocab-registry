export interface Vocab {
    id: string;
    title: string;
    description: string;
    created: string;
    modified: string;
    type: Type;
    license: License;
    locations: VocabLocation[];
    namespace: Namespace | null;
    topic: Topic | null;
    reviews: Review[];
    publishers: Publisher[];
    versions: VocabVersion[];
}

export interface Type {
    syntax: string;
    kos: string | null;
    entity: string | null;
}

export interface License {
    uri: string;
    label: string;
}

export interface Review {
    id: number;
    review: string;
    rating: number;
    likes: number;
    dislikes: number;
}

export interface VocabLocation {
    location: string;
    type: 'homepage' | 'endpoint';
    recipe: 'sparql' | 'skosmos' | 'doc' | 'rdf' | 'cache' | null;
}

export interface Namespace {
    uri: string;
    prefix: string;
}

export interface Topic {
    domain: Domain | null;
    tags: Tag[];
}

export interface Domain {
    unesco: string | null;
    nwo: string | null;
}

export interface Tag {
    tag: string;
    uri: string | null;
}

export interface Publisher {
    identifier: string;
    name: string;
    uri: string;
}

export interface VocabVersion {
    version: string;
    validFrom: string | null;
    locations: VocabLocation[];
    summary: VocabSummary | null;
}

export interface VocabSummary {
    stats: VocabSummaryCounts;
    subjects: VocabSummaryCounts;
    predicates: VocabSummaryCounts & VocabSummaryList;
    objects: VocabObjectSummary & {
        classes: VocabSummaryCounts & VocabSummaryList | null;
        literals: VocabSummaryCounts & VocabSummaryList & {
            languages: {
                code: string;
                count: number;
            }[];
        } | null;
    }
}

export interface VocabSummaryCounts {
    count: number;
    stats: {
        uri: string;
        prefix: string;
        count: number;
    }[];
}

export interface VocabSummaryList {
    list: VocabSummaryListItem[];
}

export interface VocabSummaryListItem {
    uri: string;
    prefix: string;
    name: string;
    count: number;
}

export interface VocabObjectSummary {
    classes: VocabSummaryCounts | null;
    literals: VocabSummaryCounts | null;
}

export interface VocabIndex {
    id: string;
    title: string;
    description: string;
    type: string;
}
