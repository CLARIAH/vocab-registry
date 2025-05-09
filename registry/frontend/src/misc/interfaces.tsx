export interface Vocab {
    identifier: string;
    title: string;
    namespace: Namespace | null;
    creators: Authority[];
    maintainers: Authority[];
    contributors: Authority[];
    description: string;
    date_issued: string;
    languages: string[];
    topic: Topic | null;
    keywords: Authority[];
    type: Type;
    licenses: Authority[];
    registries: Registry[];
    locations: Location[];
    versions: Version[];
    reviews: Review[];
}

export interface Namespace {
    uri: string;
    prefix: string;
}

export interface Authority {
    uri: string | null;
    label: string;
}

export interface Topic {
    unesco: string | null;
    nwo: string | null;
}

export interface Type {
    syntax: string;
    kos: string | null;
    entity: string | null;
}

export interface Registry {
    title: string;
    url: string;
    landing_page: string | null;
}

export interface Location {
    location: string;
    type: 'homepage' | 'endpoint';
    recipe: 'sparql' | 'skosmos' | 'doc' | 'rdf' | 'cache' | null;
}

export interface Version {
    version: string;
    validFrom: string | null;
    locations: Location[];
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

export interface Review {
    id: number;
    published: string;
    body: string;
    rating: number;
    likes: number;
    dislikes: number;
}

export interface VocabIndex {
    id: string;
    title: string;
    description: string;
    syntax: string;
}
