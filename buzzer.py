import RPi.GPIO as GPIO   # RPi.GPIO에 정의된 기능을 GPIO라는 $
import time   # time 모듈

GPIO.setmode(GPIO.BCM)   # GPIO 이름은 BCM 명칭 사용

buzz = 23   # 핀번호 1 대신 buzz 명칭사용을 위>$
GPIO.setup(buzz, GPIO.OUT)   # GPIO buzz핀(1)을 출력으로 설정

#freq = [523,587,659,698,784,880,988,1047]   # freq 리스트 ( 음계 주파수 리스트 )
freq = [ 523, 659, 784 ]
warn = [ 1047, 1047, 1047, 1047, 1047, 1047 ]

def makeOkay(freq):   # 매개변수로freq를 받는 makeTone함수$
        scale = GPIO.PWM(buzz, freq)   # buzz핀으로 freq(Hz) PWM파형을 $
        scale.start(10)   # scale 시작
        time.sleep(0.2)   # 0.5초 대기
        scale.stop()   # scale 정지 ( makeTone함수$
try:
        for x in freq:   # freq 리스트 만큼 반복 시작
                makeOkay(x)   # makeTone 함수에 freq
        GPIO.cleanup()   # GPIO 관련설정 Clear

except KeyboardInterrupt:   # Ctrl-C 입력 시
        GPIO.cleanup()   # GPIO 관련설정 Clear


GPIO.setmode(GPIO.BCM)
buzz = 23   # 핀번호 1 대신 buzz 명칭사용을 위>$
GPIO.setup(buzz, GPIO.OUT)   # GPIO buzz핀(1)을 출력으로 설정


def makeWarning(warn):   # 매개변수로freq를 받는 makeTone>$
        scale = GPIO.PWM(buzz, warn)   # buzz핀으로 freq(Hz) PWM파형을 $
        scale.start(10)   # scale 시작
        time.sleep(0.3)   # 0.5초 대기
        scale.stop()   # scale 정지 ( makeTone함수$

try:
        for x in warn:   # freq 리스트 만큼 반복 시작
                makeWarning(x)   # makeTone 함수에 freq
        GPIO.cleanup()   # GPIO 관련설정 Clear

except KeyboardInterrupt:   # Ctrl-C 입력 시
        GPIO.cleanup()   # GPIO 관련설정 Clear

