import sys
import math


RADIUS_CHECKPOINT=600
RADIUS_POD=400
MAX_THRUST=100

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
    self.checkpoints=[]

  def addCheckpoint(self,checkpoint):
    if any(p==checkpoint for p in self.checkpoints):
      if checkpoint==self.firstCheckpoint:
        self.lap=self.lap+1
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
    self.thrust=MAX_THRUST
    self.boost=0
    self.targetAngle=90

  def isBoostAvailable(self):
    if self.boost==0:
      return True
    return False

  def useBoost(self):
    self.boost +=1

  def tryToBoost(self,nextCheckpoint):
    if self.isBoostAvailable():
      # PAOLO: insert here the boost logic
      if self.circuit.lap>1:
        self.useBoost()
        return " BOOST"
    return " "+str(self.thrust)

  def approcchingThrust(self,nextCheckpointAngle):
    if nextCheckpointAngle > self.targetAngle or nextCheckpointAngle < -self.targetAngle:
        self.thrust = 10
    else:
        self.thrust = MAX_THRUST

  def adaptThrustOnDistance(self,nextCheckpointDist):
    if nextCheckpointDist<(RADIUS_CHECKPOINT*1.7):
        self.thrust=int(thrust*0.4)
    elif nextCheckpointDist<(RADIUS_CHECKPOINT*3):
        self.thrust=int(thrust*0.7)
    elif nextCheckpointDist<(RADIUS_CHECKPOINT*4):
        self.thrust=int(thrust*0.8)   

  def makeNextMove(self,nextCheckpoint,nextCheckpointAngle,nextCheckPointDistance,circuit):
    self.circuit.addCheckpoint(nextCheckpoint)
    self.approcchingThrust(nextCheckpointAngle)
    self.adaptThrustOnDistance(self.position.distance(nextCheckpoint))
    return print(nextCheckpoint.x,nextCheckpoint.y, self.tryToBoost(nextCheckpoint))
    
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

    nextCheckpoint=Point(next_checkpoint_x,next_checkpoint_y)
    myPod.makeNextMove(nextCheckpoint,next_checkpoint_angle,next_checkpoint_dist,circuit)
