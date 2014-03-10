import os
import urllib

from flask import Flask, render_template, request
from pyelasticsearch import ElasticSearch


app = Flask(__name__)
app.config['DEBUG'] = True

# We'll initalize the ElasticSearch engine with the URL from the settings file
es = ElasticSearch(os.environ['ES_URL'])

#
# This controls the view for the homepage, which shows the most recent additions
#
@app.route('/')
def show_splash():
    platform = request.user_agent.platform
    if platform == 'android' or platform == 'iphone' or platform == 'ipad':
        query_url = 'zxing://scan/?ret=%s/{CODE}' % urllib.quote_plus(request.url_root)
    else:
        query_url = None
        
    return render_template('search.html', query_url=query_url)

#
# This controls the view for query pages.
#  
@app.route('/<upc>')
def search_results(upc):
    recalls = es.search('product-description:%s' % upc, index=os.environ['ES_INDEX'])
    
    return render_template('show_recalls.html', recalls=recalls["hits"]["hits"], count=recalls["hits"]["total"], page_title=upc)