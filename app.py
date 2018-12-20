# -*- coding: utf-8 -*-:

from bottle import Bottle, run, request, view
import urllib
import requests

# ------------------
# utility
# ------------------
def fetch_all_tags():
    query = '''
    select ?tag, ?label where {
      ?tag <https://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>.
      ?tag <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/socprob/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql'

    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    tags_array = []
    count_array = []
    for x in responce['results']['bindings']:
        tag = x['label']['value']
        count = count_number_of_annotates_at_tagname(tag)
        tags_array.append(tag)
        count_array.append(count)

    return tags_array, count_array


def count_number_of_annotates_at_tagname(tagname):
    query = '''
    select count(*) where{
      ?annotate a <http://lod.srmt.nitech.ac.jp/tags/ontology#annotate>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#body> <http://tag.srmt.nitech.ac.jp/socprob/''' + tagname + '''>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#target> ?target.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#creator> ?creator.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://lod.srmt.nitech.ac.jp/tags/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql'
    
    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    return responce['results']['bindings'][0]['callret-0']['value']




def count_number_of_annotates():
    query = '''
    select count(*) where{
      ?s a <http://lod.srmt.nitech.ac.jp/tags/ontology#annotate>.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://lod.srmt.nitech.ac.jp/tags/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql'

    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()
    number = int(responce['results']['bindings'][0]['callret-0']['value'])
    number = number + 1

    return number


def fetch_parent_tags(tagname):
    query = '''
    select ?label where {
      <http://tag.srmt.nitech.ac.jp/socprob/''' + tagname + '''> <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?parent.
      ?parent <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/socprob/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql'

    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    parent_array = []
    for x in responce['results']['bindings']:
        label = x['label']['value']
        parent_array.append(label)

    return parent_array


def fetch_child_tags(tagname):
    query = '''
    select ?label where {
      ?child <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://tag.srmt.nitech.ac.jp/socprob/''' + tagname + '''>.
      ?child <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/socprob/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql'

    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    child_array = []
    for x in responce['results']['bindings']:
        label = x['label']['value']
        child_array.append(label)

    return child_array


def fetch_annotates_from_tagname(tagname):
    query = '''
    select * where{
      ?annotate a <http://lod.srmt.nitech.ac.jp/tags/ontology#annotate>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#body> <http://tag.srmt.nitech.ac.jp/socprob/''' + tagname + '''>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#target> ?target.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#creator> ?creator.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://lod.srmt.nitech.ac.jp/tags/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql'
    
    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    target_array = []
    for x in responce['results']['bindings']:
        target = x['target']['value']
        target_array.append(target)

    return target_array


# ------------------
# api
# ------------------
app = Bottle()

@app.get('/')
@app.get('/taglist')
@view('tags')
def tags():
    tags_array, count_array = fetch_all_tags()

    return {
        'tags_array' : tags_array,
        'count_array' : count_array
    }


@app.get('/socprob/<tagname>')
@view('socprob')
def socprob(tagname = '社会問題'):
    parent_array = fetch_parent_tags(tagname)
    child_array = fetch_child_tags(tagname)
    target_array = fetch_annotates_from_tagname(tagname)
    count = count_number_of_annotates_at_tagname(tagname)
    
    return {
        'tagname' : tagname,
        'parent_array' : parent_array,
        'child_array' : child_array,
        'target_array' : target_array,
        'count' : count
    }


@app.get('/annotate')
@view('hello_template')
def get_tag():
    tags_array, count_array = fetch_all_tags()
    return {
        'tags_array' : tags_array,
        'count_array' : count_array,
    }


@app.post('/annotate')
@view('hello_template')
def post_tag():
    tag = str(request.forms.tag)
    annotate = str(request.forms.annotate)
    email = (request.forms.email)
    
    number = count_number_of_annotates()
    
    query = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX tags-annotate: <http://lod.srmt.nitech.ac.jp/tags/annotate/>
    PREFIX tags: <http://lod.srmt.nitech.ac.jp/tags/ontology#>
    
    INSERT DATA
    {
      tags-annotate:'''+str(number)+''' rdf:type tags:annotate ;
      tags:target <'''+annotate+'''> ;
      tags:body <'''+tag+'''> ;
      tags:creator "'''+email+'''" .
    }
    '''
    graphuri = 'http://lod.srmt.nitech.ac.jp/tags/'
    uri = 'http://lod.srmt.nitech.ac.jp/sparql-auth'
    user = 'dba'
    password = 'srmt1ab'
    
    r = requests.get(uri, params={
        'default-graph-uri' : graphuri,
        'query' : query
    }, auth=requests.auth.HTTPDigestAuth(user, password))

    tags_array, count_array = fetch_all_tags()


    return {
        'tags_array' : tags_array,
        'count_array' : count_array
    }




run(app, host='0.0.0.0', port=8088, debug=True)
