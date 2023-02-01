Greedy Hillclimber
	Takes a random rail network
	Greedily replaces routes in rail network by generating new routes
	Stops when no improvement is found after 15000 attempts at improving the rail network

Greedy Hillclimber is an algorithm that improves a random rail network. It does so by taking the lowest scoring route in a rail network and then compares that to a randomly generated route. Whichever of the two routes is better gets incorporated into the rail network. It does this until it fails to improve the rail network 15 thousand times.

With an average score of 5354.58 and a range of final scores between 4449.12 and 6274.28, the algorithm performs significantly better in a shorter amount of time.