from flask import Flask, make_response, request
from flask_cors import cross_origin
from flask_talisman import Talisman
from utils import perform_notebook_conversion, authorized


# Webservice routing
app = Flask('calhoun')
Talisman(app)
app.config.from_pyfile('config.py')


@app.route('/_ah/warmup')
def warmup():
    return '', 200, {}


@app.route('/status')
def status():
    response = make_response('OK')
    response.mimetype = 'text/plain'
    return response


@app.route('/api/convert', methods={'POST'})
@cross_origin()
@authorized(app.config['SAM_ROOT'])
def convert():
    json = request.get_json(force=True)
    return perform_notebook_conversion(json)


if __name__ == '__main__':
    app.run(port=8000)
