# from flask import Flask, render_template, request
# import sys
# sys.path.append("..")
# from engine.elasticsearch_orm import SearchEngine
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match, Q




client = Elasticsearch()
s = Search(using=client, index='python_documents')


# @app.route('/search/', methods=['POST'])
def search(keys):
    try:
        if keys not in ['']:
            query = s.query(MultiMatch(query=keys, fields=['title', 'body']))
            results = query.execute()
            print(results.to_dict())
    except:
        print('search error!')



client = Elasticsearch()
s = Search(using=client, index='python_documents')

query = s.query(MultiMatch(query='os', fields=['title', 'body']))
results = query.execute()
print(results.to_dict())





























