from random import random
import numpy
import copy

import simulate

class Asami:
  T_START = 10
  Lambda = .1

  def __init__(self):
    self.t = 0
    self.w_a = 0
    self.w_s = 0

    # action model with init config
    self.actionModel = ActionModel([0, .01, 0])
    self.actionModelInit = self.actionModel.copy()

    self.sensorModel = SensorModel([0, 0, 0])

    self.world = simulate.Simulator()

  def run(self):
    action = self.__getAction()
    self.world.act(action)
    obs = self.world.observe()

    if self.t < 2 * self.T_START:
      self.w_a += self.actionModelInit[action]
    else:
      self.w_a += self.actionModel[action]

    if self.t > self.T_START:
      old_w_s = self.w_s
      self.w_s = self.sensorModel(obs)
      self.actionModel.update(action, self.w_s - old_w_s)

      self.w_a = (1 - Lambda) * self.w_a + Lambda * self.w_s

    self.sensorModel.update(obs, self.w_a)

  # action range : [-10, 10]
  def __getAction(self):
    # naive
    return 20 * random() - 10


class PolyRegressionModel:
  def __init__(self, c):
    self.c = c
    self.x = []
    self.y = []

  def __getitem__(self, key):
    retVal = 0
    for i in range(len(self.c)):
      xi = key ** i
      retVal += xi * self.c[i]

    return retVal

  def update(self, xi, yi):
    # NON-INCREMENTAL
    self.x.append(xi)
    self.y.append(yi)

    self.c = numpy.polyfit(self.x, self.y, 2)

  def copy(self):
    return copy.deepcopy(self)


ActionModel = PolyRegressionModel
SensorModel = PolyRegressionModel


# unit test
if __name__ == "__main__":
  a = Asami()
  a.run()
