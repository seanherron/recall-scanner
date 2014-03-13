import os
import urllib

from flask import Flask, render_template, request
from pyelasticsearch import ElasticSearch


app = Flask(__name__)
app.debug = True

# We'll initalize the ElasticSearch engine with the URL from the settings file
es = ElasticSearch(os.environ['ES_URL'])

#
# This controls the view for the homepage, which shows the most recent additions
#
def generate_query(platform):
    if platform in ('iphone', 'ipad', 'ipod'):
        query_url = 'pic2shop://scan?formats=UPCE,UPC&callback=%s' % urllib.quote_plus('%ssearch?upc=UPC' % request.url_root)
        app_prefix = 'pic2shop://'
        app_name = 'pic2shop'
        app_url = 'itms-apps://itunes.apple.com/us/app/pages/id308740640?mt=8&uo=4'
    elif platform == 'android':
        query_url = 'intent://scan/?ret=%s#Intent;scheme=zxing;package=com.google.zxing.client.android;end' % urllib.quote_plus('%ssearch?upc={CODE}' % request.url_root)
        app_prefix = 'zxing://'
        app_name = 'ZXing Barcode Scanner'
        app_url = 'market://details?id=com.google.zxing.client.android'
        
    else:
        query_url = None
        app_prefix = None
        app_name = None
        app_url = None
        
    return query_url, app_prefix, app_name, app_url


@app.route('/')
def show_splash():
    query_url, app_prefix, app_name, app_url = generate_query(request.user_agent.platform)
    return render_template('search.html', scan=request.args.get('scan'), root_url = request.url_root, query_url=query_url, app_prefix=app_prefix, app_name=app_name, app_url=app_url, platform=request.user_agent.platform)
#
# This controls the view for query pages.
#  
@app.route('/search')
def search_results():
    if request.args.get('upc'):
        upc = request.args.get('upc')
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
    
        query_url, app_prefix, app_name, app_url = generate_query(request.user_agent.platform)
        return render_template('show_recalls.html', scan=request.args.get('scan'), recalls=recalls, page_title=upc, query_url=query_url, app_prefix=app_prefix, app_name=app_name, app_url=app_url)
    else:
        return "No UPC Code Provided!"