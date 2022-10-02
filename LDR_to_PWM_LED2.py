from machine import Pin, ADC, PWM
import utime

pwm = PWM ( Pin ( 1 ) ) 				# GP1
pwm. freq ( 100000 ) 					# 100kHz 
ldr = machine.ADC(26)
conversion_factor = 3.3/(65536)
pwmint = int
pwm.duty_u16(0)							# generate PWM signal with 0% duty cycle

print("startup")
while True:
    ldrval=ldr.read_u16() * conversion_factor
    pwmint=((2-ldrval)*43691)
    if (ldrval) < 2:
        pwm. duty_u16 (int(pwmint)) 	# duty
        print("led val 1, ldr val")
        print(ldrval)
        print("pwm duty val")
        print(pwmint)
        utime.sleep(0.1)
    else:
        pwm. duty_u16 ( 0 ) 			# duty 0% 
        print("led val 0, ldr val")
        print(ldrval)
        utime.sleep(0.1)



