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

'''
    The payoff matrix for each hunt is as follows:
    
    ___|____H____|____S____|
    _h_|_(0,0)___|_(-3,1)__|
    _s_|_(1,-3)__|_(-2,-2)_|
    
    A quick game theory analysis shows that the Nash equilibrium for
    each hunt is for both players to slack. Therefore, it would seem
    that the optimal strategy is to always slack. 

    Although it may seem the public goods bonus might encourage
    hunting, the public goods bonus shouldn't really be incorporated
    into a strategy because it benefits everyone equally, and even
    if a strategy is simply trying to survive, extra hunting, to make
    the bonus more likely, simply allows other players to take
    advantage. However, extra hunting does have an advantage in that
    it increases reputation, and we will come back to that later.
    
    A little thinking can show that if two players both hunt with
    only each other, then they can win against any number of players 
    that only slack. In this manner, if a player can find another
    player to cooperate with (or more), that player could potentially
    fare well in the competition. One problem with this is that it
    would be hard to keep track of this player, and harder yet to
    determine if this player is actually cooperating, or if they are
    slacking with you and taking advantage.

    Therefore, I have decided that the most feasible player that does
    not require a lot of work would be one that always slacks.
    However, I suspect others will submit a player that always
    slacks, and mine would need to have an advantage over them. I
    tried to make a player that will find others to hunt with, and
    convince others to hunt with me.

    In the beginning, my player will boost its reputation by hunting
    more than it does later on, but I would prefer to hunt with those
    who hunt back, such that my disadvantages are not too large. I
    set a changing 'cutoff' such that I will only hunt with those
    above this cutoff. After 63 turns, I never hunt with anyone. The
    change in the cutoff, 0.016, was chosen by testing different
    values using Chad Miller's test engine. My player wins against
    the test bots, and other players I wrote.

    I see that if someone incorporates tracking successfully, and, if 
    in the competition, they successfully manage to find a hunting
    parter, my player would suffer. However, it would be difficult
    for me to do so, with time limitations. I must rely on either
    it proving difficult for others as well, or other players taking
    advantage of their hunting partners. I try to go for both victory
    and survival, and don't try to focus on one.

    In summary, after some thinking and analysis, I decided to have
    my player do the following:

    1) Hunt with those above an increasing cutoff for the first few
       turns.

       This serves to increase reputation, such that others decide to
       hunt with me later on, when it matter. I rely on the
       difficulty of determining whether I cooperated with them.

    2) Never hunt after that.

       This is due to the fact that the dominant strategy for this
       game is to never hunt. However, if some player decides to hunt
       with me, this will give me an advantage over other players.
'''

class Test(BasePlayer):
    """OOP player implementation"""
    def hunt_choices(self,round_number,current_food,current_reputation,m,player_reputations):
        decisions=[]                     # strategy is the list of hunting decisions
        for x in player_reputations:
            if x>(round_number-1)*0.016: # only hunt with those with high reputation
                decisions.append('h')
            else:
                decisions.append('s')
        return decisions

    def hunt_outcomes(self, food_earnings):
        pass

    def round_end(self, award, m, number_hunters):
        pass