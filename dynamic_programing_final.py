## Assignment 3 -- Alexander Arbisman
## This assignment implements a dynamic programing algorithm to find the optimal
## return on real estate investments given a large amount of possible investments 

def printTable(table):
	'''A simple way to display matrices in a more readable format'''
	for i in table:
		print(i)

def optimize(items, money, increment):
	''' This function carries out the dynamic programming solution to a 
	list of possible investments, budget, and money increment'''
	
	## Since we might be working with large amounts of money, we 
	## Use a given increment to ensure that the price changes
	## in meaningful steps only
	money = int(money / increment)
	for item in items:
		item[1] = int(item[1] / increment)
	
	## First we use the list of items and money allowed to build
	## the value table and traceback table
	nItems = len(items)
	table = [[-1 for i in range(money + 1)] for i in range(nItems + 1)]
	traceback = [[None for i in range(money + 1)] for i in range(nItems + 1)]
	
	## Now we fill in our base cases for when money = 0
	for i in range(money + 1):
		table[0][i] = 0
	
	## Now we fill in our table using Dynamic Programming
	## we start by incrementing through every item (or investment opportunity)
	for itemNum in range(1,nItems + 1):
		
		## with every item, we increment through our budget
		for j in range(money + 1):
			
			## first we check to see if the cost of the investment is
			## less than our budget increment
			if int(items[itemNum - 1][1]) <= j:	

				## For ease of use, we explicitly record the ROI of the investment
				valItem = int(items[itemNum - 1][2])
				
				## Then we calculate and record the best ROI of our remaining money
				restOfROI = table[itemNum - 1][j - int(items[itemNum - 1][1])] 
				
				## We compare it to the optimal value of not buying the investment,
				## which is basically the optimal value between all previous investments
				noBuy = table[itemNum - 1][j]
			
				## If the value of buying the investment and optimizing the remaining money
				## is greater than the value of not buying and investing in previous options,
				## We record this newly calculated optimal value in our table record our traceback to buy
				if valItem + restOfROI >= noBuy:
					table[itemNum][j] = valItem + restOfROI
					traceback[itemNum][j] = True
					
				## Otherwise, we record the optimized value of previous investments in our table
				## and mark a false in our traceback table
				else:
					table[itemNum][j] = noBuy
					traceback[itemNum][j] = False
					
			## If we can not afford the investment, we have to treat it as if we
			## chose not to make the investment in terms of our table and traceback table
			else:
				table[itemNum][j] = table[itemNum - 1][j]
				traceback[itemNum][j] = False
				

	
	## To return the optimized investment portfolio, we create an empty return list
	## and initialize our item marker value, and a money iteration value
	ret_list = []
	val = nItems
	i = -1
	
	## we loop through our table until our value (signifying the current item) is at 0
	while val > 0:
	
		## If our traceback table tells us to buy the investment
		if traceback[val][i]:
		
			## We add our investment number, cost, and ROI to our output list
			ret_list.append((items[val - 1][0], items[val - 1][1] * increment, items[val - 1][2]))
			
			## We increment our money iteration value backwards
			## by the amount that we "spent" on the investment
			i -= int(items[val - 1][1])
			
			## And increment our item marker value back by 1
			val -= 1
					
		## If our traceback table tells us to not buy the investment,
		## we simply increment our item marker value back by 1
		else:
			val -= 1
			
			
	print("Total Optimized ROI: " + str(table[nItems][money]))		
	for inv in ret_list:
		print("Investment Name: " + inv[0] + ",\t Investment Cost: " + str(inv[1]) + ",\t Investment ROI: " + str(inv[2]))
	## We return our total ROI and our return list
	
	return table[nItems][money], ret_list
	

def loadData(name):
	'''This function takes a housing data csv and returns a list of
	investment item number, investment cost, and estimated ROI''' 
	
	##First we load the file 
	file = open(name, "r")
	
	## We disregard the first two lines, as they are the header and average data
	header = file.readline()
	avg = file.readline()
	t1 = file.readline()
	t2= file.readline()
	t3 = file.readline()
	
	
	## We initialize an empty list
	items = []
	counter = 0
	
	## For every line of data in our file, we take the most recent January price
	## as the cost of the divestment and the difference in January price from last 
	## years price as the ROI
	for line in file:
		line = line.split(",")
		price = int(line[-1])
		roi = int(line[-1]) - int(line[-13])
		id = line[1]
		items.append([id, price, roi])
	
	return items

	
def main(file, money, increment):
	items = loadData(file)
	optimize(items, money, increment)
	
main("Metro.csv", 1000000, 1000)