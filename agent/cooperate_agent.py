from .base_agent import BaseAgent

class CooperateAgent(BaseAgent):
  def __init__(self):
    super().__init__(0)

  def opt(self):
    return 1