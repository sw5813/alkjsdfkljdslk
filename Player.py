# This file is intended to be a final submission. python tester.py Player.py
# should work at all times. If it does not, there is a bug.
# If you're just trying to test a solution, scroll down to the Player
# class.

# This file is intended to be in the same format as a valid solution, so
# that users can edit their solution into Player and then submit just this
# file to the contest. If you see any reason this would not work, please submit
# an Issue to https://github.com/ChadAMiller/hungergames/issues or email me.

# You can see more sample player classes in bots.py

class BasePlayer(object):
    '''
    Base class so I don't have to repeat bookkeeping stuff.
    Do not edit unless you're working on the simulation.
    '''
    
    def __str__(self):
        try:
            return self.name
        except AttributeError:
            # Fall back on Python default
            return super(BasePlayer, self).__repr__()
    
    def hunt_choices(*args, **kwargs):
        raise NotImplementedError("You must define a strategy!")
        
    def hunt_outcomes(*args, **kwargs):
        pass
        
    def round_end(*args, **kwargs):
        pass


class Player(BasePlayer):
    '''
    Your strategy starts here.
    '''
    def __init__(self):
        self.name = "MEEEEE"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        '''Required function defined in the rules'''

        if round_number < 100:
            hunt_decisions = []
            for x in player_reputations:
                if x>(round_number-1)*0.016: # only hunt with those with high reputation
                    hunt_decisions.append('h')
            else:
                    hunt_decisions.append('s')
            return hunt_decisions
        else:
            avg_rep = sum(player_reputations) / float(len(player_reputations))
            huntquota = round(avg_rep * float(len(player_reputations))) 
            hunts = len(player_reputations)
            sorted_player_reps = sorted(player_reputations)
            remainder = list(sorted_player_reps)
            dictionary = {}
            
            for rep in sorted_player_reps:
                if rep >= 0.9 or rep < 0.5:
                    dictionary[rep] = 's'
                    remainder.remove(rep)
            
            last = list(remainder)
            
            for r in range(1,int(huntquota+1)):
                if huntquota < len(last):
                    dictionary[remainder[len(remainder)-r]] = 'h'
                    last.remove(remainder[len(remainder)-r])
                else:
                    for x in last:
                        dictionary[x] = 'h'
                        last.remove(x)

            if last:
                for x in last:
                    dictionary[x] = 's'
            
            hunt_decisions = []

            for rep in player_reputations:
                hunt_decisions.append(dictionary[rep])

            return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        '''Required function defined in the rules'''
        pass
        

    def round_end(self, award, m, number_hunters):
        '''Required function defined in the rules'''
        pass
        