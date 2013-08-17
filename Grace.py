# This file is intended to be a final submission. python tester.py Player.py
# should work at all times. If it does not, there is a bug.
# If you're just trying to test a solution, scroll down to the Player
# class.

# This file is intended to be in the same format as a valid solution, so
# that users can edit their solution into Player and then submit just this
# file to the contest. If you see any reason this would not work, please submit
# an Issue to https://github.com/ChadAMiller/hungergames/issues or email me.

# You can see more sample player classes in bots.py

import random

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


class Grace(BasePlayer):
    '''
    Your strategy starts here.
    '''
    def __init__(self):
        self.name = "GRACE"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        '''Required function defined in the rules'''
        if round_number==1:
            total_pos_hunts=0
            total_hunts=0
            determine_hunting_limit=0
            switch=0
            p=1
            freeloaders=0
        global total_pos_hunts
        global total_hunts
        global determine_hunting_limit
        global switch
        global p
        global average
        global freeloaders
        #First, we will calculate the average reputation ignoring ourself

        #We want to count the number of freeloaders because if the game is all freeloaders,
        #there's no point in calculating the average and we will also become a freeloader
        if freeloaders>-1:
            freeloaders=0
            for i in player_reputations:
                if i==0:
                    freeloaders=freeloaders+1
        else:   #Also, if in the previous round everyone slacked w/ us,
            freeloaders=len(player_reputations) #we will treat everyone like freeloaders and always slack
        

        average=0
        hunt_decisions=[]
        people_to_hunt_with=[]

        our_reputation=0
        if total_pos_hunts>0:
            our_reputation=total_hunts/total_pos_hunts

        if (len(player_reputations)-freeloaders)>0:
            average=(sum(player_reputations)-our_reputation)/(len(player_reputations)-1)
            needed_hunts=average*(total_pos_hunts+len(player_reputations))-total_hunts
            needed_hunts=int(needed_hunts)+1
            
            #It seems like a bad idea to just hunt with all possible players to increase reputation
            #We have multiple methods to determine what hunting cap we'll use
            #The value of the variable determine_hunting_limit determines which method we'll use

            #So long as people are willing to hunt with us, slacking is always a good idea,
            #so it's possible we won't hunt with anyone.
            #Because slacking is beneficial, rather than focusing on building reputation, we will try to
            #slack as much as we can get away with

            #if something goes wrong w/ the code, the default will be to always slack
            hunting_limit=0

            #If we realize that we're running out of food, it's better to slack more than to risk hunting more

            if current_food<200 and determine_hunting_limit>1:
                determine_hunting_limit=0

            #We have the option of hunting a below or equal to average amount
            #The actual amount we in between the average and 0 amount is in incriments of 10%
            #This will happen for determine_hunting_limit from 0-10

            if determine_hunting_limit<=10:
                hunting_limit=average*.1*determine_hunting_limit*len(player_reputations)

            #Of course, to build reputation, it is necessary to hunt an above average amount.
            #It's best to never hunt more than the maximum player reputation since that would cause too many losses
            #So again in incriments of 10%, we also have the option to hunt some amount between the average and maximum player reputation
            #This will happen for determine_hunting limit from 11 to 20(the subtract 10 below is so the 10% increments work out)
            
            elif determine_hunting_limit<=20:
                amount_above_average=(max(player_reputations)-average)*.1*(determine_hunting_limit-10)
                hunting_limit=(average+amount_above_average)*len(player_reputations)

            #If we need more hunts to raise our reputation than the hunting cap, we hunt the cap number of hunts    
            if needed_hunts>hunting_limit:
                needed_hunts=int(hunting_limit)

            #Next, we make a copy of player_reputations and remove all the freeloaders and people that always hunt
            player_reputation_copy=[]
            for x in player_reputations:
                player_reputation_copy.append(x)
            player_reputation_copy.sort()
            while player_reputation_copy[0]==0:
                player_reputation_copy.remove(0)
            player_reputation_copy.reverse()
            while player_reputation_copy[0]==1:
                player_reputation_copy.remove(1)
            player_reputation_copy.sort() #player reputations will be smallest to largest


            #One theory we have is that some people will build reputation and then start slacking.
            #Based on that, we shouldn't always just hunt with the highest reputations by default
            #p determines what is the maximum reputation player we will hunt with.
            #when things don't go right and most of the time we end up hunting with slackers switch becomes 1 (see next funciton of the game)
            #and percent is a new random number. 70% is an arbitary threashold
            if switch==1:
                while p<.70:
                    p=random.random()
                switch=0
                    
            #if we need more hunts to maintain our reputation than people who aren't freeloaders or always hunters, we'll hunt with everyone availible
            if len(player_reputation_copy)<=needed_hunts:
                for rep in player_reputations:
                    if rep==0 or rep==1:
                        hunt_decisions.append('s')
                    else:
                        hunt_decisions.append('h')

            #Otherwise, starting with the p percent reputation, we decrease in reputation and add all the reputations
            #of people we will hunt with to the list "people_to_hunt_with"
            else:
                index=int(p*(len(player_reputation_copy)-1))
                while index>-1:
                    people_to_hunt_with.append(player_reputation_copy[index])
                    index=index-1
                    if len(people_to_hunt_with)>=needed_hunts:
                        break
                if needed_hunts==0:
                    people_to_hunt_with=[]

                #now we form the list hunt_decisions and hunt with all the reputations in people_to_hunt_with
                for rep in player_reputations:
                    if rep==0 or rep==1:
                        hunt_decisions.append('s')
                    elif rep in people_to_hunt_with:
                        hunt_decisions.append('h')
                    else:
                        hunt_decisions.append('s')

            #Finally, we update our total possible hunt and total hunt count so we can calculate our own reputation
            #and how many people we need to hunt with to maintain the average

            total_pos_hunts=total_pos_hunts+len(hunt_decisions)
            total_hunts=total_hunts+hunt_decisions.count('h')
                
        else: #if everyone is a freeloader, slack all the time
            for rep in player_reputations:
                hunt_decisions.append('s')
                total_pos_hunts=total_pos_hunts+1

        if round_number==1: #In the first round, we'll go for a reputation of 50%
            hunt_decisions=[]
            for rep in player_reputations:
                x=random.random()
                if x<.5:
                    hunt_decisions.append("s")
                else:
                    hunt_decisions.append("h")
                    
        return hunt_decisions
        

    def hunt_outcomes(self, food_earnings):
        '''Required function defined in the rules'''

        global determine_hunting_limit
        global switch
        global freeloaders

        sucessful_hunts=food_earnings.count(0)
        failed_hunts=food_earnings.count(-3)
        times_hunted=sucessful_hunts+failed_hunts
        
        sucessful_slack=food_earnings.count(1)
        failed_slack=food_earnings.count(-2)
        times_slack=sucessful_slack+failed_slack

        #If everyone slacked with us in the last round, we will also slack w/ everyone
        if sucessful_hunts+sucessful_slack==0:
            freeloaders=-1
            determine_hunting_limit=0

        counter=0
        
        #If we find that we're often hunting with slackers, we should change who
        #we're hunting with or hunt less often
        #If we realize that it would be more beneficial to freeload than to hunt with the people we hunted with,
        #or that our hunts are less sucessful than the average, we definitely need to hunt less or with different people

        if (-3*failed_hunts)<(-2*times_hunted*(1-average)) or sucessful_hunts<average*times_hunted:    
            if determine_hunting_limit in range(1,21):
                determine_hunting_limit=determine_hunting_limit-1
                counter=1
            elif determine_hunting_limit==0:
                switch=1
        
        #If we find that the people we're slacking with are also slackers, we should probably raise
        #our reputation and slack less or change who we're slacking with

        if sucessful_slack<average*(times_slack-freeloaders):
            if determine_hunting_limit in range(0,20):
                determine_hunting_limit=determine_hunting_limit+1
                if counter==1:
                    switch=1
            elif determine_hunting_limit==4:
                switch=1
                
    def round_end(self, award, m, number_hunters):
        '''Required function defined in the rules'''

        #not sure what to do about m, since it doesn't seem like we'll affect it much
        pass
        
