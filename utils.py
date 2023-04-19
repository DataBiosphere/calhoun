from flask import request
from requests import get
from requests.exceptions import ConnectionError
from functools import wraps
from nbconvert import HTMLExporter
from nbformat.v4 import to_notebook
from tempfile import NamedTemporaryFile
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import *
from rpy2.robjects.packages import importr
import json
import os
import logging
from bs4 import BeautifulSoup

def perform_notebook_conversion(notebook_json):
    # Get the notebook json into a NotebookNode object that nbconvert can use
    nb = to_notebook(notebook_json)

    # set up a default nbconvert HTML exporter and run the conversion
    html_exporter = HTMLExporter()
    (nb_html, resources_dict) = html_exporter.from_notebook_node(nb)
    
    safe_html = remove_inline_scripts(nb_html)
    
    return safe_html


def perform_rmd_conversion(stream):
    binary_data = stream.read()
    data = binary_data.decode('ascii')
    sanitized_data = __sanitize_rmd(data)
    
    # The rmarkdown converter unfortunately only works with files.
    # So we create temp files for the source markdown and destination html data.
    # The temp files are deleted as soon as the below with block ends.
    with NamedTemporaryFile(suffix=".Rmd") as in_file:
        in_file.write(sanitized_data) 
        in_file.seek(0)

        # Call R rmarkdown package from python.
        # See https://cran.r-project.org/web/packages/rmarkdown/index.html
        rmd = importr("rmarkdown")
        rendered_html = rmd.render(in_file.name)
        out_path = rendered_html[0]
        
        try:
            out_file = open(out_path)
            read_outfile = out_file.read()
        finally:
            out_file.close()
            os.remove(out_path)
        return read_outfile
    
# We need to sanitize any code blocks (ex ```{bash}) from the rmd before rendering it
# This is because kitr (https://rmarkdown.rstudio.com/authoring_quick_tour.html#Rendering_Output.), which powers our rendering
# Actually executes any code in a labeled codeblock. By processing out any of these labels, we ensure we display a preview without a possible arbitrary code execution vulnerability
# See this document, issue number one, for more details on the vulnerability: https://docs.google.com/document/d/1aNCOKitTJH-GEkBSR4i-x91O0OQCZ8ZYa3feXtkja94/edit#heading=h.rvpr6zoz0jem 
# Takes a string and returns binary
def __sanitize_rmd(data: str) -> bytes:
    logging.info(f'printing data to sanitize pre-split: {data}')
    lines = data.split('\n')
    logging.info(f'printing lines of file: {lines}')
    sanitized_file = []
    for line in lines:
        if line.startswith('```'):
            sanitized_line = '```'
        else: 
            sanitized_line = line
        sanitized_file.append(sanitized_line)    
        
    file = '\n'.join(sanitized_file)
    logging.info(f'putting data put back together {file}')
    
    return file.encode('ascii')


# Authorization decorator
# Decorated routes will first check the request to see if the caller is authorized to perform the operation
# taken from example in Sanic documentation
# https://sanic.readthedocs.io/en/latest/sanic/decorators.html
def authorized(sam_root):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check the Terra authorization service SAM for user auth status
            user_is_authorized = __check_sam_authorization(sam_root)
            if user_is_authorized:
                # run the handler method and return the response
                response = f(*args, **kwargs)
                return response
            else:
                raise Forbidden
        return decorated_function
    return decorator


# Query Terra's authorization service SAM to determine user authorization status. Return auth status boolean
def __check_sam_authorization(sam_root):
    sam_url = sam_root + '/register/user/v2/self/info'

    # Well-formed requests must contain an authorization header
    if 'authorization' not in request.headers:
        raise Unauthorized('Request requires authorization header supplying Oauth2 bearer token')
    try:
        sam_response = get(sam_url, headers={'authorization': request.headers['authorization']})
        return __process_sam_response(sam_response)
    except ConnectionError:
        raise ServiceUnavailable('Service Unavailable. Unable to contact authorization service')


# Check the sam response and respond appropriately.
# Return True if the user is authorized, otherwise raise a relevant exception with a helpful message
def __process_sam_response(sam_response):
    # For an authorized user, we will receive a 200 status code with 'enabled: True' in the response body
    status = sam_response.status_code
    if status == 200:
        if 'enabled' not in sam_response.json():
            raise InternalServerError('Internal Server Error. Unable to determine user authorization status')
        elif not sam_response.json()['enabled']:
            raise Forbidden('Forbidden. User is registered in Terra, but not activated.')
        else:
            # SAM service returned 200 and the user was enabled. User is authorized.
            return True
    # Intercept non-successful status codes and return a more helpful message
    else:
        if status == 401:
            raise Unauthorized('Unauthorized. User is not allowed in Terra or has not signed in.')
        elif status == 403:
            raise Forbidden
        elif status == 404:
            raise Unauthorized('Unauthorized. User is authenticated to Google but is not a Terra member')
        elif status == 500:
            raise InternalServerError('Internal Server Error. Authorization service query failed')
        elif status == 503:
            raise ServiceUnavailable('Service Unavailable. Authorization service unable to contact one or more services')
        else:
            raise InternalServerError('Internal Server Error. Unknown failure contacting authorization service.')

def read_json_file(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data
    
def remove_inline_scripts(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    # remove math jax script from dom
    # this would be done together with the for loop below, but semantically it makes sense to separate them
    # all previews will have this first script, as it is part of the nbconvert lib we use
    # on the other hand, any other scripts to remove are a result of python libs in a specific notebook relying on javascript to render output 
    mathJaxUnsafeScript = soup.select_one('script[type="text/x-mathjax-config"]')
    
    if mathJaxUnsafeScript is not None:
        mathJaxUnsafeScript.decompose()
    
    allJavascriptTags = soup.findAll('script')
    allUntrustedJavascriptTags = list(filter(lambda scriptTag: not ('src' in scriptTag.attrs and 'https://cdnjs.cloudflare.com' in scriptTag['src']), allJavascriptTags))
    
    # Remove all script tags that dont have a src containing https://cdnjs.cloudflare.com, which is trusted via the terra-ui CSP
    # See this PR for implementation in UI https://github.com/DataBiosphere/terra-ui/pull/2438/files#diff-d506904027666817584075d2f1141152f8d72d02f355f39f3585453278ecdedbR24
    if len(allUntrustedJavascriptTags) > 0:
        logging.info(f"Detected preview has Javascript from an untrusted source. Removing {len(allUntrustedJavascriptTags)} count(s) as required by csp")
        for untrustedScriptTag in allUntrustedJavascriptTags:
            untrustedScriptTag.decompose()
             
    return str(soup)
