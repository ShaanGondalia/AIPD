class BaseAgent:

  def __init__(self, i=-1):
    self.i = i
    self.prev_val = 0
    self.val = 0

  def id(self):
    return self.i
  
  def update(self, val):
    pass

  def play(self):
    self.prev_val = self.val
    return self.val

  def previous(self):
    return self.prev_val