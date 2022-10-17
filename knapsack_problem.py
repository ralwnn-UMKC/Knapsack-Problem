import numpy as np

# function that manages current items in knapsack
def knapsack(packing, utility, weight, max_weight) :
	total_utility = 0.0
	total_weight = 0.0
	num_items = len(packing)

	# tracking the weight and utility of the knapsack
	for i in range(num_items) :
		if packing[i] == 1 :
			total_utility += utility[i]
			total_weight += weight[i]

	if total_weight > max_weight :
		total_utility = 0.0

	return (total_utility, total_weight)


# function to move to next item
def next_item(packing, step_size) :
	num_items = len(packing)
	item = np.copy(packing)
	i = step_size.randint(num_items)

	if item[i] == 0 :
		item[i] = 1
	elif item[i] == 1 :
		item[i] = 0
	return item


# function determining which items to pack
def pack(num_items, step_size, utilities, weights, max_weight, iterations, start_temp, cooldown_rate) :
	current_temp = start_temp
	current_items = np.ones(num_items)
	(current_utility, current_weight) = knapsack(current_items, utilities, weights, max_weight)
	iteration = 0
	cool_down = 0

	while iteration < iterations :
		next = next_item(current_items, step_size)		
		(next_utility, _) = knapsack(next, utilities, weights, max_weight)

		# packing the next item because utility is higher
		if next_utility > current_utility :
			current_items = next; current_utility = next_utility

		# determining item is worse, and making random step to new item
		else :
			worse_item = np.exp((next_utility - current_utility) / current_temp)
			item = step_size.random()

			# choosing to take the worse item
			if item < worse_item :
				current_items = next; current_utility = next_utility

		# reducing temperature after every 4000 iterations
		if iteration == cool_down:
			current_temp *= cooldown_rate
			cool_down += 4000 
	
		iteration += 1

	return current_items


if __name__ == '__main__':

	input_data = np.genfromtxt('Program2Input.txt', delimiter='	')
	
	utilities = input_data[:, 0]
	weights = input_data[:, 1]
	max_weight = 500
	step_size = np.random.RandomState(1)
	iterations = 40000
	start_temp = 500
	cooldown_rate = .4
	num__items = 100

	packing = pack(num__items, step_size, utilities, weights, max_weight, iterations, start_temp, cooldown_rate)
	(total_utility , total_weight) = knapsack(packing, utilities, weights, max_weight)

	file = open("Knapsack Output.txt", 'w')
	file.write("total number of items : {}\n".format(len(utilities)))
	file.write("max weight allowed : {}\n".format(max_weight))
	file.write("number of iterations : {}\n".format(iterations))
	file.write("start temperature : {}\n".format(start_temp))
	file.write("cool down rate : {}\n".format(cooldown_rate))
	file.write("number of items attempting to pack : {}\n".format(num__items))
	file.write("\n")
	file.write("Total utility of packing = {}\n".format(total_utility))
	file.write("Total weight  of packing = {}\n".format(total_weight))
	file.close()





