def clean_dk_data(file):
        
    ## REad in the file
    players_df = pd.read_csv(file)
    
    ## Get the position name and drop non essential columns
    players_df["Position"] = players_df["Roster Position"].str[0]
    players_df = players_df.drop(columns=["Name + ID","ID","Game Info","TeamAbbrev", "Roster Position"])
    
    ## Convert the dataframe into a list of lists
    data_for_algo = players_df[["Name", "Salary", "AvgPointsPerGame", "Position"]].values.tolist()
    
    ## print an example row and return the nested list
    print('example entry:', data_for_algo[0])
    
    return data_for_algo


def get_optimal_set(players_list, budget, inc, limits):
    '''Uses a Dynamic Programming Algorithm to get the maximum number of points scored on a fantasy hockey team,
    constrained by salary cap (budget) and limits on positions (only 3 centers, 2 wings, etc.)'''
    
    ## inputs
    # players_list--a list of lists: player name, salary, expected points, position--ex:['Nathan MacKinnon', 9000, 14.94, 'C']
    # budget -- a total budget/salary cap--ex:50000
    # inc -- an increment that you go up/down by when you use the algorithm--ex:100 
    # limits -- a dictionary of constraints for each position--ex:{"C": 2,"W": 3 ,"D" : 2,"G": 1}
    
    
    ## first we divide all working money sums by the increment
    ## This allows us to control the granularity of the algorith
    players = [[player[0], int(int(player[1])/inc), player[2], player[3]] for player in players_list]
    budget = int(budget / inc)


    ## we get our number of players and create dictionaries for our combo table and our combo traceback table
    nPlayers = len(players) 
    combos = {}
    combos_traceback = {}
    
    ## A cassic napsack problem is only measuring 2 variables (weight and value), making it a nested list solution
    ## since this has a limitation of how many of each positions you can have, we are making a nest list solution
    ## for every possible combination of position limits
    
    ## We iterate through every possible combination of centers, wings, defenders, and goalies
    for centers in range(limits["C"] + 1):
        for wings in range(limits["W"] + 1):
            for defenders in range(limits["D"] + 1):
                for goalies in range(limits["G"] + 1):
                    
                    ## For each combination, we initialize a list of lists of placeholder values                 
                    combos[(centers, wings, defenders, goalies)] = [[-1 for i in range(budget + 1)] for i in range(nPlayers + 1)]
                    combos_traceback[(centers, wings, defenders, goalies)] = [[None for i in range(budget + 1)] for i in range(nPlayers + 1)]

                    
    ## Now that we have created players/budget tables for each combination of positions,
    ## we iterate through through each combination to start calculating our best draft option    
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
                        
                        player_cost = players[player_row - 1][1]
                        player_points = players[player_row - 1][2]
                        player_position = players[player_row -1][3]
                        
                        
                        ## For each player, we increment through our budget
                        for budget_interval in range(budget + 1):
                        
                            ##For each acceptable player, we see if we can afford the player and if we have roster space
                            if roster_limits[player_position] > 0 and budget_interval >= player_cost:
                                
                                
                                ## To determine if we want to select a player or not, we find the higher value between:
                                ## The ROI of the player + the optimized ROI of our remaining budget and available positions
                                ## The ROI of not selecting the player
                                
                                ## Since these are tables of previously filled in dictionaries,
                                ## We just have to go to the right player limit combination, player row, and budget interval
                                ## to get the already-calculated optimized ROI
                                if player_position == "C":
                                    restOfROI = combos[(centers - 1, wings, defenders, goalies)][player_row - 1][budget_interval - player_cost]
                                elif player_position == "W":
                                    restOfROI = combos[(centers, wings -1 , defenders, goalies)][player_row - 1][budget_interval - player_cost]
                                elif player_position == "D":
                                    restOfROI = combos[(centers, wings, defenders - 1, goalies)][player_row - 1][budget_interval - player_cost]
                                elif player_position == "G":
                                    restOfROI = combos[(centers, wings, defenders, goalies - 1)][player_row - 1][budget_interval - player_cost]
                                    

                                ## We compare it for the optimal ROI if we dont sign the player
                                noSign = table[player_row - 1][budget_interval]
                
                                ## if signing the player generates more profit than not signing the player, then we add him to the table
                                if player_points + restOfROI > noSign:
                                    table[player_row][budget_interval] = player_points + restOfROI
                                    traceback[player_row][budget_interval] = True
                                
                                else:
                                    table[player_row][budget_interval] = noSign
                                    traceback[player_row][budget_interval] = False
                                    
                            ## if we cant afford the player or don't have roster room, we treat it as a noSign
                            else:
                                table[player_row][budget_interval] = table[player_row - 1][budget_interval]
                                traceback[player_row][budget_interval] = False
                                
                                
                                
    
    ## To return the optimized investment portfolio, we create an empty return list
    ## and initialize our item marker value, and a money iteration value
    ret_list = []
    players_remaining = copy.deepcopy(nPlayers)
    i = -1
    centers = copy.deepcopy(limits["C"])
    wings = copy.deepcopy(limits["W"])
    defenders = copy.deepcopy(limits["D"])
    goalies = copy.deepcopy(limits["G"])
    
    ## we loop through our table until our value (signifying the current item) is at 0
    while players_remaining > 0:
        
        ## If our traceback table tells us to buy the investment
        if combos_traceback[(centers, wings, defenders, goalies )][players_remaining][i]:
            
            ## We record the player position
            player_position = players[players_remaining - 1][3]
            
            ## We add our player's name, cost, ROI, and position to our output list
            output_row = (players[players_remaining - 1][0], players[players_remaining - 1][1] * inc, players[players_remaining - 1][2], players[players_remaining - 1][3])
            ret_list.append(output_row)
                            
            ## We increment our money iteration value backwards by the amount that we "spent" on the investment
            ## And increment our item marker value back by 1
            ## and incrememnt back the roster space
            i -= players[players_remaining - 1][1]
            players_remaining -= 1
            
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
            players_remaining -= 1
    
    
    return ret_list#, combos, combos_traceback
 
    

def draft_algo_for_dk(data_for_algo, cap, inc, limits, ir_list, players_not_wanted):
   
    remaining_players = [player for player in data_for_algo if player[0] not in ir_list]    
    remaining_players = [player for player in data_for_algo if player[0] not in players_not_wanted]    

    best_combo = ''
    highest_points = -1
    util_draft = ''
    
    ## If you get one extra center
    
    limits_extra_center = copy.deepcopy(limits)
    limits_extra_center["C"] += 1
    results_extra_center = get_optimal_set(remaining_players, cap, inc, limits_extra_center)
    total_points_extra_center = sum([player[2] for player in results_extra_center])
   
    if total_points_extra_center > highest_points:
        highest_points = total_points_extra_center
        best_combo = results_extra_center
        util_draft = "Center"
    
    print('Extra Center:', total_points_extra_center, 'expected points')

    ## if you get one extra Wing    
    limits_extra_wing = copy.deepcopy(limits)
    limits_extra_wing["W"] += 1
    results_extra_wing = get_optimal_set(remaining_players, cap, inc, limits_extra_wing)
    total_points_extra_wing = sum([player[2] for player in results_extra_wing])

    if total_points_extra_wing > highest_points:
        highest_points = total_points_extra_wing
        best_combo = results_extra_wing
        util_draft = "Wing"

    print('Extra Wing:', total_points_extra_wing, 'expected points')

    ## if you get one extra Defender    
    limits_extra_defender = copy.deepcopy(limits)
    limits_extra_defender["D"] += 1
    
    results_extra_defender = get_optimal_set(remaining_players, cap, inc, limits_extra_defender)
    total_points_extra_defender = sum([player[2] for player in results_extra_defender])

    if total_points_extra_defender > highest_points:
        highest_points = total_points_extra_defender
        best_combo = results_extra_defender
        util_draft = "Defender"

    print('Extra Defender:', total_points_extra_defender, 'expected points')


    ## We get the best option from our 
    print("The Util should be used for an aditional", util_draft)
    return best_combo, highest_points
