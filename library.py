import datetime
import BeautifulSoup 

#date format sample: 13 April 2015 02:43AM
def getDate():
    return str(datetime.datetime.now().strftime('%d %B %Y %I:%M%p'))


#given the dicts of player status of format dict[player] -> human | zombie | OZ
#returns a string summarizing changes,count of humans, count of zombies
#(including OZ in zombie populations)
def compareDict(old_dict,new_dict):
    joining_human = []
    joining_zombie = []
    dying = []
    revived = []
    revealed_OZs = []
    removed = []
    human_count = 0
    zombie_count = 0

    for player in new_dict:
        if new_dict[player] == 'human':
            human_count+=1   
        elif new_dict[player] == 'zombie' or new_dict[player] == 'OZ':
            zombie_count+=1   
        else:
            raise ValueError('Unknown status of player '+player+': '+new_dict[player])

        if (player not in old_dict.keys()):#new player joining
            if new_dict[player] == 'human':
                joining_human.append(player)
            elif new_dict[player] == 'zombie' or new_dict[player] == 'OZ':
                joining_zombie.append(player)
            else:
                print 'strange status of player '+player+': '+new_dict[player]

        elif new_dict[player] == old_dict[player]:#no change, most common case
            continue
        elif (new_dict[player]=='zombie' and old_dict[player]=='human'):#dead 
            dying.append(player)
        elif (new_dict[player]=='human' and old_dict[player]=='zombie'):#revived
            revived.append(player)
        elif (new_dict[player]=='OZ' and old_dict[player]=='human'):#reveal OZ
            revealed_OZs.append(player)
        elif (new_dict[player]=='OZ' and old_dict[player]=='zombie'):#timout OZ
            revealed_OZs.append(player)
        else:
            print 'unable to process '+player+':'+old_dict[player]+'->'+new_dict[player]

    for player in old_dict:
        if player not in new_dict:
            removed.append(player)

    #return the results of the diff
    result = ''
    if (len(joining_human)>0):
        result += 'Joining as human: '+(', '.join(joining_human))+' '
    if (len(joining_zombie)>0):
        result += 'Joining as zombie: '+(', '.join(joining_zombie))+' '
    if (len(dying)>0):
        result += 'Dying: '+(', '.join(dying))+' '
    if (len(revived)>0):
        result += 'Revived: '+(', '.join(revived))+' '
    if (len(revealed_OZs)>0):
        result += 'Revealed OZ: '+(', '.join(revealed_OZs))+' '
    if (len(removed)>0):
        result += 'Removed: '+(', '.join(removed))+' '
    
    return result.strip(), human_count, zombie_count

