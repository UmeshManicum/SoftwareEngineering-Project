from App.models import state
from .state import *

class NoChange(State):
    __tablename__='no_change'

    #def __init__(self, ranking):
    #    self.ranking = ranking

    def notify(self, student_id, curr_ranking, prev_ranking):
        return None
        #return("No Change State")
