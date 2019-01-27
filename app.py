# -*- coding: utf-8 -*-:

from bottle import Bottle, run, request, view
import urllib
import requests

from datetime import datetime

# ------------------
# global val
# ------------------
sparql_endpoint_url = 'http://lod.srmt.nitech.ac.jp/sparql'
sparql_endpoint_url_auth = 'http://lod.srmt.nitech.ac.jp/sparql-auth'
sparql_auth_user = 'dba'
sparql_auth_pass = 'srmt1ab'

# ------------------
# utility
# ------------------
def fetch_all_other_tags():
    query = '''
    select ?tag, ?label where {
      ?tag <https://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>.
      ?tag <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/other/'

    r = requests.get(sparql_endpoint_url, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    tags_array = []
    labels_array = []
    count_array = []
    for x in responce['results']['bindings']:
        tag = x['tag']['value']
        label = x['label']['value']
        count = count_number_of_annotates_at_taguri(tag)
        tags_array.append(tag)
        labels_array.append(label)
        count_array.append(count)

    return tags_array, labels_array, count_array


def fetch_all_social_tags():
    query = '''
    select ?tag, ?label where {
      ?tag <https://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>.
      ?tag <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/socprob/'

    r = requests.get(sparql_endpoint_url, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    tags_array = []
    labels_array = []
    count_array = []
    for x in responce['results']['bindings']:
        tag = x['tag']['value']
        label = x['label']['value']
        count = count_number_of_annotates_at_taguri(tag)
        tags_array.append(tag)
        labels_array.append(label)
        count_array.append(count)

    return tags_array, labels_array, count_array


def count_number_of_annotates_at_taguri(taguri):
    query = '''
    select count(*) where{
      ?annotate a <http://lod.srmt.nitech.ac.jp/tags/ontology#annotate>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#body> <''' + taguri + '''>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#target> ?target.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#creator> ?creator.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://mf.srmt.nitech.ac.jp/tags/'
    
    r = requests.get(sparql_endpoint_url, params={
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
    graphuri = 'http://mf.srmt.nitech.ac.jp/tags/'

    r = requests.get(sparql_endpoint_url, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()
    number = int(responce['results']['bindings'][0]['callret-0']['value'])
    number = number + 1

    return number


def fetch_parent_social_tags(taguri):
    query = '''
    select ?label where {
      <''' + taguri + '''> <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?parent.
      ?parent <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/socprob/'

    r = requests.get(sparql_endpoint_url, params={
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


def fetch_child_social_tags(taguri):
    query = '''
    select ?label where {
      ?child <http://www.w3.org/2000/01/rdf-schema#subClassOf> <''' + taguri + '''>.
      ?child <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://tag.srmt.nitech.ac.jp/socprob/'

    r = requests.get(sparql_endpoint_url, params={
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


def fetch_annotates_from_taguri(taguri):
    query = '''
    select * from <http://mf.srmt.nitech.ac.jp/tags/> where{
      ?annotate a <http://lod.srmt.nitech.ac.jp/tags/ontology#annotate>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#body> <''' + taguri + '''>.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#target> ?target.
      ?annotate <http://lod.srmt.nitech.ac.jp/tags/ontology#creator> ?creator.
      
      {
        select ?target ?name ?missionname
        from <http://mf.srmt.nitech.ac.jp/>
        where {
         ?target <http://purl.org/dc/terms/title> ?name.
         ?target <http://lod.srmt.nitech.ac.jp/resource/MissionForest/ontology#mission> ?mission .
         ?mission <http://purl.org/dc/terms/title> ?missionname
        }
      }
    }
    '''
    retformat = 'application/sparql-results+json'
    graphuri = 'http://mf.srmt.nitech.ac.jp/tags/'
    
    r = requests.get(sparql_endpoint_url, params={
        'default-graph-uri' : graphuri,
        'query' : query,
        'format' : retformat
    })
    responce = r.json()

    target_array = []
    name_array = []
    for x in responce['results']['bindings']:
        target = x['target']['value']
        name = x['name']['value'] + ' | ' + x['missionname']['value']
        target_array.append(target)
        name_array.append(name)

    return target_array, name_array


# ------------------
# api
# ------------------
app = Bottle()

@app.get('/')
@app.get('/taglist')
@view('tags')
def tags():
    print('[' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '] ' + '/')
    
    social_tags_array, social_labels_array, social_count_array = fetch_all_social_tags()
    other_tags_array, other_labels_array, other_count_array = fetch_all_other_tags()

    return {
        'social_tags_array' : social_tags_array,
        'social_labels_array' : social_labels_array,
        'social_count_array' : social_count_array,
        'other_tags_array' : other_tags_array,
        'other_labels_array' : other_labels_array,
        'other_count_array' : other_count_array
    }



@app.get('/socprob/<tagname>')
@view('socprob')
def socprob(tagname = '社会問題'):
    print('[' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '] ' + '/socprob/' + tagname)
    taguri = 'http://tag.srmt.nitech.ac.jp/socprob/' + tagname
    parent_array = fetch_parent_social_tags(taguri)
    child_array = fetch_child_social_tags(taguri)
    target_array, name_array = fetch_annotates_from_taguri(taguri)
    count = count_number_of_annotates_at_taguri(taguri)
    
    return {
        'tagname' : tagname,
        'parent_array' : parent_array,
        'child_array' : child_array,
        'target_array' : target_array,
        'name_array' : name_array,
        'count' : count
    }

@app.get('/other/<tagname>')
@view('other')
def other(tagname = 'イベント開催'):
    print('[' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '] ' + '/other/' + tagname)
    taguri = 'http://tag.srmt.nitech.ac.jp/other/' + tagname
    target_array, name_array = fetch_annotates_from_taguri(taguri)
    count = count_number_of_annotates_at_taguri(taguri)
    
    return {
        'tagname' : tagname,
        'target_array' : target_array,
        'name_array' : name_array,
        'count' : count
    }



@app.get('/newtag')
@view('newtag')
def get_new_tag():
    return None

@app.post('/newtag')
@view('newtag')
def post_tag():
    tagname = str(request.forms.tagname)
    
    query = '''
    INSERT
    {
      <http://tag.srmt.nitech.ac.jp/other/'''+str(tagname)+'''> <http://www.w3.org/2000/01/rdf-schema#label> "'''+str(tagname)+'''"@jp .
      <http://tag.srmt.nitech.ac.jp/other/'''+str(tagname)+'''> <https://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>
    }
    '''
    graphuri = 'http://tag.srmt.nitech.ac.jp/other/'
    
    r = requests.get(sparql_endpoint_url_auth, params={
        'default-graph-uri' : graphuri,
        'query' : query
    }, auth=requests.auth.HTTPDigestAuth(sparql_auth_user, sparql_auth_pass))
    

    return None


@app.get('/annotate')
@view('annotate')
def get_tag():
    tags_array = []
    labels_array = []
    count_array = []
    
    social_tags_array, social_labels_array, social_count_array = fetch_all_social_tags()
    tags_array.extend(social_tags_array)
    labels_array.extend(social_labels_array)
    count_array.extend(social_count_array)
    
    other_tags_array, other_labels_array, other_count_array = fetch_all_other_tags()
    tags_array.extend(other_tags_array)
    labels_array.extend(other_labels_array)
    count_array.extend(other_count_array)
    
    return {
        'tags_array' : tags_array,
        'labels_array' : labels_array,
        'count_array' : count_array,
    }


@app.post('/annotate')
@view('annotate')
def post_tag():
    tag = str(request.forms.tag)
    annotate = str(request.forms.annotate)
    
    number = count_number_of_annotates()
    
    query = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX tags-annotate: <http://lod.srmt.nitech.ac.jp/tags/annotate/>
    PREFIX tags: <http://lod.srmt.nitech.ac.jp/tags/ontology#>
    
    INSERT
    {
      tags-annotate:'''+str(number)+''' rdf:type tags:annotate ;
      tags:target <http://lod.srmt.nitech.ac.jp/resource/MissionForest/tasks/'''+annotate+'''> ;
      tags:body <'''+tag+'''> ;
      tags:creator "m-watanabe@srmtlab.org" .
    }
    '''
    graphuri = 'http://mf.srmt.nitech.ac.jp/tags/'
    
    r = requests.get(sparql_endpoint_url_auth, params={
        'default-graph-uri' : graphuri,
        'query' : query
    }, auth=requests.auth.HTTPDigestAuth(sparql_auth_user, sparql_auth_pass))

    tags_array = []
    labels_array = []
    count_array = []
    
    social_tags_array, social_labels_array, social_count_array = fetch_all_social_tags()
    tags_array.extend(social_tags_array)
    labels_array.extend(social_labels_array)
    count_array.extend(social_count_array)
    
    other_tags_array, other_labels_array, other_count_array = fetch_all_other_tags()
    tags_array.extend(other_tags_array)
    labels_array.extend(other_labels_array)
    count_array.extend(other_count_array)
    
    return {
        'tags_array' : tags_array,
        'labels_array' : labels_array,
        'count_array' : count_array,
    }




run(app, host='0.0.0.0', port=8088, debug=True)
