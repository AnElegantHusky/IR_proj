from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class engineMiddleware(DocType):
    title = Text(analyzer="standard")
    body = Text(analyzer="standard")
    url = Keyword()

    # class Index:
    #     name = "scrapy"
    #     settings = {
    #         "number_of_shards": 5
    #     }
    #     doc_type = "python_documents"
    #
    class Meta:
        index = "python_documents"
        doc_type = "collections"

class SearchEngine(object):
    pass


if __name__ == "__main__":
    engineMiddleware.init()

# from elasticsearch import Elasticsearch
#
# es = Elasticsearch()







