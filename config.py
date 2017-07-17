
import os

mongo_config = {}
config = {}
baidu = {}
baidu['ak'] = 'DIm4fQkBGR2aZWorGMDPILqclf46gAX5'
baidu['serviceid'] = '139760'

config['host'] = '192.168.0.131'
config['port'] = 81
config['phantomjs-url'] = 'http://127.0.0.1:8910'

__web_host = os.environ.get('WEB_HOST')
if __web_host:
    config['host'] = __web_host

__phantomjs_url = os.environ.get('PHANTOMJS_URL')
if __phantomjs_host:
    config['phantomjs-url'] = __phantomjs_url

__web_port = os.environ.get("WEB_PORT")
if __web_port:
    config['port'] = __web_port

mongo_config['host'] = "192.168.0.55"
mongo_config['port'] = 27017
mongo_config['user'] = 'admin'
mongo_config["pwd"] = 'admin'

__mongo_host = os.environ.get('MONGO_HOST')
if __mongo_host:
    mongo_config['host'] = __mongo_host

__mongo_port = os.environ.get('MONGO_PORT')
if __mongo_port:
    mongo_config['port'] = __mongo_port

__mongo_user = os.environ.get('MONGO_USER')
if __mongo_user:
    mongo_config['user'] = __mongo_user

__mongo_pwd = os.environ.get("MONGO_PWD")
if __mongo_pwd:
    mongo_config['pwd'] = __mongo_pwd

__baidu_ak = os.environ.get('BAIDU_AK')
__baidu_serviceid = os.environ.get('BAIDU_SERID')
if __baidu_ak:
    baidu['ak'] = __baidu_ak
if __baidu_serviceid:    
    baidu['serviceid'] = __baidu_serviceid