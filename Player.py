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

        #for use in tracking in hunt_outcomes
        global reps
        reps = list(player_reputations)

        sorted_player_reps = sorted(player_reputations)
        hunt_decisions = []
        dictionary = {}
        matched = []
        decision = []

        #Setting the variables in round 1
        if round_number == 1:
            self.strategy = 'blank'
            self.hunt_cap = 0
            self.avg_hunts = 0
            self.tracking = False
            global total_hunts
            total_hunts = 0  
            global h
            h = 0

        #This section which results in tit for tat is run when self.tracking is set to true; the default from round 1 is false
        if self.tracking:
            print("TRACKING IN PROGRESS")
            for x in tracking_reputations:
                for y in reps:
                    if abs(x - y) < 0.001:
                        matched.append(y)
            for x in tracking_responses:
                if tracking_responses == 's':
                    decision.append('h')
                else: 
                    decision.append('s') 
            for index in range(1,len(reps)+1):
                dictionary[matched[index]] = decision[index]

        else:
            #The default decision is to always slack. These decisions are put in a dictionary.
            for rep in sorted_player_reps:
                dictionary[rep] = 's'

            if self.strategy == 'slack':
                dictionary[rep] = ['s' for rep in player_reputations]
            else:
                for rep in sorted_player_reps:
                    if rep > round_number / 75:             #hunts with an increasingly narrow range of players with high reputations
                        for r in range(1,int(self.avg_hunts+1)):         
                            dictionary[sorted_player_reps[len(sorted_player_reps)-r]] = 'h'
            
            #The final step is to transfer the reputations from the dictionary to the list "hunt_decisions" for submission
        for rep in player_reputations:
            hunt_decisions.append(dictionary[rep])

        return hunt_decisions

    def hunt_outcomes(self, food_earnings): 
        #Using food_earnings, it's possible to figure out what each player I hunted with chose to do
        successful_hunts=food_earnings.count(0)
        failed_hunts=food_earnings.count(-3)
        my_hunts=successful_hunts+failed_hunts
        
        successful_slacks=food_earnings.count(1)
        failed_slacks=food_earnings.count(-2)
        my_slacks=successful_slacks+failed_slacks

        opponents_hunt = successful_hunts + successful_slacks
        
        #If the players I hunted with hunted more often than I did, I should hunt less, specifically approximately how often they did
        if opponents_hunt > my_hunts:
            self.hunt_cap = opponents_hunt

        #When each round barely impacts reputation, I begin to track my opponents
        global total_hunts
        total_hunts += players
        global h
        h += my_hunts
        x=((h+players)/(total_hunts+players))-(h/total_hunts)
        print 'change in rep=', x 
        print 'players=', players
        print 'h=',h
        print 'total_hunts=',total_hunts
        if ((h + players)/(total_hunts+players))-(h/total_hunts) < .001:
            self.tracking = True
            print("START TRACKING NEXT ROUND")

        if self.tracking:
            global tracking_responses
            tracking_responses = []
            for food in food_earnings:
                if food == 0 or food == 1:
                    tracking_responses.append('h')
                else:
                    tracking_responses.append('s')
            global tracking_reputations
            tracking_reputations = list(reps)

    def round_end(self, award, m, number_hunters):
        #If nobody hunted in the last round, I should stop hunting
        if number_hunters == 0:
            self.strategy = 'slack'

        #This determines the average amount of times players hunted in the last round, and in the next round I set that as the cap for my hunting so that I'm not overhunting. If everyone else's reputation is very low, I don't want mine to be too much higher.
        if players > 1:
            self.avg_hunts = round(number_hunters/(players*(players-1)))
        else:
            self.avg_hunts = number_hunters/1

        if self.hunt_cap > self.avg_hunts:
            self.avg_hunts = self.hunt_cap
        