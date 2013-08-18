class BasePlayer(object):
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
        global players
        players = len(player_reputations)

        sorted_player_reps = sorted(player_reputations)
        hunt_decisions = []
        dictionary = {}
        global tracking_dict
        tracking_dict = {}  
        location = {}

        if round_number == 1:
            self.strategy = 'blank'
            self.hunt_cap = 0
            self.avg_hunts = 0
            self.tracking = False
            global total_hunts
            total_hunts = 0  
            global h
            h = 0

        if self.tracking:
            print("TRACKING IN PROGRESS: PLAYER REPUTATIONS")
            index = 1
            for rep in player_reputations:
                tracking_dict[index] = rep
                index += 1
            for x in range(1, len(tracking_dict)+1):
                for y in range(1, len(tracking_dict_copy)+1):
                    if tracking_dict_copy[y] == tracking_dict[x]:
                        location[y] = tracking_dict[x]

        for rep in sorted_player_reps:
            dictionary[rep] = 's'

        if self.strategy == 'slack':
            dictionary[rep] = ['s' for rep in player_reputations]
        else:
            for rep in sorted_player_reps:
                if rep > round_number / 75:
                    for r in range(1,int(self.avg_hunts+1)):         
                        dictionary[sorted_player_reps[len(sorted_player_reps)-r]] = 'h'
        
        for rep in player_reputations:
            hunt_decisions.append(dictionary[rep])

        return hunt_decisions

    def hunt_outcomes(self, food_earnings): #IMPLEMENT HUNT_CAP
        tracking_dict2 = {}

        successful_hunts=food_earnings.count(0)
        failed_hunts=food_earnings.count(-3)
        my_hunts=successful_hunts+failed_hunts
        
        successful_slacks=food_earnings.count(1)
        failed_slacks=food_earnings.count(-2)
        my_slacks=successful_slacks+failed_slacks

        opponents_hunt = successful_hunts + successful_slacks
        
        if opponents_hunt > my_hunts:
            self.hunt_cap = opponents_hunt

        global total_hunts
        total_hunts += players
        print(total_hunts)
        global h
        h += my_hunts
        print(h)
        if (h+players)/(total_hunts+players)-h/total_hunts<.001:
            self.tracking = True

        if self.tracking:
            index = 1
            for food in food_earnings:
                if food == 0 or food == 1:
                    tracking_dict2[index] = 'h'
                else:
                    tracking_dict2[index] = 's'
                index += 1
            global tracking_dict_copy
            tracking_dict_copy = dict(tracking_dict)
            print("TRACKING: OPPONENT REPUTATIONS")
            print tracking_dict_copy
            print("TRACKING: OPPONENT ACTION")
            print(tracking_dict2)

    def round_end(self, award, m, number_hunters):
        if number_hunters == 0:
            self.strategy = 'slack'

        if players > 1:
            self.avg_hunts = round(number_hunters/(players*(players-1)))
        else:
            self.avg_hunts = number_hunters/1

        if self.hunt_cap > self.avg_hunts:
            self.avg_hunts = self.hunt_cap
        