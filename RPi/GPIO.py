from os.path import exists


BCM = 1
OUT = 1
IN = 1
HIGH = 1
LOW = 0
RISING = 1
FALLING = 0
PUD_DOWN = 0

def setmode(_a):
   pass
def setup(_a, _b, pull_up_down=None):
   pass
def output(_a, _b):
   with open('/tmp/gpio' + str(_a), 'w') as fakegpio:
      fakegpio.write(str(_b))
def input(_a):
   if not exists('/tmp/gpio' + str(_a)):
      with open('/tmp/gpio' + str(_a), 'w') as fakegpio:
         fakegpio.write('0')
      return 0
   with open('/tmp/gpio' + str(_a), 'r') as fakegpio:
      data = fakegpio.read()
   return int(data)
def cleanup():
   print('Fucking cleanup called')
def setwarnings(flag):
   pass

def add_event_detect(_a, _b, callback):
   pass