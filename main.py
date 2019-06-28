from sanic import Sanic
from sanic import response
from sanic_cors import CORS, cross_origin
from utils import perform_notebook_conversion, authorized


# Webservice routing
app = Sanic('douglass')
app.config.from_pyfile('config.py')
CORS(app)


@app.get('/status')
async def status(request):
    return response.text('OK')

@app.route('/api/convert', methods={'POST','OPTIONS'})
@cross_origin(app, automatic_options=True)
@authorized(app.config.SAM_ROOT)
async def convert(request):
    return response.html(await perform_notebook_conversion(request.json))


if __name__ == '__main__':
    app.run(port=8000)
