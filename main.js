const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')

let mainWindow = null
const createWindow = () => {
  mainWindow = new BrowserWindow({
    center: true, icon: path.join(__dirname, 'logo.png'),
    width: 1200, height: 900,
    minWidth: 1200, minHeight: 700,
    maxWidth: 1400, maxHeight: 1200})
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))
  // mainWindow.webContents.openDevTools() //esto tengo que comentar a la hora de hacer la build
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
app.on('activate', function () {
  if (mainWindow === null) {
    createWindow()
  }
})

//para crear el ejecutable del python
const PY_DIST_FOLDER = 'aprioriDistribucion'
const PY_FOLDER = 'apriori'
const PY_MODULE = 'server' // without .py suffix

let pyProc = null
let pyPort = null

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

//para crear el proceso servidor python
const selectPort = () => {
  pyPort = 4242
  return pyPort
}

const createPyProc = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  if (guessPackaged()) {
    pyProc = require('child_process').execFile(script, [port])
  } else {
    pyProc = require('child_process').spawn('python', [script, port])
  }
  if (pyProc != null) {
    console.log('child process success on port ' + port)
    //para que imprima todo lo que ponga print en el archivo apriori.python
    pyProc.stdout.on('data',function(chunk){
        var textChunk = chunk.toString('utf8')
        console.log(textChunk)
    })
    //debuggers nomas
    // pyProc.stderr.on('data', (data) => {
    //   console.error(`child stderr:\n${data}`)
    // })
    pyProc.on('exit', function (code, signal) {
      console.log('child process exited with ' +
      `code ${code} and signal ${signal}`)
      return false
    })
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)
