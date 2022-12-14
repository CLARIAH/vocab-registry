from elasticsearch import Elasticsearch
import math


class Index:
    def __init__(self, config):
        self.config = config
        # self.es = Elasticsearch(hosts=[{"host": "ecodices_es"}], retry_on_timeout=True)
        self.client = Elasticsearch(hosts=[{"host": "elastic"}], retry_on_timeout=True)

    def no_case(self, str_in):
        str = str_in.strip()
        ret_str = ""
        if (str != ""):
            for char in str:
                ret_str = ret_str + "[" + char.upper() + char.lower() + "]"
        return ret_str + ".*"

    def get_facet(self, field, amount):
        ret_array = []
        response = self.client.search(
            index="vocab",
            body=
            {
                "size": 0,
                "aggs": {
                    "names": {
                        "terms": {
                            "field": field,
                            "size": amount,
                            "order": {
                                "_term": "asc"
                            }
                        }
                    }
                }
            }
        )
        for hits in response["aggregations"]["names"]["buckets"]:
            buffer = {"key": hits["key"], "doc_count": hits["doc_count"]}
            ret_array.append(buffer)
        return ret_array



    def get_filter_facet(self, field, amount, facet_filter):
        ret_array = []
        response = self.client.search(
            index="vocab",
            body=
            {
                "query": {
                    "regexp": {
                        field: self.no_case(facet_filter)
                    }
                },
                "size": 0,
                "aggs": {
                    "names": {
                        "terms": {
                            "field": field,
                            "size": amount,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    }
                }
            }
        )
        for hits in response["aggregations"]["names"]["buckets"]:
            buffer = {"key": hits["key"], "doc_count": hits["doc_count"]}
            ret_array.append(buffer)
        return ret_array

    def item(self, id):
        response = self.client.search(
            index="vocab",
            body={"query": {
                "terms": {
                    "record": [id]
                }
            }
            }
        )
        if response["hits"]["total"]["value"] == 1:
            return response["hits"]["hits"][0]["_source"]
        else:
            return []

    def browse(self, page, length, orderFieldName, searchvalues):
        int_page = int(page)
        start = (int_page - 1) * length
        matches = []

        if searchvalues == []:
            response = self.client.search(
                index="vocab",
                body={"query": {
                    "match_all": {}},
                    "size": length,
                    "from": start,
                    "_source": ["record","title", "publisher"],
                    "sort": [
                        {orderFieldName: {"order": "asc"}}
                    ]
                }
            )
        else:
            for item in searchvalues:
                for value in item["values"]:
                    if item["field"] == "FREE_TEXT":
                        matches.append({"multi_match": {"query": value, "fields": ["*"]}})
                    else:
                        matches.append({"match": {item["field"] + ".keyword": value}})
            response = self.client.search(
                index="vocab",
                body={"query": {
                    "bool": {
                        "must": matches
                    }},
                    "size": length,
                    "from": start,
                    "sort": [
                        {orderFieldName: {"order": "asc"}}
                    ]
                }
            )

        ret_array = {"amount": response["hits"]["total"]["value"],
                     "pages": math.ceil(response["hits"]["total"]["value"] / length), "items": []}
        for item in response["hits"]["hits"]:
            tmp_arr = item["_source"]
            tmp_arr["_id"] = item["_id"]
            ret_array["items"].append(tmp_arr)
        return ret_array
