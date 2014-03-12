import os
import urllib

from flask import Flask, render_template, request
from pyelasticsearch import ElasticSearch


app = Flask(__name__)
app.config['DEBUG'] = True
app.debug = True

# We'll initalize the ElasticSearch engine with the URL from the settings file
es = ElasticSearch(os.environ['ES_URL'])

#
# This controls the view for the homepage, which shows the most recent additions
#
def generate_query_url(platform):
    if platform == 'android':
        query_url = 'zxing://scan/?ret=%ssearch?q={CODE}' % urllib.quote_plus(request.url_root)
    elif platform == 'iphone' or platform == 'ipad':
        query_url =  'pic2shop://scan?formats=UPCE,UPC&lookup=%s/CODE' % urllib.quote_plus(request.url_root)
    else:
        
        query_url = None
    
    return query_url


@app.route('/')
def show_splash():            
        return render_template('search.html', query_url=generate_query_url(request.user_agent.platform), platform=request.user_agent.platform)
#
# This controls the view for query pages.
#  
@app.route('/search')
def search_results():
    if request.args.get('ean'):
        # Remove the first digit from the pic2shop returned UPC code
        upc = request.args.get('ean')
        if len(upc) == 13:
            upc = upc[:1]
        elif len(upc) == 12:
            upc = request.args.get('ean')
        else:
            upc = request.args.get('ean')
    else:
        upc = request.args.get('q')
    recalls_raw = es.search('product-description:%s' % upc, index=os.environ['ES_INDEX'])
    recalls_raw = recalls_raw["hits"]["hits"]
    recalls = []
    for item in recalls_raw:
        recall = {}
        recall['product_type'] = item['_source']['product-type']
        recall['event_id'] = item['_source']['event-id']
        recall['status'] = item['_source']['status']
        recall['recalling_firm'] = item['_source']['recalling-firm']
        recall['city'] = item['_source']['city']
        recall['state'] = item['_source']['state']
        recall['country'] = item['_source']['country']
        recall['voluntary_mandated'] = item['_source']['voluntary-mandated']
        recall['distribution_pattern'] = item['_source']['distribution-pattern']
        recall['product_description'] = item['_source']['product-description']
        recall['code_info'] = item['_source']['code-info']
        recall['reason_for_recall'] = item['_source']['reason-for-recall']
        recall['date'] = item['_source']['recall-initiation-date']
        recall['product_name'] = item['_source']['product-description'].split(',', 1)[0]
        
        recalls.append(recall)
    return render_template('show_recalls.html', recalls=recalls, page_title=upc, query_url=generate_query_url(request.user_agent.platform))