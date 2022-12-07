import pandas as pd
from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine

import integration
from paginate_pandas import paginate
import os
from flask_jsonpify import jsonpify
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

Bootstrap(app)

pub=[]
query=''
data=pd.DataFrame(columns=['Article Title', 'Authors', 'PMID', 'Language', 'Date'])
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        query=request.form.get('data')
        publications=request.form.getlist('Publication')
        return redirect(url_for("retrive",publications=publications,query=query))

@app.route('/<publications>/<query>', methods = ['GET', 'POST'])
def retrive(publications,query):
    page = request.args.get('page', 1, type=int)
    #print(query)
    global q
    q=query
    global pub
    pub=publications.replace('[','').replace(']','').replace("'",'').split(',')
    #print(pub)
    if ('PubMed' in pub) and len(pub) == 1:
        print('PubMed')
        print(len(publications))
        page = 'Y'
        global i
        i = 0
        #while (page == 'Y'):
        global data
        data=integration.pubmeddata(query, i)
        print(data)
        i = i + 20
        #page = input('Do you want to load the next 20 results?(Y/N):')
    return render_template('result.html',tables=[data.to_html(classes='data')], titles=data.columns.values)

@app.route('/next20')
def next():
    print(q)
    print(pub)
    if ('PubMed' in pub) and len(pub) == 1:
        print('PubMed')
        print(len(pub))
        page = 'Y'
        global data
        #i = len(data)
        #while (page == 'Y'):
        global i
        data=integration.pubmeddata(q, i)
        print(len(data))
        i = i + 20
        #page = input('Do you want to load the next 20 results?(Y/N):')
    return render_template('result.html',tables=[data.to_html(classes='data')], titles=data.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
