document.addEventListener("DOMContentLoaded", () => {

    const cab = document.getElementById("locomotiveId")
    const speed = document.getElementById("velocitySliderInput")
    const direction = document.getElementById("directionUsage")
    const lights = document.getElementById("frontLight")
    const cabButton = document.getElementById("confirmLocomotiveId") 
    //const honkButton = document.getElementById("honkButton") //Não achei o botão de buzina

    function sendData() {
      const data = {
        'cab': parseInt(cab.value),
        'speed': parseInt(speed.value),
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
  
    speed.addEventListener("input", (event) => {
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