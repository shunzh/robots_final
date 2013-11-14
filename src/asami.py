from random import random

class Asami:
  T_START = 10
  Lambda = .1

  def __init__(self):
    self.t = 0
    self.w_a = 0
    self.w_s = 0
    # content are (act, obs) tuples
    self.history = []

  def run(self):
    if self.t < 2 * self.T_START:
      w_a += actionModel_0(action)     
    else:
      w_a += actionModel(action)     

    if self.t > self.T_START:
      w_s = sensorModel(obs)
      updateActionModel(action, w_s)
      w_a = (1 - Lambda) * w_a + Lambda * w_s

    updateSensorModel(obs, w_a)

  # action range : [-10, 10]
  def getAction(self):
    # naive
    return 20 * random() - 10


# experience
class Experience:
  def __init__(self, act, obs):
    self.act = act
    self.obs = obs


class ActionModel:
