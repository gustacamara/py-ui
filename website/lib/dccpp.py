# MQTT topic: pyui/dcc-K3xWvP4p4D

def generateDccThrottleCmd(cabId, speed, direction):
    speed = 126 if speed > 126 else speed
    speed = 0 if speed < 0 else speed
    
    return f'<t 1 {cabId} {speed} {direction}>'

def generateDccFunctionCmd(cabId, lights, secondaryLights):
    function0 = 1 if lights else 0
    function1 = 1 if secondaryLights else 0

    functionByte = 128 + function1 + function0 * 16

    return f'<f {cabId} {functionByte}>'