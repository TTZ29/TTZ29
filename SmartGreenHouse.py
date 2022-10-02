import LCD1602
import RPi.GPIO as GPIO
import dht11
from time import sleep
import time
from flask import Flask, render_template_string, request

GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

servo_pin =18
LEDpin1=23
LEDpin2=19

myDHT=dht11.DHT11(pin=24)
GPIO.setup(LEDpin1,GPIO.OUT)
GPIO.output(LEDpin1,GPIO.HIGH)
GPIO.setup(LEDpin2,GPIO.OUT)
GPIO.setup(servo_pin,GPIO.OUT) 
GPIO.output(LEDpin2,GPIO.HIGH)
LCD1602.init(0x27,1)
    
p = GPIO.PWM(servo_pin, 50)  
p.start(0) # Zero duty cycle initially
app = Flask(__name__)

TPL = '''
<html>
    <head><title>Web Page Controlled Door</title></head>
    <body>
    <h2> Web Page to Control Door</h2>
        <form method="POST" action="test">
            <h3> Use the slider to Door  </h3>
            <p>Open Door   -----Min<input type="range" min="8" max="11" name="slider" /> Max</p>
            <input type="submit" value="Go!" />
        </form>
    </body>
</html>

'''


try:
    while True:
       
        result=myDHT.read()
        tempC=result.temperature
      
        hum=result.humidity
        
        if result.is_valid():
            if tempC<=35 and tempC>=23:
                GPIO.output(LEDpin1,GPIO.HIGH)
                GPIO.output(LEDpin2,GPIO.LOW)
                LCD1602.write(0,0,'Temp: ')
                LCD1602.write(6,0,str(tempC) + chr(223))
                LCD1602.write(11,0,'C   ')
                LCD1602.write(0,1,'Humidity: ')
                LCD1602.write(10,1,str(hum))
                LCD1602.write(14,1,'%')
                
                @app.route("/")               
                def home():                                                                                                                                                         
                    return render_template_string(TPL)                        
                @app.route("/test", methods=["POST"])
                def test():
                    slider = request.form["slider"]
                    p.ChangeDutyCycle(float(slider))
                    sleep(1)
                    p.ChangeDutyCycle(0)
                    return render_template_string(TPL)
                if __name__ == "__main__":
                   app.run(host="0.0.0.0", port=8500)
                
            if tempC>35:
                GPIO.output(LEDpin1,GPIO.LOW)
                GPIO.output(LEDpin2,GPIO.LOW)
                LCD1602.write(0,0,'Temp: ')
                LCD1602.write(6,0,str(tempC) + chr(223))
                LCD1602.write(11,0,'C   ')
                LCD1602.write(0,1,'ALERT: High Temp!')
                
                @app.route("/")               
                def home():                                                                                                                                                         
                    return render_template_string(TPL)                        
                @app.route("/test", methods=["POST"])
                def test():
                    slider = request.form["slider"]
                    p.ChangeDutyCycle(float(slider))
                    sleep(1)
                    p.ChangeDutyCycle(0)
                    return render_template_string(TPL)
                if __name__ == "__main__":
                   app.run(host="0.0.0.0", port=8500)
                
            if tempC<23:
                GPIO.output(LEDpin1,GPIO.HIGH)
                GPIO.output(LEDpin2,GPIO.HIGH)
                LCD1602.write(0,0,'Temp: ')
                LCD1602.write(6,0,str(tempC) + chr(223))
                LCD1602.write(11,0,'C   ')
                LCD1602.write(0,1,'ALERT: LOW Temp!')
                time.sleep(.9)
                @app.route("/")               
                def home():                                                                                                                                                         
                    return render_template_string(TPL)                        
                @app.route("/test", methods=["POST"])
                def test():
                    slider = request.form["slider"]
                    p.ChangeDutyCycle(float(slider))
                    sleep(1)
                    p.ChangeDutyCycle(0)
                    return render_template_string(TPL)
                if __name__ == "__main__":
                   app.run(host="0.0.0.0", port=8500)
                

                
                
except KeyboardInterrupt:
    time.sleep(.2)
    GPIO.cleanup()
    LCD1602.clear()
    print('System Good to Go')

