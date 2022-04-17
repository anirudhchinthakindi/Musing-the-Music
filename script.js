var data
var reader = new FileReader()

function sendData(files) {
  reader.readAsText(files[0], "UTF-8")
  reader.onload = function(event) {
    data = reader.result
    alert("Text to send to program: " + data)
    musicPlayer.src = "https://open.spotify.com/embed/playlist/0Tf8Sf4k3oiK3KWu8m2bMi?utm_source=generator"
  }
}

var musicPlayer = document.getElementById("embeded-music")


/* read text */

var text = document.getElementById('text-area')

document.getElementById('text-submit').addEventListener("dblclick", handleText)

function handleText(evt) {
  data = text.value
  alert("Text to send to program: " + data)
  musicPlayer.src = "https://open.spotify.com/embed/playlist/0Tf8Sf4k3oiK3KWu8m2bMi?utm_source=generator"
}

/* file upload */

function handleFileSelect(evt) {
    console.log("File uploaded.")
    evt.stopPropagation()
    evt.preventDefault()

    let files = evt.dataTransfer.files // FileList object.
    sendData(files)
  }

  function handleDragOver(evt) {
    
    evt.stopPropagation()
    evt.preventDefault()
    evt.dataTransfer.dropEffect = 'copy' // Explicitly show this is a copy.
  }

// Setup the dnd listeners.
var dropZone = document.getElementById('file-upload')

dropZone.addEventListener('dragover', handleDragOver, false)

dropZone.addEventListener('drop', handleFileSelect, false)

dropZone.onchange = e => { 
  sendData(e.target.files)
}

