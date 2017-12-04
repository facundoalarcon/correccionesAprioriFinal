// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

const path = require('path')
const fs = require("fs")
const zerorpc = require("zerorpc")
let client = new zerorpc.Client()

//cliente, me conecto al servidor zerorpc
client.connect("tcp://127.0.0.1:4242")

//testeo la conexion con el servidor
client.invoke("prueba", "Conexion al servidor correcta", (error, res) => {
  if (error) {
    console.error(" --- NO ANDA NADA :D --- ", error)
  } else {
    console.log(res)
  }
})

//parametros que obtengo de la pagina
let procesar = document.querySelector('#proceseNomas')
let soporte = document.querySelector('#soporte')
let confianza = document.querySelector('#confianza')
let longregla = document.querySelector('#longregla')
let contenido = document.querySelector('#contenido')
let repetidos = document.querySelector('#repetidos')
let pagina = document.querySelector('.container-fluid')

//las reglas que devolvera en el textbox
let reglas = document.querySelector('#reglas')

// Asynchronous read
var leer = (reglasPath) => {
  fs.readFile(reglasPath, function (err, data) {
    if (err) {
      return console.error(err)
    }
    reglas.textContent = data.toString()
  })
}

// para que muestre las informaciones al posarse sobre el signo de pregunta
$('#info').popover()
$('#info2').popover()
$('#info3').popover()

// para poder quitar las advertencias en caso de ingresar mal valores de supp y conf
pagina.addEventListener('click', (err) => {
  try {
    $('#soporteMal').popover('hide')
    $('#confianzaMal').popover('hide')
  }
  catch (error) {
    return true
  }
})

// evento de envio de formulario, llamar a apriori con los parámetros especificados
procesar.addEventListener('click', () => {
  //mostrar barra progreso
  $('#progreso').toggle()
  //obtener dataset local path
  // if (document.querySelector('#dataset').files[0] != undefined) {
    let dataset = document.querySelector('#dataset').files[0].path
  // } else {
  //   $('#noDataset').popover('show')
  //   return false
  // }
  //validaciones de soporte y confianza
  if (!((parseFloat(soporte.value) > 0) && (parseFloat(soporte.value) <= 1))) {
    $('#soporteMal').popover('show')
    $('#progreso').toggle()
    return false
  }
  if (!((parseFloat(confianza.value) > 0) && (parseFloat(confianza.value) <= 1))) {
    $('#confianzaMal').popover('show')
    $('#progreso').toggle()
    return false
  }
  console.log(repetidos.checked)
  //llamada a api del servidor
  client.invoke("apri", dataset, soporte.value, confianza.value,
    longregla.value, contenido.value, repetidos.checked, (error, res) => {
    if(error) {
      $('#progreso').toggle()
      console.error('OOPS: ' + error)
      reglas.textContent = 'No se pudo generar reglas con los valores asignados'
    } else {
      $('#progreso').toggle()
      leer(res)
    }
  })
})
