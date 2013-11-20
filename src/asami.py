#!/usr/bin/python

from random import random
import numpy as np
import copy

import simulate


class Direction:
  Forward = 0
  Backward = 1

class Asami:
  T_START = 100
  Lambda = 1.0 / 30

  def __init__(self):
    self.t = 50
    self.w_a = 0
    self.w_s = 0
    self.direct = Direction.Forward

    # action model with init config
    self.actionModel = ActionModel(np.array([0, 0, 1]))
    self.actionModelInit = self.actionModel.copy()

    #self.sensorModel = SensorModel # ANSWER
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
    if self.world.s > 100 and self.direct == Direction.Forward:
      self.direct = Direction.Backward
    elif self.world.s < -100 and self.direct == Direction.Backward:
      self.direct = Direction.Forward

    if self.direct == Direction.Forward:
      return 10 * random()
    else:
      return - 10 * random()


class PolyRegressionModel:
  Gama = .99

  def __init__(self, c):
    self.c = c
    self.x = []
    self.y = []
    self.w = []

  def __getitem__(self, key):
    p = np.poly1d(self.c)
    return p(key)

  def update(self, xi, yi):
    # NON-INCREMENTAL
    self.x.append(xi)
    self.y.append(yi)
    self.w.append(1)
    self.w = [x * self.Gama for x in self.w]
    
    self.c = np.polyfit(self.x, self.y, 2, w=self.w)

  def copy(self):
    return copy.deepcopy(self)


ActionModel = PolyRegressionModel
SensorModel = PolyRegressionModel


# unit test
if __name__ == "__main__":
  a = Asami()
  log = open("log.out", 'w')

  for i in range(1000):
    a.run()
    log.write(str(a.world.s) + " " + str(a.w_s) + " " + str(a.w_a) + "\n")

  print "Action Model", a.actionModel.c
  print "Sensor Model", a.sensorModel.c
  print "End with", a.w_a, a.w_s

  log.close()
