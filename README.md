# RailNL Ticket-To-Ride
This module allows the user to optimize train routing for a rail network consisting of train stations and connections in batch mode with user-defined parameters.

Obtained results can then be visualized using the visualization tools supplied in visualization mode.

User-defined parameters are initialized from a .json file specified in the command line arguments.

By Simon de Jong, Finn Leurs and Hajo Groen

---

## Table of contents
* [Overview](#Overview)
* [Algorithms](#algorithms)
    * [Random](#random)
    * [Greedy Hillclimber](#greedy-hillclimber)
    * [Snake Hillclimber](#snake-hillclimber)
    * [Simulated Annealing Hillclimber](#simulated-annealing-hillclimber)
* [Tuning](#tuning)
    * [Convergence](#convergence)
    * [Logarithmic Cooling](#logarithmic-cooling)
    * [Linear Cooling](#linear-cooling)
    * [Geometric Cooling](#geometric-cooling)
* [Experiments](#experiments)
    * [Holland](#holland)
    * [Random Baseline](#random-baseline)
    * [Snake Hillclimber](#snake-hillclimber-1)
    * [Greedy Hillclimber](#greedy-hillclimber-1)
    * [Simulated Annealing Hillclimber](#simulated-annealing-hillclimber-1)
* [Usage](#usage)
* [References](#references)
---

## Overview

Train routing is a highly complex problem. It involves creating a rail network that routes existing connections between train stations in the most optimal way. The routing of a rail network is considered optimal when the connection coverage is high and when the amount of duplicate connections is low. This while keeping the amount of routes in the rail network and the total time those routes in the rail network take as low as possible. Note that a high connection coverage does not mean every connection has to be used.

To measure the quality of a rail network in our case, it should generate as high as score as possible in the following function:

$$
    K = 10000p - (100T + duration_{tot})
$$

where p is the fraction of connections covered, T is the amount of routes in a rail network and duration<sub>tot</sub> is the sum of durations for all routes in the network.

When optimizing a rail network for Holland, the network is restricted to 7 routes with a maximum duration of 120 minutes per route. The theoretical maximum score for this rail network would be 9219.0 if all connections were covered by as few routes as possible.

When optimizing a rail network for the Netherlands, the network is restricted to 20 routes with a maximum duration of 180 minutes per route. The theoretical maximum score for this rail network would be 7549.0 if all connections were covered by as few routes as possible.

<br>

### Statespace
The amount of permuations of the system depends on the amount of routes and the possible permutations per route. The order of connections does not matter while duplicate connections are allowed if a route is taken as a list of connections in the network that do not have to be connected. The permutations per route also depend on the lengths of the route, which is between 1 and a maximum length. This then depends on what the maximum amount of route durations is that fit inside the maximum time. This means that the sum of all permutations of all possible route lengths has to be taken. As the amount of routes is variable, the sum of all permutations of the system for every amount of routes has to be taken. This results in the following equation for the statespace:

$$
    \sum_{i=1}^{x}
    {
        ({
            \sum_{r = 1}^{m}
            {
                (r+n-1)!
                \over
                r!(n-1)!
            }
        })!
        \over
        i!
        (
            ({
                \sum_{r = 1}^{m}
            {
                (r+n-1)!
                \over
                r!(n-1)!
            }
            })
            -i
        )!
    }
$$

with x for the maximum amount of routes, m for the maximum length of a route, r for the connections in a route and n for the total amount of connections in the system.

As the equation is too computationally expensive to solve using tools like WolframAlpha, a number can not be given.

---

## Algorithms
In order to find the best possible solution for this train routing problem, four different algorithms were developed, starting with a random algorithm as a baseline. The individual algorithms are explained below.

<br>

### Random
The random algorithm chooses an amount of routes between a minimum (either 1 or the minimum amount of routes required to satisfy all connections) and the maximum amount of routes allowed for the problem. It then chooses a random maximum duration for every route between the duration of the longest connection in the system and the maximum duration for a route allowed by the system. After this, it attempts to fill up the route to the maximum duration until it can no longer make any legal moves. When it cannot make any new, legal moves, it starts with a new route.

A legal move in this case means that a station is appended to a route, so that this station has a connection with a station in the
route. The duration of the appended route may not exceed its maximum duration.

Any newly generated route has to be able to score points if they were in an isolated system. If a route does not adhere to this, it is emptied and a new route is made.

<br>

### Greedy Hillclimber
Greedy Hillclimber is an algorithm that improves a random rail network. It does so by taking the lowest scoring route in a rail network and then compares that to a randomly generated route. Whichever of the two routes is better gets incorporated into the rail network. It does this until it fails to improve the rail network 15 thousand times.

<br>

### Snake Hillclimber
This algorithm is a hill climber that seeks to optimize the score of a traject within the totality of the railNetwork. To do this, it takes a random generated railNetwork. Next, it chooses for every traject if the first or last station needs to be removed. This happens randomly. Next, it will add a station to the beginning or the end of the traject. The goal is that a traject improves every time it finds a better path to take. There is also the option that the traject adds another route. It calculates the totality of the scores before it approves if every single traject is indeed an improvement. Because it is possible that a new path taken optimizes the score of the single traject, but downgrades the score of the totality of the railNetwork.

<br>

#### Adjustments to the algorithm
I noticed that this method has mainly effect on the outer stations of every single traject, but does not easily/often lead to changes in the middle of the traject. To resolves this problem, there are two algorithms with a small change. 'SnakeHillClimber1' removes the first two or the last two stations of the traject, and adds two.
'SnakeHillClimber2' removes the stations at the beginning or the end of a traject and replaces them next. This is done so that the middle section of traject will easily be changed as well.

<br>

### Simulated Annealing Hillclimber
The simulated annealing Hillclimber algorithm attempts to optimize a random solution for the train routing problem by either removing, adding or replacing a route. The algorithm is biased towards replacing a route with a 75% chance. Adding and removing a route both have a 12.5% chance to occur.

New routes are created in the same manner that they are created for the random algorithm.

Any change that results in a point increase for the system is immediately accepted. Otherwise it has a chance of being accepted based on its cooling scheme.

<br>

#### Cooling schemes
The main reason for using simulated annealing algorithms is that it allows an algorithm to accept a state that may score less points than the previous state. This can prevent an algorithm from getting stuck at a local optimum, giving it more opportunities to find the true optimum state of a system.

Probability of the accepting the worse state is based on the score difference between the old and new state (dScore) and the "Temperature" (T) of the system according to the following formula<sup>1</sup>:

$$
    P = e^{-{dScore \over T}}
$$

Probability increases with higher temperatures, and decreases with higher score differences. "Temperature" is therefore, in layman's terms, a measure for how likely a worse state is accepted.

In order to increase effectiveness of the hillclimber, the temperature is reduced according to a cooling scheme, of which four have been implemented:

<br>

#### Hillclimber
Not a cooling sceme per-se, but is handled as such. Makes the algorithm act purely as a hillclimber, a worse state for the system will never accepted.

<br>

#### Logarithmic cooling
The system temperature (T) depends on a single constant (C) and the total amount of iterations (i), as seen in the following formula<sup>1</sup>

$$
    T = {C \over log(1 + i)}
$$

The initial temperature (T<sub>init</sub>) in this case will be equal to

$$
    T_{init} = {C \over log(2)}
$$

#### Linear cooling
The temperature (T) of the system depends on an initial temperature (T<sub>init</sub>) and decreases linearly over iterations (i) with a constant speed (C) according to the following formula<sup>1</sup>

$$
    T = T_{init} - Ci
$$

A worse state is never accepted if the temperature is less than or equal to 0.

<br>

#### Geometric cooling
The temperature (T) of the system depends on an initial temperature (T<sub>init</sub>) and decreases geometrically over iterations (i) depending on a constant (C) according to the following formula<sup>1</sup>

$$
    T = T_{init}C^{i}
$$

Where C is any number between 0 and 1.

As T approaches 0, a worse state will not be accepted.

---

## Tuning
The simulated annealing algorithm can make use of multiple cooling schemes and is heavily influenced by its initial temperature and cooling constant. In order to more effectively apply the algorithm to the problem, the simulated annealing algorithm had to be tuned.

### Convergence
In order to find the best convergence limit, 8 batches of 10 runs were done with the simulated annealing algorithm in hillclimber mode using varying convergence limits, as seen below (note that the x-axis is not to scale).

![annealing_convergence](docs/annealing_convergence.png)

From these runs, it was determined that accepting runs with maximum convergence of `10 000`, `20 000` and `50 000` all yielded similar results. Therefore `10 000` was chosen, as it gives good scores in an acceptable timeframe.

### Logarithmic Cooling
The logarithmic cooling scheme is relatively simple, with one parameter that both determines cooling speed and starting temperature. 7 batches of 10 runs were done with the simulated annealing algorithm using the logarithmic cooling scheme and different logarithmic cooling constants, as seen below (note that the x-axis is not to scale).

![annealing_logCooling](docs/annealing_logCooling.png)

The cooling scheme with cooling constant 10 seemed to perform the best out of all the cooling constants, with both the highest average as well as the highest overall score. As this corresponds to an initial temperature of `32`, it was used as initial guess temperature for the `linear cooling` scheme.

### Linear Cooling
With an initial guess for the initial temperature, it was decided that the linear constant should be the initial temperature times a power of 10. To find the best power, 4 batches of 10 runs were done with varying linear constants, as seen below (Note that the x-axis has a logarithmic scale)

![annealing_linConstant](docs/annealing_linConstant.png)

From this, `0.0032` (or `initial temp * 10^-4`) was chosen as the best linear constant, for it had both the highest average score, as well as the best overall score.

Next, 3 batches of 10 runs were done with varying initial temperatures with proportionate linear constants, as seen below (Note that the axis has a logarithmic scale).

![annealing_linTemp](docs/annealing_linTemp.png)

From this, it was taken that initial temperature `64` had a more variable spread, yielding the best scoring solution than had thus been found, and was therefore taken as the best initial temperature for the `linear cooling` scheme.

### Geometric Cooling
The final cooling scheme to be tuned was the geometric cooling scheme. 64 was taken as initial temperature, as it performed well with the `linear cooling` scheme. It was decided that the geometric cooling constant should be of nines. Therefore 4 batches of 10 runs were done with varying geometric constants as seen below (Note that the x-axis has a logarithmic scale)

![annealing_geometric](docs/annealing_geoConstant.png)

The geometric cooling scheme was taken to be outperformed by the `linear cooling` scheme, with initial temperature 64 and `linear cooling` constant `64 * 10^-4`, in all cases. For this reason, the `linear cooling` scheme was chosen as the best suitable for this problem.

---

## Experiments
### Holland
The first instance of the case asked to build a rail system with up to 7 routes of each up to 120 minutes that utilizes all rail connections in Holland. The second instance asked to optimize the system with the score function.

These instances were both evaluated over 10 runs using the simulated annealing algorithm (`linear cooling`) with initial temperature `64` and `linear cooling` constant `64 * 10^-4`.

All the resulting rail systems contained all rail connections, with a high scoring system with 9035 points, as displayed below.

![solution_holland](docs/holland_score9035.png)

As all 10 runs resulted in a high scoring system with all routes, it can be assumed that an optimal rail system in Holland uses all rail connections. It was also observed that all optimized systems used either 5, 6 or 7 routes, but no less. The score is also very close to the theoretical maximum score of 9219, indicating that there is very little left that can be optimized for this network.

---

### Random Baseline
In order to judge a developed algorithm on its effectiveness, a large baseline calculation from 1.6 million valid solutions was made using the random algorithm, which has been displayed in the histogram below:

![baseline_netherlands](docs/random_hist.png)

From this, it was determined that the random algorithm had an average score of 2212.11, with most scores falling between 300 and 4000 points with a slight bias towards lower scores.

---

### Snake Hillclimber
To start, the 'snakeClimber' is compared to the random baseline. The 'snakeClimber' significantly outperforms the random baseline. With results ranging from 4212.20 towards 5991.76 points and an average of 5155.15. This is above random, but can be improved.
![Solution](docs/railNetwork-snakeClimber.png)
![Hist](docs/hist-SnakeClimber.png)

#### snakeClimber1
'snakeClimber1' has an average of 5487.20, with a broader range; the lowest is 4304.12. But, interestingly, it turns out that 'snakeClimber1' gives more results on the higher end of the spectrum compared to 'snakeClimber', with a highest result of 6536.76 points.
This means that it gives faster better results than the 'snakeClimber'.
![Solution](docs/railNetwork-snakeClimber1.png)
![Hist](docs/hist-snakeClimber1.png)

#### snakeClimber2
'snakeClimber2' has an average of 5528.73 with a minimum of 4445.92, but it gives higher
results than 'snakeClimber1'. It even reaches the 6500.28. This is probably due the fact that it has a higher probability
to change closer to the middle of the route. This means that the adjustments to the algorithm generated the expected changes.
![Solution](docs/railNetwork-snakeClimber2.png)
![Hist](docs/hist-SnakeClimber2.png)

It is interesting for further studies to see what will happen when we eliminate 4, 5 or even 6 stations,
but this will probably re-do a total route. Therefore, the choice has been made to combine this algorithm 'snakeClimber2'
with a greedy route replacing algorithm. This is another algorithm that replaces the route with the lowest score.

#### routesnakeclimber
The results of this algorithm (routeSnakeClimber) are as follows: it has an average of 5690.80 and the range is from 4650.12 to 6468.20.
This means that this algorithm has not generated a higher score than 'snakeClimber1', but it did give a more useful range.
![Solution](docs/railNetwork-routeSnakeClimber.png)
![Hist](docs/hist-routeSnakeClimber.png)

#### snakeClimber2-WithoutUtrecht
The 'snakeClimber2'- algorithm has run without the station Utrecht. This gave a surprising result: the scores were generally higher than that of the complete railNetwork. With an average of 5768.85 and a highest score of 6563.0, which gives a higher score than the runs with Utrecht.
[Hist](docs/hist-SnakeClimberUtrecht2.png)

---

### Greedy Hillclimber
With an average score of 5354.58 over 350 runs and a range of final scores between 4449.12 and 6274.28, the algorithm performs significantly better than random in a shorter amount of time.

![map_rail_network_greedy_hillclimber](docs/railNetworkGreedyHillClimberNederland.png)

![histogram_greedy_hillclimber](docs/histGreedyHillClimberNederland.png)

---

### Simulated Annealing Hillclimber
In order to determine whether the `linear cooling` scheme of the simulated annealing algorithm would be effective, a baseline of the simulated annealing algorithm with the hillclimber cooling scheme was taken over 100 runs, which has been displayed in the histogram below.

![annealing_baselineHill](docs/annealing_baselineHill.png)

From this, it can be concluded that the algorithm without any cooling scheme already far outperforms the random algorithm, both in its average score of 6165.99 and overall score spread.

The same baseline was made for the simulated annealing algorithm with the `linear cooling` scheme, with initial temperature 64 and `linear cooling` constant 64 * 10^-4, as displayed below.

![annealing_baselineLin](docs/annealing_baseline_linearCooling.png)

The results from this baseline are interesting, as it shows a worse overall spread and lower average score of 6050.45, while also having a better median score and being more likely to obtain results with scores higher than 6400 points overall. It is therefore preferable to run with the `linear cooling` scheme when performing multiple runs over a longer period of time.

The overall score for the Netherlands was also recorded using the algorithm with the same cooling schedule and parameters. This network had a score of 6605.0 and is displayed below.

![bestSolution](docs/annealing_best_overall.png)

Interesting about this solution is that it utilizes all possible connections in the Netherlands, whilst still scoring higher than any other solution discovered.

### Station Removal
To test what would happen to the final scores of an optimized network if certain stations were removed, 5 batches of 10 runs were done with the simulated annealing algorithm (Linear cooling, T64, C64*10^-4), each lacking a single station, as well as a control batch of 10 runs with all stations.

The stations chosen were

![removedStations](docs/removedStations_finalScores.png)


#### Utrecht Centraal
One of the assignments was to  disconnect Utrecht Centraal from the railNetwork connections. The results of leaving Utrecht out, were surprising at first. The results, counter intuitively, lead to higher overall scores as defined by our score function. We believe that the cause of this is that Utrecht is the biggest junction on the map. Omitting this station causes a significant reduction in the amount of rail that can be traveled. This influences the percentage of rails traveled, and might be the reason for higher scores.

#### Den Helder
Den Helder is an often missing connection in the railNetwork. This is the reason why we decided to remove this station from the network. But this new lay out does not result in major score differences with simulated annealing algorithm.

#### Vlissingen
Vlissingen is, just like Den Helder, a connection that is frequently missing in the results. But leaving this out does not show major results differences in score with simulated annealing algorithm. The reason why there is not a major difference without Vlissingen (or Den Helder) is, we think, because of the fact that they are often left out in the standard run as well. The amount of rail reduction is not a lot (only 1 connection), therefore it does not make a big difference in percentage covered rail. (Unlike Utrecht).


#### Groningen
Groningen was a recommendation. It only has a few connections, and these are of long distances. But the results in score are not significantly different with simulated algorithm.

#### Zwolle
We decided to remove Zwolle from the stations, because it only has a few connections. These connections are of long distance. Because Zwolle is normally a part of routes, it is surprising that this does not give major different results. The reason could be that, just like Groningen, the amount of rails omitted and time gains, does not make a significant contrast in the calculation.


---

## Usage
### Batch mode
In order to optimize rail networks in batch mode, call the module like `python .\railNL [FILENAME].json`

.json properties for batch mode and their valid values are explained below.

<br>

### Main batch properties
`"jobType":` Whether an optimization algorithm has to be ran or if data has to be visualized. Valid values are `["batch" , "bat", "b"]` for batch mode and `["visualize", "vis", "v"]` for visualization mode.

`"stationsFilepath":` The filepath of the .CSV file containing station names and coordinates. Most commonly `"data/StationsNationaal.csv"` for the Netherlands and `"data/StationsHolland.csv"` for Holland

`"connectionsFilepath":` The filepath of the .CSV file containing rail connections and durations. Most commonly `"data/ConnectiesNationaal.csv"` for the Netherlands and `"data/ConnectiesHolland.csv"` for Holland

`"runs":` The amout of times the algorithm has to be ran in batch. Must be an integer equal to or more than 1.

`"algorithm":` The name of the chosen algorithm. Current options are:
- `"random"` - Random Algorithm
- `"annealing"` - Simulated Annealing Algorithm
- `"snakeclimber"`
- `"snakeclimber1"`
- `"snakeclimber2"`
- `"routesnakeclimber"`
- `"routeclimber_finn"`

`"runName":` The human readable part of the result filename.

`"targetFolder":` The folder to where results should be exported.

`"maxRoutes":` The maximum amount of routes allowed in the rail system. 7 for Holland, 20 for the Netherlands

`"maxDuration":` The maximum duration a route is allowed to have. 120 for Holland, 180 for the Netherlands

`"maxConvergence"`: The maximum amount of iteration the algorithm should continue to run for without score improvments.

<br>

### Algorithm specific properties
#### Simulated Annealing Algorithm
`"coolingScheme":` The name of the cooling scheme to be used. Current options are:
- `"Hillclimber"` - Runs the algorithm as a hillclimber
- `"Logarithmic"` - Runs the algorithm with the logarithmic cooling scheme
- `"Linear"` - Runs the algorithm with the linear cooling scheme. Best tested cooling scheme.
- `"Geometric"` - Runs the algorithm with the geometric cooling scheme.

`"initialTemperature":`: The initial temperature for the simulated Annealing algorithm. 64 for the best tested linear annealing scheme. Not nessesary when using the Logarithmic cooling scheme.
`"coolingConstant":` The constant in the cooling scheme. 0.0064 for the best tested linear annealing scheme.

---

### Visualization mode
In order to visualize obtained results, you also call the module like `python .\railNL [FILENAME].json`

The different types of visualization and their .json properties are explained below.

<br>

### Network visualization
Visualizes a solution for the train routing problem.

`"jobType":` any one of `["visualize", "vis", "v"]`

`"plotType":` any one of `["network", "net", "n"]`

`"stationsFilepath":` The filepath of the CSV file containing station names and coordinates.

`"connectionsFilepath":` The filepath of the CSV file containing station connections anddurations.

`"resultFilepath":` The filepath of the solution csv file to visualize.

`"title":` The title of the figure.

`"stationNames":` True if station names have to be displayed next to station nodes, else false.

<br>

### Algotithm Convergence visualization
Plots the score of an algorithm over iterations.



`"jobType":` any one of `["visualize", "vis", "v"]`

`"plotType":` any one of `["algorithm", "alg", "a"]`

`"resultFilepath":` The filepath of the run summary file to collect data from.

`"title":` The title to be displayed on the figure.

<br>

### Histogram visualization
plots the score data from a batch summary file as a histogram.

`"resultFilepath":` The filepath of the batch summary file to collect data from.

`"title":` The title to be displayed on the figure.

`"binCount":` The amount of bins for the histogram

---

Example jobfiles have been provided in the jobs folder for every algorithm and visualisation type, as well as a generic job file for running algorithms.

---

## References
1: Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. https://doi.org/10.13053/cys-21-3-2553
