export interface Vocab {
    id: string;
    type: string;
    title: string;
    description: string | null;
    license: string;
    versioningPolicy: string | null;
    sustainabilityPolicy: string | null;
    created: string;
    modified: string;
    locations: VocabLocation[];
    user: string;
    reviews: Review[];
    usages: {
        count: number;
        outOf: number;
    };
    recommendations: VocabRecommendation[];
    versions: VocabVersion[];
}

export interface Review {
    author: string;
    review: string;
    rating: number;
    like: any[];
    dislike: any[];
}

export interface VocabLocation {
    location: string;
    type: 'homepage' | 'endpoint';
    recipe: 'sparql' | 'skosmos' | 'doc' | 'rdf' | 'cache' | null;
}

export interface VocabVersion {
    version: string;
    validFrom: string | null;
    locations: VocabLocation[];
    summary: VocabSummary | null;
}

export interface VocabRecommendation {
    publisher: string;
    rating: string | null;
}

export interface VocabSummary {
    namespace: {
        uri: string;
        prefix: string;
    },
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
