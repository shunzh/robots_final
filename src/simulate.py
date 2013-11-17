import math, numpy

class Simulator:
  DEG_T_RAD = math.pi / 180
  # same as Nao
  FOVx = DEG_T_RAD * 60.97
  FOVy = DEG_T_RAD * 47.64
  canvasHeight = 240.0
  worldHeight = 200.0

  def __init__(self):
    # assume starting position
    self.s = 0
    self.beaconPos = 1000
    self.cameraHeight = 240

  def act(self, action):
    if action > 10 or action < -10:
      raise Exception("Invalid action" + str(action))
      return None

    self.s += self.__getV(action)
  
  # velocity = action / 10, action \in [-10, 10]
  def __getV(self, action):
    return 1.0 * action / 10

  # get the number of pixels would be observed
  def observe(self):
    dist = self.beaconPos - self.s
    tanValue = self.worldHeight / 2 / dist
    theta = 2 * numpy.arctan(tanValue)
    return theta * self.canvasHeight / self.FOVy

# unit test
if __name__ == "__main__":
  s = Simulator()
  for i in range(800):
    s.act(10)
    print s.s, s.observe()
