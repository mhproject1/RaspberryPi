

#################################################

# 지능 IoT 시스템 기말 팀 프로젝트 #

# 과목 : 지능 IoT 시스템
# 주제 : 스마트 원격 멀티탭
# 참여자 : 구명회, 김선재, 김형민

# 구현 순서
# 1. 패키지 import
# 2. blynk 어플리케이션 사용
# 3. 버튼 이벤트 
# 4. setmode / setup
# 5. 버튼 제어
# 6. Ctrl +C

#################################################

############## 필요한 패키지 import ##############
import RPi.GPIO as MH
import time
import blynklib
##################################################

############## blynk 어플리케이션을 사용합니다 ##############
# blynk 어플리케이션을 사용하기 위한 licence code 입니다.
# 이 licence code는 어플리케이션의 로그인 계정의 고유 코드로,
# 어플리케이션에서 회원가입을 하면 메일로 코드를 받을 수 있습니다.
# 이 코드를 사용해서 blynk 웹서버를 구동하고 해당 아이디로 로그인 하면
# blynk 어플리케이션을 사용해서 어디서든 원격으로 조작할 수 있습니다.
BLYNK_AUTH = 'yYGVdaQZie519u_p-T7n2xnD48zG4-VM'
blynk = blynklib.Blynk(BLYNK_AUTH)

# 무슨 버튼이 눌렸는지 라즈베리파이에서 로그를 기록합니다.
# V1~V4의 value값은 0과 1을 가지며,
# value값이 0일때 off, 1일때 on이 되도록 설정되어 있습니다.
# ex) V1 눌렀을 때 > [WRITE_VIRTUAL_PIN_EVENT] Pin: V1 Value: '['0']'
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

#############################################################

######################## 버튼 이벤트 ########################
# state 변수는 버튼의 상태를 기록하고 있습니다.
# [state[0] - 3구] [state[1], state[2], state[3] - 1구]
# 각 버튼을 누를때마다 버튼의 상태값에 1을 더합니다.
# state 변수를 2로 나눴을 때
# 나머지가 1이면 전원이 켜진것이고 0이면 전원이 꺼진것입니다.
state = [0,0,0,0]

# V0 ~ V3 변수는 blynk 어플리케이션에서 지원하는 가상의 핀으로
# 출력값으로 0과 1을 가지고 있고, 기본값은 0입니다.
# 버튼이 입력될 때마다 출력값이 바뀝니다. [기본값 0 > 1 > 0 > 1 > 0 > ...]
### blynk 이벤트 - 3구 제어 ###
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    
    if(value == ['1']):             
        state[0] = state[0] + 1
        GPIO.output(17,True)    # 3구 멀티탭의 전류를 연결합니다.
        GPIO.output(5,True)     # 3구 led On
    else:
        state[0] = state[0] + 1
        GPIO.output(17,False)   # 3구 멀티탭의 전류를 차단합니다.
        GPIO.output(5,False)    # 3구 led Off
        GPIO.output(21,False)   # 1구 led들 Off
        GPIO.output(22,False)   # led가 켜져 있을수도 있기 때문에
        GPIO.output(23,False)   # 3구 버튼을 Off할때 전부 꺼줘야 합니다

### blynk 이벤트 - 1구 제어 ###
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    
    if(value == ['1']):
        state[1] = state[1] + 1
        GPIO.output(18,True)    # 첫번째 1구 멀티탭의 전류를 연결합니다.
        GPIO.output(21,True)    # 첫번째 1구 멀티탭 led On
    else:
        state[1] = state[1] + 1
        GPIO.output(18,False)   # 첫번째 1구 멀티탭의 전류를 차단합니다.
        GPIO.output(21,False)   # 첫번째 1구 멀티탭 led Off

### blynk 이벤트 - 1구 제어 ###
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    
    if(value == ['1']):
        state[2] = state[2] + 1
        GPIO.output(19,True)    # 두번째 1구 멀티탭의 전류를 연결합니다.
        GPIO.output(22,True)    # 두번째 1구 멀티탭 led On
    else:
        state[2] = state[2] + 1
        GPIO.output(19,False)    # 두번째 1구 멀티탭의 전류를 차단합니다.
        GPIO.output(22,False)    # 두번째 1구 멀티탭 led Off

### blynk 이벤트 - 1구 제어 ###
@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    
    if(value == ['1']):
        state[3] = state[3] + 1
        GPIO.output(20,False)   # 세번째 1구 멀티탭의 전류를 연결합니다.
        GPIO.output(23,True)    # 세번째 1구 멀티탭 led On
    else:
        state[3] = state[3] + 1
        GPIO.output(20,True)    # 세번째 1구 멀티탭의 전류를 차단합니다.
        GPIO.output(23,False)   # 세번째 1구 멀티탭 led Off
###########################################################

################## setmode / setup ##################
# 라즈베리파이 핀의 번호로 사용합니다.
MH.setmode(MH.BCM)

# 라즈베리파이에서 사용되고 있는 GPIO핀을
# setup했을때 발생하는 에러를 방지 합니다.
MH.setwarnings(False)

### 멀티탭 ###
# [17 - 3구 멀티탭]  [18, 19, 20 - 1구 멀티탭]
for i in range(17, 21):
    MH.setup(i, MH.OUT)

### On/Off 확인용 LED ###
# [5 - 3구 탭]  [21, 22, 23 - 1구 탭]
MH.setup(5,MH.OUT)

for j in range(21, 24):
    MH.setup(j, MH.OUT)

### 버튼 제어 ###
# [24 - 3구]  [25, 26, 27 - 1구]
for l in range(24, 28):
    MH.setup(l, MH.IN)
##################################################

######################## 버튼 제어 ########################
while True:
    blynk.run()  # blynk 어플리케이션 웹서버 구동

    button = MH.input(24)          # 3구 제어 버튼
    if button == True:                 # 3구 버튼이 눌렸을 때
        state[0] = state[0] + 1     # 3구 버튼의 상태를 변화시킵니다
        time.sleep(0.5)
    
    elif state[0] % 2 == 1:          #3구 전원, LED 켜기
        MH.output(17,True)  
        MH.output(5,True) 
                
        button1 = MH.input(27)    # 1구 제어 버튼        
        button2 = MH.input(26)    # 1구제어들은 3구가 활성화 되어야 
        button3 = MH.input(25)    # 제어할 수 있습니다.
        
        if button1 == True:             # 첫번째 버튼이 눌렸을 때 
            state[1] = state[1] + 1   # 버튼의 상태를 변화시킵니다
            time.sleep(0.5)
        elif state[1] % 2 == 1:       # 해당 1구 전원, LED 켜기
            MH.output(18,True)
            MH.output(21,True)
        elif state[1] % 2 == 0:      # 해당 1구 전원, LED 끄기
            MH.output(18,False)
            MH.output(21,False)
        
        if button2 == True:             # 두번째 버튼이 눌렸을 때 
            state[2] = state[2] + 1  # 버튼의 상태를 변화시킵니다
            time.sleep(0.5)
        elif state[2] % 2 == 1:         # 해당 1구 전원, LED 켜기
            MH.output(19,True)
            MH.output(22,True)
        elif state[2] % 2 == 0:         # 해당 1구 전원, LED 끄기
            MH.output(19,False)
            MH.output(22,False)
                
        if button3 == True:             # 세번째 버튼이 눌렸을 때 
            state[3] = state[3] + 1  # 버튼의 상태를 변화시킵니다
            time.sleep(0.5)
        elif state[3] % 2 == 1:      # 해당 1구 전원, LED 켜기
            MH.output(20,True)
            MH.output(23,True)
        elif state[3] % 2 == 0:     # 해당 1구 전원, LED 끄기
            MH.output(20,False)
            MH.output(23,False)
      
    elif state[0] % 2 == 0:      # 3구 전원 끄기
        MH.output(17,False)    # 3구 전원이 꺼지면 
        MH.output(5,False)     # 1구들의 전력도 차단되며 
        MH.output(21,False)    # 1구 전원의 led도 전부 Off상태로
        MH.output(22,False)    # 설정해줘야 합니다
        MH.output(23,False)
#########################################################

##################### Ctrl +C #####################
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:   # 키보드 인터럽트를 감지하면
        MH.cleanup()               # GPIO 핀을 초기화시키고 
        break                           # 프로그램을 종료합니다
#################################################
    
