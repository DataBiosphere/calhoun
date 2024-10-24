from flask import Flask, make_response, render_template, request
from flask_cors import cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from flask_talisman import Talisman
from os import environ

from authorize import authorized
import convert_ipynb_file
import convert_rmd_file


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
        'app_name': 'Calhoun'
    },
    oauth_config={
      'clientId': app.config['SWAGGER_CLIENT_ID'],
      'realm': app.config['SWAGGER_REALM'],
      'appName': 'Calhoun',
      'scopeSeparator': ' '
    }
)

app.register_blueprint(swaggerui_blueprint)

# Swagger CSP needs to have 'unsafe-inline' in the script-src and style-src fields
SWAGGER_CSP = {
    'script-src': ["'self'", "'unsafe-inline'"],
    'style-src': ["'self'", "'unsafe-inline'"]
}
app.view_functions['swagger_ui.show'].talisman_view_options = {
    'content_security_policy': SWAGGER_CSP
}


@app.route('/_ah/warmup')
def warmup():
    # see https://cloud.google.com/appengine/docs/standard/configuring-warmup-requests?tab=python
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
      return convert_ipynb_file.to_safe_html(json)
    except Exception as e:
      errMessage = f'{e.__class__.__name__} : {"".join(str(e).splitlines())} .'
      return render_template('jupyter-error.html', error=errMessage), f'400 {errMessage}'


@app.route('/api/convert/rmd', methods={'POST'})
@cross_origin()
@authorized(app.config['SAM_ROOT'])
def convert_rmd():
    stream = request.stream
    try:
      return convert_rmd_file.to_safe_html(stream)
    except Exception as e:
      errMessage = f'{e.__class__.__name__} : {"".join(str(e).splitlines())} .'
      return render_template('rstudio-error.html', error=errMessage) , f'400 {errMessage}'


if __name__ == '__main__':
    if(environ.get('DEVELOPMENT') == 'true'):
       app.run(port=8080, host='0.0.0.0', ssl_context=('/etc/ssl/certs/server.crt', '/etc/ssl/private/server.key'))
    else:
      app.run(port=8080, host='0.0.0.0')
