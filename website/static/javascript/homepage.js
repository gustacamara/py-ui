document.addEventListener("DOMContentLoaded", () => {
    const cab = document.getElementById("cab-id")
    const speed = document.getElementById("speed-slider-input")
    const direction = document.getElementById("direction-switch")
    const frontLight = document.getElementById("front-light")
    const secondaryLight = document.getElementById("secondary-light")
    const cabButton = document.getElementById("confirm-cab-id") 
    //const honkButton = document.getElementById("honkButton")

    function sendData() {
      const data = {
        'cab': parseInt(cab.value),
        'speed': parseInt(speed.value),
        'direction': direction.value,
        'frontLight': frontLight.checked,
        'secondaryLight': secondaryLight.checked
      }
  
      console.log(data)
  
      fetch('/send_dcc_cmd', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
    }
  
    speed.addEventListener("input", (event) => {
      sendData()
    })
  
    frontLight.addEventListener("input", (event) => {
      sendData()
    })

    secondaryLight.addEventListener("input", (event) => {
      sendData()
    })
  
    direction.addEventListener("input", (event) => {
      sendData()
    })
  
    cabButton.addEventListener("click", (event) => {
      sendData()
    })
  
    // honkButton.addEventListener("mousedown", (event) => {
    //   console.log("down")
    // })
  
    // honkButton.addEventListener("mouseup", (event) => {
    //   console.log("up")
    // })
  
  function getSensorsValues() {
    fetch('/get_sensors_values')
      .then((response) => response.text())
      .then((html) => {
        const dom = new DOMParser().parseFromString(html, "text/xml")
        document.getElementById("real-time").replaceChildren(dom.firstChild)
      })
  }

  setInterval(getSensorsValues, 1000)
})





