from state import * 
import commands, core, util, pose
import time
from task import HeadBodyTask
import head, math
import PIDController as PID

def say(x):
  core.speech.say(x)
  #print x
  pass

# tolerance on angle when orienting
angle_tol = math.pi / 4

class LearnFSM(StateMachine):
  def setup(self):
    start = Node()
    finish = Node()

    scan = StandNode()
    walk = WalkToCenterNode()

    self._adt(start, N, scan)
    self._adt(scan, C, walk)
    self._adt(walk, SuccessEvent(), scan)
    self._adt(walk, FailureEvent(), scan)


class StandNode(Node):
  def __init__(self):
    super(StandNode, self).__init__()
    self.task = pose.Stand()

  def run(self):
    say("Scanning state.")
    self.task.processFrame()

    if self.getTime() > 6:
      self.postCompleted()


class WalkToCenterNode(Node):
  def __init__(self):
    super(WalkToCenterNode, self).__init__()

    self.robot = core.world_objects.getObjPtr(core.robot_state.WO_SELF)
    self.xPID = PID.PIDController(1, 0.0001, 0.0001, 10)
    self.yPID = PID.PIDController(1, 0.0001, 0.0001, 10)
    self.anglePID = PID.PIDController(1, 0.0001, 0.0001, 10)

  def clear(self):
    self.anglePID.reset()
    self.xPID.reset()
    self.yPID.reset()

  def run(self):
    say("Walking to center state.")

    x = self.robot.loc.x
    y = self.robot.loc.y
    theta = self.robot.orientation

    m_theta = math.atan2(- y, - x)
    angle_error = normalizeAngle(m_theta - theta)
    dist_error = math.sqrt(x ** 2 + y ** 2)
    x_error = dist_error * math.cos(angle_error)
    y_error = dist_error * math.sin(angle_error)

    angle = - self.anglePID.update(angle_error)
    v_x = - self.xPID.update(x_error / 150)
    v_y = - self.yPID.update(y_error / 150)

    setWalkVelocity(v_x, v_y, angle)

    if dist_error < 100:
      self.clear()
      self.postSuccess()
      self.postCompleted()

    if self.robot.height == 1: 
      self.clear()
      self.postFailure()
      self.postCompleted()


# useful functions
def normalizeAngle(angle):
  if angle > 3 * math.pi or angle < - 3 * math.pi:
    print "Weird angle"

  while angle > math.pi:
    angle -= 2 * math.pi
  while angle < -math.pi:
    angle += 2 * math.pi

  return angle

def constrainV(v):
  v = min(.5, v)
  v = max(-.3, v)
  return v

def constrainAngle(angle):
  angle = min(math.pi / 10, angle)
  angle = max(-math.pi / 10, angle)
  return angle

def setWalkVelocity(vx, vy, angle):
  commands.setWalkVelocity(constrainV(vx), constrainV(vy), constrainAngle(angle))
