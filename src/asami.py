#!/usr/bin/python

from random import random
import numpy as np
import copy

import simulate

class Asami:
  T_START = 5
  Lambda = .1

  def __init__(self):
    self.t = 50
    self.w_a = 0
    self.w_s = 0

    # action model with init config
    #self.actionModel = ActionModel(np.array([0, .1, 0]))
    self.actionModel = ActionModel(np.array([0, 0.001, 0]))
    self.actionModelInit = self.actionModel.copy()

    #self.sensorModel = SensorModel(np.array([-1.9135e-01, 4.0880e+01, -1.7393e+03]))
    self.sensorModel = SensorModel(np.array([0, 0, 0]))

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
      self.w_s = self.sensorModel[obs]
      self.actionModel.update(action, self.w_s - old_w_s)

      self.w_a = (1 - self.Lambda) * self.w_a + self.Lambda * self.w_s

    self.sensorModel.update(obs, self.w_a)

    self.t += 1

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
    p = np.poly1d(self.c)
    return p(key)

  def update(self, xi, yi):
    # NON-INCREMENTAL
    self.x.append(xi)
    self.y.append(yi)

    self.c = np.polyfit(self.x, self.y, 2)
    print "got ", self.c

  def copy(self):
    return copy.deepcopy(self)


ActionModel = PolyRegressionModel
SensorModel = PolyRegressionModel


# unit test
if __name__ == "__main__":
  a = Asami()
  for i in range(500):
    a.run()
    print "Iteration #", i
    print "w_a", a.w_a
    print "w_s", a.w_s
    print "Action Model", a.actionModel.c
    print "Sensor Model", a.sensorModel.c
