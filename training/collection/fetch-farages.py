from bing_search_api import BingSearchAPI 
import os, sys
import json
import requests
import shutil

key = os.getenv("BING_KEY")
bing = BingSearchAPI( key )
query = "nigel farage"

out_dir = os.path.dirname(os.path.realpath(__file__))
if len(sys.argv) > 1:
    out_dir = os.path.realpath(sys.argv[1])

count = 0
skip = 0
pagelength = 50

params = { '$format': 'json' }

fetching = True
while fetching:
    params["$skip"] = count
    r = bing.search( 'Image', query, params )
    fetching = False
    results = []
    try:
        results = r.json()["d"]["results"][0]["Image"]
    except Exception as e:
        raise e

    l = len(results)
    print "Bing returned %d results." % l
    if l > 0:

        for result in results:       
            image_url = result["MediaUrl"] 
            image_request = requests.get( image_url, stream=True )
            image_path = os.path.join( out_dir, "%05d.jpg" % count )
            print image_path
            if image_request.status_code == 200:
                with open(image_path, 'wb') as f:
                    image_request.raw.decode_content = True
                    shutil.copyfileobj(image_request.raw, f)  
            count += 1      

        if l >= pagelength:
            fetching = True


print "Fetched %d Farages." % count






