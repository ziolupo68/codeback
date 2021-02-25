import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


RADIUS_CHECKPOINT=600
RADIUS_POD=400
MAX_THRUST=100
BOOST_ANGLE=20
BOOST_DISTANCE=3000

def log(message):
    print(message, file=sys.stderr, flush=True)
def inside(value, radius):
    if -radius <= value <= radius:
        return True
    return False


class Point:
  def __init__(self,x,y,):
      self.x = x
      self.y = y

  def distance(self, other):
    return math.sqrt( (self.x - other.x)**2 + (self.y- other.y)**2)

  def distance2(self, other):
    return  (self.x - other.x)**2 + (self.y- other.y)**2

  def __eq__(self, other):
      return ((self.x, self.y) == (other.x, other.y))

  def __ne__(self, other):
    return not self.__eq__(other) 

  def __str__(self):
    return "Point(%s,%s)"%(self.x, self.y)        

  def __repr__(self):
    return "Point(%s,%s)"%(self.x, self.y) 

class Circuit:
  def __init__(self):
    self.lap=1
    self.numberOfCheckpoints=0
    self.firstCheckpoint=None
    self.lastCheckpoint=Point(0,0)
    self.nextnextCheckpoint=None
    self.checkpoints=[]

  def addCheckpoint(self,checkpoint):
    if any(p==checkpoint for p in self.checkpoints):
      if checkpoint==self.firstCheckpoint and self.firstCheckpoint!=self.lastCheckpoint:
        self.lap=self.lap+1
      if self.lap>1:
        i=self.checkpoints.index(checkpoint)
        self.nextnextCheckpoint=self.checkpoints[(i + 1) % len(self.checkpoints)]
    else:
      self.numberOfCheckpoints = self.numberOfCheckpoints+1
      self.checkpoints.append(checkpoint)
    if not self.firstCheckpoint:
      self.firstCheckpoint=checkpoint
    if (self.lastCheckpoint!=checkpoint):
      self.lastCheckpoint=checkpoint

class Pod():
  def __init__(self,name,circuit):
    self.name=name
    self.circuit=circuit
    self.position=Point(0,0)
    self.previous_position=Point(0,0)
    self.nextCheckpointAngle=0
    self.nextCheckPointDistance=0
    self.nextCheckpoint=Point(0,0)
    self.speed_x=0
    self.speed_y=0
    self.speed=0
    self.angle=0
    self.thrust=MAX_THRUST
    self.boost=0
    self.targetAngle=90

  def isBoostAvailable(self):
    if self.boost==0:
      return True
    return False

  def useBoost(self):
    self.boost +=1

  def tryToBoost(self):
    if self.isBoostAvailable():
      # PAOLO: insert here the boost logic
      # We boost only if thrust is 100. No sense give penalties to thrust and than boost
      # if at start angle is 0 and next checkpoint is far enough, boost immediately
      if self.circuit.lap>1:
        if self.nextCheckPointDistance>BOOST_DISTANCE and self.thrust==MAX_THRUST and inside(self.nextCheckpointAngle,BOOST_ANGLE):
          self.useBoost()
          log("---*** BOOST")
          return " BOOST"
      else:
        if self.nextCheckPointDistance>BOOST_DISTANCE and self.nextCheckpointAngle==0:
          self.useBoost()
          log("---*** BOOST STARTUP")
          return " BOOST"
    return " "+str(self.thrust)

  def approcchingThrust(self,nextCheckpointAngle):
    if nextCheckpointAngle > self.targetAngle or nextCheckpointAngle < -self.targetAngle:
        self.thrust = 10
    else:
        self.thrust = MAX_THRUST

  def adaptThrustOnDistance(self,nextCheckpointDist):
    if nextCheckpointDist<(RADIUS_CHECKPOINT*1.7):
        self.thrust=int(self.thrust*0.4)
    elif nextCheckpointDist<(RADIUS_CHECKPOINT*3):
        self.thrust=int(self.thrust*0.7)
    elif nextCheckpointDist<(RADIUS_CHECKPOINT*4):
        self.thrust=int(self.thrust*0.8)
        
  def adaptThrustOnDistance2(self,nextCheckpointDist):
    # Some ideas:
    # - correct thrust based on distance and angle
    # performance erally bad after angle correction
    e=nextCheckpointDist/(RADIUS_CHECKPOINT*2.5)
    if e>1:
        e=1
    self.thrust=int(e)*self.thrust
    if not inside(self.nextCheckpointAngle,BOOST_ANGLE):
        e=(90-(abs(self.nextCheckpointAngle)))/90
        self.thrust=self.thrust*int(e)        
        
  def newDestination(self,position,nextCheckpoint):
    # we don't have a way for rotating the pod
    # TRICK: we could invent a fake position:take the line between nextCheckpoint and NextNextCheckpoint
    # then "anticipate" this new poit and use inertia for reaching nextCheckpoint
    #
    #we don't have speed to!!! But if we collect previous position and current position we can have x and y speed!
    if self.circuit.lap>2:
        x=(self.circuit.nextnextCheckpoint.x-self.circuit.lastCheckpoint.x)/4
        x=(self.circuit.nextnextCheckpoint.x-x)
        y=self.circuit.lastCheckpoint.y-500
        return nextCheckpoint
    return nextCheckpoint

  def updatePosition(self,position):
    self.previous_position=self.position
    self.position=position

  def speedCalculation(self):
    # v=s/t
    # time: one turn -> in this way speed=distance
    # Don't know if needed but this calculation could help in future

    self.speed_x=self.previous_position.x-self.position.x
    self.speed_y=self.previous_position.y-self.position.y
    self.speed=math.sqrt(self.speed_x*self.speed_x+self.speed_y*self.speed_y)

    #the angle should be equal to the one given by the server
    self.angle=math.degrees(math.atan(self.speed))

  def makeNextMove(self,x,y):
    self.updatePosition(Point(x,y))
    self.circuit.addCheckpoint(self.nextCheckpoint)
    self.approcchingThrust(self.nextCheckpointAngle)
    self.adaptThrustOnDistance(self.nextCheckPointDistance)
    self.speedCalculation()
    newdest=self.newDestination(self.position,self.nextCheckpoint)
    log(f"dist: {self.nextCheckPointDistance} - thurst:{self.thrust} - SPEED: {self.speed:.2f}- POS: {self.position} -EXPOS: {self.previous_position}")
    return print(newdest.x,newdest.y, self.tryToBoost())


circuit=Circuit()
myPod=Pod("Homundus",circuit)
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    myPod.nextCheckpointAngle=next_checkpoint_angle
    myPod.nextCheckPointDistance=next_checkpoint_dist
    myPod.nextCheckpoint=Point(next_checkpoint_x,next_checkpoint_y)
    myPod.makeNextMove(x,y)
