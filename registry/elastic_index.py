import math
import string

from elasticsearch import Elasticsearch

from registry.config import es_host, es_user, es_password, es_index


class Index:
    def __init__(self):
        self.client = Elasticsearch(
            es_host,
            basic_auth=(es_user, es_password) if es_user and es_password else None,
            verify_certs=False,
            retry_on_timeout=True
        )

    @staticmethod
    def make_matches(search_values):
        return [
            {"multi_match" if item["field"] == "FREE_TEXT" else "match":
                 {"query": value, "fields": ["title", "description"]} if item["field"] == "FREE_TEXT" \
                     else {item["field"]: value}}
            for item in search_values
            for value in item["values"]
        ]

    def get_facet(self, field, amount, facet_filter, search_values):
        terms = {
            "field": field,
            "size": amount,
            "order": {
                "_count": "desc"
            }
        }

        if facet_filter:
            filtered_filter = facet_filter.translate(str.maketrans('', '', string.punctuation))
            filtered_filter = ''.join([f"[{char.upper()}{char.lower()}]" for char in filtered_filter])
            terms["include"] = f'.*{filtered_filter}.*'

        body = {
            "size": 0,
            "aggs": {
                "names": {
                    "terms": terms
                }
            }
        }

        if search_values:
            body["query"] = {
                "bool": {
                    "must": self.make_matches(search_values)
                }
            }

        response = self.client.search(index=es_index, body=body)

        return [{"key": hits["key"], "doc_count": hits["doc_count"]}
                for hits in response["aggregations"]["names"]["buckets"]]

    def browse(self, page, length, search_values):
        int_page = int(page)
        start = (int_page - 1) * length

        if search_values:
            query = {
                "bool": {
                    "must": self.make_matches(search_values)
                }
            }
        else:
            query = {
                "match_all": {}
            }

        response = self.client.search(index=es_index, body={
            "query": query,
            "size": length,
            "from": start,
            "_source": ["id", "title", "description", "type"],
            "sort": [
                {"title.keyword": {"order": "asc"}}
            ]
        })

        return {"amount": response["hits"]["total"]["value"],
                "pages": math.ceil(response["hits"]["total"]["value"] / length),
                "items": [item["_source"] for item in response["hits"]["hits"]]}
