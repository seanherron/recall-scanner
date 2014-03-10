import os

from flask import Flask
from pyelasticsearch import ElasticSearch


app = Flask(__name__)

# We'll initalize the ElasticSearch engine with the URL from the settings file
es = ElasticSearch(os.environ['ES_URL'])

#
# This controls the view for the homepage, which shows the most recent additions
#
@app.route('/')
def show_splash():
    return "Hello World!"

#
# This controls the view for query pages.
#  
@app.route('/search/<upc>')
def search_results(upc):
    return upc