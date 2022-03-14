class BaseAgent:

  def __init__(self):
    self.val = 0
  
  def update(self, val):
    self.val = val

  def play(self):
    return self.val


class CooperateAgent(BaseAgent):

  def play(self):
    return 0

  def opt(self):
    return 1


class CopyAgent(BaseAgent):

  def opt(self):
    return 0


class DefectAgent(BaseAgent):

  def play(self):
    return 1
  
  def opt(self):
    return 1


class GrudgeAgent(BaseAgent):

  def update(self, val):
    if val == 1:
      self.val = 1
  
  def opt(self):
    if self.val == 0:
      return 0
    return 1

