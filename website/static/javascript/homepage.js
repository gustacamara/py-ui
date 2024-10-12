document.addEventListener("DOMContentLoaded", () => {
    const cab = document.getElementById("cab-id")
    const speedScrollbar = document.getElementById("speed-slider-input")
    const direction = document.getElementById("direction-usage")
    const lights = document.getElementById("front-light")
    const cabButton = document.getElementById("confirm-cab-id") 
    //const honkButton = document.getElementById("honkButton") //Não achei o botão de buzina

    function sendData() {
      const data = {
        'cab': parseInt(cab.value),
        'speedScrollbar': parseInt(speedScrollbar.value),
        'direction': direction.value,
        'lights': lights.checked
      }
  
      console.log(data)
  
      fetch('http://192.168.100.107:3000', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
    }
  
    speedScrollbar.addEventListener("input", (event) => {
      sendData()
    })
  
    lights.addEventListener("input", (event) => {
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
  
  });