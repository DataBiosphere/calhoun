from flask import Flask, make_response, request
from flask_cors import cross_origin
from flask_talisman import Talisman
from flask_swagger_ui import get_swaggerui_blueprint
from utils import perform_notebook_conversion, perform_rmd_conversion, authorized


# Webservice routing
app = Flask('calhoun')
Talisman(app, force_https=False)
app.config.from_pyfile('config.py')

# Swagger
SWAGGER_URL = '/swagger-ui'
API_URL = '/static/api-docs.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={
        'app_name': "Calhoun"
    },
    oauth_config={
      'clientId': app.config['SWAGGER_CLIENT_ID'],
      'realm': app.config['SWAGGER_REALM'],
      'appName': "Calhoun",
      'scopeSeparator': " "
    }
)

app.register_blueprint(swaggerui_blueprint)

# Swagger CSP needs to have 'unsafe-inline' in the script-src and style-src fields
SWAGGER_CSP = {
    "script-src": ["'self'", "'unsafe-inline'"],
    "style-src": ["'self'", "'unsafe-inline'"]
}
app.view_functions["swagger_ui.show"].talisman_view_options = {
    "content_security_policy": SWAGGER_CSP
}


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
    try:
      return perform_notebook_conversion(json)
    except Exception as e:
      resp = make_response('Response')
      resp.status_code = 400
      resp.data = e.__class__.__name__ + ": " + str(e)
      return resp

@app.route('/api/convert/rmd', methods={'POST'})
@cross_origin()
@authorized(app.config['SAM_ROOT'])
def convert_rmd():
    stream = request.stream
    try:
      return perform_rmd_conversion(stream)
    except Exception as e:
      resp = make_response('Response')
      resp.status_code = 400
      resp.data = e.__class__.__name__ + ": " + str(e)
      return resp

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
