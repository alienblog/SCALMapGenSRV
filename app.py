from flask import Flask, Response
from config import config, mongo_config, baidu
from rendermap import webscreen, quit_driver
import requests
import json
import pymongo
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

app = Flask(__name__, static_folder='static')

client = pymongo.MongoClient(
    host=mongo_config['host'], port=mongo_config['port'])
db = client.swmdb
eagleyedates = db.hawkeyedata


def getpoints_mongo(entity, start, end):
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


def getpoints_baidu(entity, start, end):
    AK = baidu['ak']
    serviceID = baidu['serviceid']
    url = 'http://yingyan.baidu.com/api/v3/track/gettrack?ak={}&service_id={}&entity_name={}&' \
              'start_time={}&end_time={}'.format(AK, serviceID, entity, int((int(start)-28800000) / 1000), int((int(end)-28800000) / 1000))
    res = requests.get(url)
    data = res.json()
    print(data)
    return res.json()['points']

def __getpoints(entity, start, end):
    points = getpoints_mongo(entity, start, end)
    if points is None or len(points) == 0:
        points = getpoints_baidu(entity,start,end)
    return points


@app.route("/map/<entity>/<start>/<end>")
def render(entity, start, end):
    img = webscreen(entity, start, end)

    return Response(img, mimetype="image/png")


@app.route("/data/<entity>/<start>/<end>")
def getpoints(entity, start, end):
    points = __getpoints(entity, start, end)

    data = json.dumps(points, ensure_ascii=False,
                      separators=(',', ':')).encode('utf-8')
    return Response(data, mimetype="application/json")


if __name__ == "__main__":
    # app.run(port=config['port'])
    http_server = WSGIServer(('0.0.0.0', config['port']), app)
    try:
        print("Start at" + http_server.server_host +
              ':' + str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit...')
    finally:
        quit_driver()
