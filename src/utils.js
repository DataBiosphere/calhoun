const { exec } = require('child_process')

const execWithPromise = (...args) => {
  let childProcess
  const promise = new Promise((resolve, reject) => {
    childProcess = exec(...args, (error, stdout, stderr) => {
      if (error) {
        reject(error)
      } else {
        resolve({ stdout, stderr })
      }
    })
  })
  return { childProcess, promise }
}

class ErrorResponse extends Error {
  constructor(status, message) {
    super(message)
    this.status = status
  }
}

module.exports = {
  execWithPromise,
  ErrorResponse
}
