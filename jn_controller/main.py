import packagecap.api
import routetable.api
import tfn2k.api
import bottle
import os


DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 1227

app = bottle.Bottle()
logdir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'log'
if not os.path.exists(logdir):
    os.makedirs(logdir)

@app.route('/start')
def start():
    packagecap.api.API().start_packagecap()
    routetable.api.API().start_routetable()
    tfn2k.api.API().start_tfn2k()

@app.route('/stop')
def stop():
    packagecap.api.API().stop_packagecap()
    routetable.api.API().stop_routetable()
    tfn2k.api.API().stop_tfn2k()


app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
