import time
import threading
import pygame
from pygame import mixer
import sys
import random

mixer.init()
mixer.music.load("yes_roundabout.ogg") #change the cars to a mini speedwagon for bonus :3
mixer.music.set_volume(0.7)
mixer.music.play()

# Default values of signal timers
defaultGreen = {0:10, 1:10, 2:10, 3:10}
defaultRed = 150
defaultYellow = 5

signals = []
noOfSignals = 4
currentGreen = 0   # Indicates which signal is green currently
nextGreen = (currentGreen+1)%noOfSignals    # Indicates which signal will turn green next
currentYellow = 0   # Indicates whether yellow signal is on or off 

speeds = {'car':0.3, 'bus':0.2, 'truck':0.2, 'bike':0.5}  # average speeds of vehicles, in the year 2030 no speeding tickets exist,feel free to increase this 

# Coordinates of vehicles' start at each of the 4 lanes per road
x = {'right':[0,0,0,0], 'down':[550,610,670,720], 'left':[1265,1265,1265,1265], 'up':[550,610,670,720]}    
y = {'right':[270,330,380,440], 'down':[0,0,0,0], 'left':[270,330,380,440], 'up':[680,680,680,680]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(455,233),(576,546),(706,100),(834,400)]
signalTimerCoods = [(455,233),(576,546),(706,100),(834,400)]

# Coordinates of stop lines
stopLines = {'right': 290, 'down': 90, 'left': 940, 'up': 690}

# Gap between vehicles
stoppingGap = 15    # stopping gap
movingGap = 15   # moving gap

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""


#your job is in this Class, you need to create functions within this class that will aid you in following the rules of the road, 
# this is where you will implement your behaviour planner
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.ogspeed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)
        self.rotated = pygame.image.load(path)
        self.angle = 0
        self.direction = direction
        
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

 ################################################################################################################

    # Behaviour Planner

    def move(self):
        
        # Right
        if self.direction == "right":

            if self.x >= 150 and self.x <= 290:

                # Stopping at red light
                if red_signal[0] == 1:
                    self.speed = 0
        
                # Slow at yellow light
                elif yellow_signal[0] == 1:
                    self.speed = self.ogspeed/2
                
                else:
                    self.speed = self.ogspeed

            # Roundabout
            if self.x >= 290 and self.y <= 270 and self.x <= 410:
                if self.angle < 20:
                    self.image = pygame.transform.rotate(self.image, 20)
                    self.angle += 20
                elif self.x <= 410:
                    self.x += self.speed*0.93
                    self.y -= self.speed*0.34
            
            elif self.x >= 410 and self.x <= 510:
                if self.angle < 60:
                    self.image = pygame.transform.rotate(self.image, 20)
                    self.angle += 40
                elif self.x <= 510:
                    self.x += self.speed*0.77
                    self.y -= self.speed*0.64
            
            elif self.x >= 510:
                if self.angle < 90:
                    self.image = pygame.transform.rotate(self.image, 50)
                    self.angle += 30
                elif self.x <= 545:
                    self.y -= self.speed
                
            # Move
            else:
                self.x += self.speed
        
        # Left
        if self.direction == "left":

            if self.x <= 1080 and self.x >= 940:

                # Stopping at red light
                if red_signal[2] == 1:
                    self.speed = 0
        
                # Slow at yellow light
                elif yellow_signal[2] == 1:
                    self.speed = self.ogspeed/2
                
                else:
                    self.speed = self.ogspeed

            # Roundabout
            if self.x <= 940 and self.x >= 820:
                if self.angle < 20:
                    self.image = pygame.transform.rotate(self.image, 20)
                    self.angle += 20
                elif self.x >= 820:
                    self.x -= self.speed*0.93
                    self.y += self.speed*0.34
            
            elif self.x <= 820 and self.x >= 700:
                if self.angle < 60:
                    self.image = pygame.transform.rotate(self.image, 20)
                    self.angle += 40
                elif self.x >= 700:
                    self.x -= self.speed*0.77
                    self.y += self.speed*0.64
            
            elif self.x <= 700:
                if self.angle < 90:
                    self.image = pygame.transform.rotate(self.image, 50)
                    self.angle += 30
                elif self.x <= 720:
                    self.y += self.speed
                
            # Move
            else:
                self.x -= self.speed

        # Up
        if self.direction == "up":
            
            if self.y <= 690 and self.y >= 680:

                # Stopping at red light
                if red_signal[3] == 1:
                    self.speed = 0
        
                # Slow at yellow light
                elif yellow_signal[3] == 1:
                    self.speed = self.ogspeed/2
                
                else:
                    self.speed = self.ogspeed

            # Roundabout
            if self.y <= 690 and self.y >= 570:
                if self.angle < 20:
                    self.image = pygame.transform.rotate(self.image, 20)
                    self.angle += 20
                elif self.y >= 570:
                    self.y -= self.speed*0.93
                    self.x -= self.speed*0.34
            
            elif self.y >= 400 and self.y <= 570:
                if self.angle < 60:
                    self.image = pygame.transform.rotate(self.image, 20)
                    self.angle += 40
                elif self.y >= 400:
                    self.y -= self.speed*0.77
                    self.x -= self.speed*0.64
            
            elif self.y <= 400:
                if self.angle < 90:
                    self.image = pygame.transform.rotate(self.image, 50)
                    self.angle += 30
                elif self.y >= 365:
                    self.x -= self.speed
                
            # Move
            else:
                self.y -= self.speed

        # Down
        if self.direction == "down":
            
            if self.y >= 0:

                if red_signal[1] == 1:
                    self.speed = 0
        
                # Slow at yellow light
                elif yellow_signal[1] == 1:
                    self.speed = self.ogspeed/2
                
                else:
                    self.speed = self.ogspeed

            # Roundabout
            if self.y >= 100 and self.y <= 240:
                if self.angle < 45:
                    self.image = pygame.transform.rotate(self.image, 45)
                    self.angle += 45
                elif self.y <= 240:
                    self.y += self.speed*0.71
                    self.x += self.speed*0.71
            
            elif self.y >= 240:
                if self.angle < 90:
                    self.image = pygame.transform.rotate(self.image, 45)
                    self.angle += 45
                elif self.y <= 425:
                    self.x += self.speed
                
            # Move
            else:
                self.y += self.speed


 #################################################################################################################       
        



#########################################################################################################################################
#dont worry about this part


# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()

def repeat():
    global currentGreen, currentYellow, nextGreen
    while(signals[currentGreen].green>0):   # while the timer of current green signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = stopLines[directionNumbers[currentGreen]]
    while(signals[currentGreen].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 0   # set yellow signal off
    
     # reset all signal times of current signal to default times
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed
       
    currentGreen = nextGreen # set next signal as green signal
    nextGreen = (currentGreen+1)%noOfSignals    # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow+signals[currentGreen].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()  

# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                signals[i].green-=1
            else:
                signals[i].yellow-=1
        else:
            signals[i].red-=1
####################################################################################################################################################

lanetodir = {0:0, 1:2, 2:2, 3:0}

# Generating vehicles in the simulation, later you can change this so it randomly generates different vehicles in different lanes
def generateVehicles():
    while(True):
        vehicle_type = random.randint(0,3)
        direction_number = random.randint(0,3)
        lane_number = lanetodir[direction_number]
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(3)


thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
thread1.daemon = True
thread1.start()

# Colours 
black = (0, 0, 0)
white = (255, 255, 255)

# Screensize 
screenWidth = 1280
screenHeight = 720
screenSize = (screenWidth, screenHeight)

# Setting background image i.e. image of Gajendra Circle
background = pygame.image.load('images/roundabout.png')

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("SIMULATION")

# Loading signal images and font
redSignal = pygame.image.load('images/signals/red.png')
yellowSignal = pygame.image.load('images/signals/yellow.png')
greenSignal = pygame.image.load('images/signals/green.png')
font = pygame.font.Font(None, 30)

thread2 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
thread2.daemon = True
thread2.start()

red_signal = [0, 0, 0, 0]
yellow_signal = [0, 0, 0, 0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background,(0,0))   # display background in simulation
    for i in range(0,noOfSignals):  # display signal and set timer according to current status: green, yello, or red
        if(i==currentGreen):
            if(currentYellow==1):
                signals[i].signalText = signals[i].yellow
                screen.blit(yellowSignal, signalCoods[i])
                red_signal[i] = 0
                yellow_signal[i] = 1
            else:
                signals[i].signalText = signals[i].green
                screen.blit(greenSignal, signalCoods[i])
                red_signal[i] = 0
                yellow_signal[i] = 0
        else:
            if(signals[i].red<=10):
                signals[i].signalText = signals[i].red
                red_signal[i] = 1
                yellow_signal[i] = 0
            else:
                signals[i].signalText = "---"
                red_signal[i] = 1
                yellow_signal[i] = 0
            screen.blit(redSignal, signalCoods[i])

    signalTexts = ["","","",""]

    # display signal timer
    for i in range(0,noOfSignals):  
        signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
        screen.blit(signalTexts[i],signalTimerCoods[i])

    # display the vehicles
    for vehicle in simulation:  
        screen.blit(vehicle.image, [vehicle.x, vehicle.y])
        vehicle.move()
    pygame.display.update()


