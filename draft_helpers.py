# draft_helpers.py>

def printTable(table):
    '''A simple way to display matrices in a more readable format'''
    for i in table:
        print(i)
        
def evaluate_util(player_row):
    if players[player_row -1][4] == True:
        restOfROI_main_role = combos[(centers - 1, wings, defenders, goalies, utils)][player_row - 1][budget_interval - players[player_row - 1][1]]
        restOfROI_util = combos[(centers, wings, defenders, goalies, utils - 1)][player_row - 1][budget_interval - players[player_row - 1][1]]
 
def get_optimal_set(players_list, budget, inc, limits):
    
    ## first we divide all working money sums by the increment
    
    players = [[player[0], int(int(player[1])/inc), player[2], player[3]] for player in players_list]
    
    budget = int(budget / inc)
    #for player in players:
    #    player[1] = int(int(player[1]) / inc)

        
    nPlayers = len(players) 
    
    combos = {}
    combos_traceback = {}
    
    for centers in range(limits["C"] + 1):
        for wings in range(limits["W"] + 1):
            for defenders in range(limits["D"] + 1):
                for goalies in range(limits["G"] + 1):
                    combos[(centers, wings, defenders, goalies)] = [[-1 for i in range(budget + 1)] for i in range(nPlayers + 1)]
                    combos_traceback[(centers, wings, defenders, goalies)] = [[None for i in range(budget + 1)] for i in range(nPlayers + 1)]
                
                
    ## First, fill in the base case for 0 forwards, defenders, and goalies
    combos[(0,0,0)] = [[-0 for i in range(budget + 1)] for i in range(nPlayers + 1)]
    
    ## Now we iterate through the combinations of forwards, defenders, and goalies
    for centers in range(limits["C"] + 1):
        for wings in range(limits["W"] + 1):
            for defenders in range(limits["D"] + 1):
                for goalies in range(limits["G"] + 1):
                
                
                    roster_limits = {"C":centers,"W": wings ,"D":defenders ,"G": goalies}
                    table = combos[(centers, wings, defenders, goalies)]
                    traceback = combos_traceback[(centers, wings, defenders, goalies)]
                
                    ## Filling in the base case for 0 players to choose from
                    for i in range(budget + 1):
                        table[0][i] = 0
                    
                    ## Now we incrememnt through each player
                    for player_row in range(1, nPlayers + 1):
                    
                        ## For each player, we increment through our budget
                        for budget_interval in range(budget + 1):
                        
                            ##For each acceptable player, we see if we can afford the player and if we have roster space
                            player_position = players[player_row -1][3]
                            if roster_limits[player_position] > 0 and budget_interval >= players[player_row - 1][1]:
                    
                    
                                ## We calculate the points
                                points = players[player_row - 1][2]
                        
                                ## We look through previous dictionarys to find the rest of the ROI
                                if player_position == "C":
                                    restOfROI = combos[(centers - 1, wings, defenders, goalies)][player_row - 1][budget_interval - players[player_row - 1][1]]
                                elif player_position == "W":
                                    restOfROI = combos[(centers, wings -1 , defenders, goalies)][player_row - 1][budget_interval - players[player_row - 1][1]]
                                elif player_position == "D":
                                    restOfROI = combos[(centers, wings, defenders - 1, goalies)][player_row - 1][budget_interval - players[player_row - 1][1]]
                                elif player_position == "G":
                                    restOfROI = combos[(centers, wings, defenders, goalies - 1)][player_row - 1][budget_interval - players[player_row - 1][1]]
                                
                                        
                                ## We compare it for the optimal value if we dont sign the player
                                noSign = table[player_row - 1][budget_interval]
                
                                ## if signing the player generates more profit than not signing the player, then we add him to the table
                                if points + restOfROI > noSign:
                                    table[player_row][budget_interval] = points + restOfROI
                                    traceback[player_row][budget_interval] = True
                                
                                else:
                                    table[player_row][budget_interval] = noSign
                                    traceback[player_row][budget_interval] = False
                                
                            ## if we cant afford the player or have roster room, we treat it as a noSign
                            else:
                                table[player_row][budget_interval] = table[player_row - 1][budget_interval]
                                traceback[player_row][budget_interval] = False
                            
    ## To return the optimized investment portfolio, we create an empty return list
    ## and initialize our item marker value, and a money iteration value
    ret_list = []
    val = nPlayers
    i = -1
    centers = limits["C"]
    wings = limits["W"]
    defenders = limits["D"]
    goalies = limits["G"]
    
    ## we loop through our table until our value (signifying the current item) is at 0
    while val > 0:
        
        ## If our traceback table tells us to buy the investment
        if combos_traceback[(centers, wings, defenders, goalies )][val][i]:
            
            ## We record the player position
            player_position = players[val - 1][3]
            
            ## We add our investment number, cost, and ROI to our output list
            ret_list.append((players[val - 1][0], players[val - 1][1] * inc, players[val - 1][2], players[val - 1][3]))
                            
            ## We increment our money iteration value backwards by the amount that we "spent" on the investment
            ## And increment our item marker value back by 1
            ## and incrememnt back the roster space
            i -= players[val - 1][1]
            val -= 1
            
            if player_position == "C":
                centers -= 1
            if player_position == "W":
                wings -= 1    
            if player_position == "D":
                defenders -= 1
            elif player_position == "G":
                goalies -= 1

        
        ## If our traceback table tells us to not buy the investment,
        ## we simply increment our item marker value back by 1
        else:
            val -= 1
    
    
    return ret_list#, combos, combos_traceback
  

def get_player_info(players, target):
    for player in players:
        if player[0] == target:
            return(player)
            
def draft_from_middle(players, already_selected, players_taken_by_other, budget, inc, limits):
    
    for selected_player in already_selected:
        player_info = get_player_info(players, selected_player)
        budget = budget - player_info[1]
        limits[player_info[3]] -= 1
    
    
    remaining_players = [player for player in players if player[0] not in players_taken_by_other]    
        
    remaining_players = [player for player in remaining_players if player[0] not in already_selected]    
    
    remaining_draft = get_optimal_set(remaining_players, budget, inc, limits)
    
    for already_selected_player in already_selected:
        remaining_draft += [get_player_info(players, already_selected_player)]
    
    return remaining_draft
    