from .base_agent import BaseAgent

class CooperateAgent(BaseAgent):
  def __init__(self, id):
    super().__init__(id)

  def opt(self):
    return 1