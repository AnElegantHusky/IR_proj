from flask import Flask, render_template, request
import sys
sys.path.append("..")
from engine.elasticsearch_orm import SearchEngine
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match, Q
from math import ceil


app = Flask(__name__)
app.config['DEBUG'] = True

client = Elasticsearch()
s = Search(using=client)

documents = dict()
results = []
global keys
global page
global docs

#########################################################
def cut_page(docs, start):
    if len(docs) >= 10:
        result = docs[start: start+10]
    else:
        result = docs[start:]
    return result


#########################################################

@app.route('/')
def main():
    return render_template('search.html', error=False)

@app.route('/search/', methods=['POST'])
def search():
    try:
        global documents, results, keys, docs, page
        keys = request.form['key_word']
        if keys not in ['']:
            query = s.query(MultiMatch(query=keys, fields=['title', 'body']))
            results_dict = query.execute().to_dict()
            results_hits = results_dict['hits']
            total = results_hits['total']
            results = results_hits['hits']

            docs = cut_page(results, 0)
            page = ceil(total / 10) + 1 #
            documents = {i['_id']: i['_source'] for i in docs}
            return render_template('search.html', key=keys, docs=docs, page=page, error=True)
    except:
        print('search error!')

@app.route('/search/<id>/', methods=['GET', 'POST'])
def content(id):
    try:
        print(documents[id])
        return render_template('content.html', doc=documents[id])
    except:
        print('content error')

@app.route('/search/page/<page_num>/', methods=['GET'])
def next_page(page_num):
    try:
        page_num = int(page_num)
        docs = cut_page(results, 10 * page_num)
        return render_template('search.html', key=keys, docs=docs, page=page, error=True)

    except:
        print('next error')

















if __name__ == '__main__':
    app.run()













