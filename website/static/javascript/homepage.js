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

  function getSensorsValues() {
    fetch('/get_sensors_values')
      .then((response) => response.text())
      .then((html) => {
        document.getElementById("real-time").innerHTML = html
      })
  }

  setInterval(getSensorsValues, 1000)

  function sendTurnoutCmd(path) {
    fetch('/send_turnout_cmd', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ path })
    })
  }

  document.querySelectorAll(".turnout-direction").forEach((select) => {
    select.addEventListener("input", sendTurnoutCmd)
  })

  document.querySelector(".js-inner-path").addEventListener("click", (event) => {
    const svg = event.srcElement.closest('svg')
    svg.classList.add('active')
    svg.style['pointerEvents'] = 'none'

    const outerSvg = document.querySelector(".js-outer-path")
    outerSvg.classList.remove('active')
    outerSvg.style['pointerEvents'] = ''

    sendTurnoutCmd('inner')
  })

  document.querySelector(".js-outer-path").addEventListener("click", () => {
    const svg = event.srcElement.closest('svg')
    svg.classList.add('active')
    svg.style['pointerEvents'] = 'none'

    const innerSvg = document.querySelector(".js-inner-path")
    innerSvg.classList.remove('active')
    innerSvg.style['pointerEvents'] = ''

    sendTurnoutCmd('outer')
  })
})





