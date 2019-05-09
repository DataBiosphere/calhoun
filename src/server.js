const express = require('express')
const fetch = require('node-fetch')
const cors = require('cors')
const { execWithPromise, ErrorResponse } = require('./utils')
const { samRoot } = require('../config')

const MAX_OUTPUT_SIZE = 1024 * 1024 * 20

const app = express()
app.use(cors())
app.use('/docs', express.static('docs'))

app.get('/status', async (req, res) => {
  res.sendStatus(200)
})

/**
 * @api {post} /api/convert Convert a notebook to static HTML
 * @apiName convert
 * @apiVersion 1.0.0
 * @apiGroup Convert
 * @apiParam {String} body Jupyter notebook file
 * @apiSuccess {String} body HTML representation of notebook
 */
app.post('/api/convert', async (req, res) => {
  try {
    const authRes = await fetch(
      `${samRoot}/register/user/v2/self/info`,
      { headers: { authorization: req.headers.authorization } }
    ).catch(() => {
      throw new ErrorResponse(503, 'Unable to contact auth service')
    })
    if (authRes.status === 401) {
      throw new ErrorResponse(401, 'Unauthorized')
    }
    if (!authRes.ok) {
      console.error('Sam error', await authRes.text())
      throw new ErrorResponse(503, 'Failed to query auth service')
    }
    const { enabled } = await authRes.json()
    if (!enabled) {
      throw new ErrorResponse(403, 'Forbidden')
    }

    const { childProcess, promise } = execWithPromise(
      'jupyter nbconvert --stdin --stdout',
      { maxBuffer: MAX_OUTPUT_SIZE }
    )
    req.pipe(childProcess.stdin)
    const { stdout } = await promise.catch(error => {
      throw new ErrorResponse(400, error.toString())
    })
    console.log(`Converted ${stdout.length} bytes`)
    return res.send(stdout)
  } catch (error) {
    console.error(error)
    res.status(error.status || 500).json({ message: error.toString() })
  }
})

app.listen(process.env.PORT || 8080)
