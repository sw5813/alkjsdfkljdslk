player_reputations = [1,0.1,0.2,0.7,0.33,0.23,0.9,0]

#find the average reputation 
avg_rep = sum(player_reputations) / float(len(player_reputations))

#the hunt quota is the number of hunts the player needs to do in order to meet the average reputation
huntquota = round(avg_rep * float(len(player_reputations)))

#create several copies of player_reputations to manipulate
sorted_player_reps = sorted(player_reputations)
remainder = list(sorted_player_reps)

#This currently empty dictionary will be used to record each decision
dictionary = {}

#Slacks with all the people with reputations greater than or equal to 0.9 and less than or equal to 0.1
for rep in sorted_player_reps:
    if rep >= 0.9 or rep < 0.5:
        dictionary[rep] = 's'
        remainder.remove(rep)
        
print(remainder)
print(dictionary)

last = list(remainder)

#hunts with the highest remaining members in order to meet huntquota. If there aren't enough people, hunt with them all.
for r in range(1,int(huntquota+1)):
    if huntquota < len(last):
        dictionary[remainder[len(remainder)-r]] = 'h'
        last.remove(remainder[len(remainder)-r])
    else:
        for x in last:
            dictionary[x] = 'h'
            last.remove(x)

print(last)
print(dictionary)

#If there are still people remaining, slack.
if last:
    for x in last:
        dictionary[x] = 's'
        
print(dictionary)

for rep in player_reputations:
    print(rep, dictionary[rep])

#return [dictionary[rep] for rep in player_reputations]

hunt_decisions = []

for rep in player_reputations:
    hunt_decisions.append(dictionary[rep])

print hunt_decisions
