class BaseAgent:

  def __init__(self, i=-1):
    self.i = i
    self.val = 0

  def id(self):
    return self.i
  
  def update(self, val):
    pass

  def play(self):
    return self.val

  def reset(self):
    self.val = 0