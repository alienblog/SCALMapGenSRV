from flask import Flask, Response
from config import config, mongo_config
from rendermap import webscreen, quit_driver
import json
import pymongo
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

app = Flask(__name__,static_folder='static')


client = pymongo.MongoClient(
    host=mongo_config['host'], port=mongo_config['port'])
db = client.swmdb
eagleyedates = db.hawkeyedata


@app.route("/map/<entity>/<start>/<end>")
def render(entity, start, end):
    img = webscreen(entity, start, end)
    
    return Response(img,mimetype="image/png")

@app.route("/data/<entity>/<start>/<end>")
def getpoints(entity, start, end):
    data = []
    criteria = {}
    criteria['loc_time'] = {
        "$gte": int(int(start) / 1000),
        "$lte": int(int(end) / 1000),
    }
    criteria['entityname'] = entity
    print(criteria)
    cursor = eagleyedates.find(criteria)
    for el in cursor:
        del el['_id']
        data.append(el)

    data = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return Response(data, mimetype="application/json")


if __name__ == "__main__":
    # app.run(port=config['port'])
    http_server = WSGIServer(('0.0.0.0', config['port']), app)
    try:
        print("Start at"+http_server.server_host+':'+str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit...')
    finally:
        quit_driver()

