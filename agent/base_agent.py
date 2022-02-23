class BaseAgent:

  def __init__(self):
    self.val = 0
  
  def update(self, val):
    self.val = val

  def play(self):
    return self.val