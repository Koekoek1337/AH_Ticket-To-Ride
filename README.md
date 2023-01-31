# RailNL Ticket-To-Ride
- Introduction

This module allows the user to optimize train routing for a rail network consisting of train stations and connections in batch mode. Obtained results can then be visualized using the visualization tools supplied in visualization mode.

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

---

## Overview
- Introduction of the problem
- Representation of Railnetwork, Station nodes,
    connection Nodes and routes
- Optimization via algorithms
- Statespace

---

## Algorithms
- Introduction of our algorithms
    - First developed a random algorithm, followed by 
        three separae algorithms
    - What are legal moves
    - Our score function

### Random
- Chooses a random amount of railconnections between the
    minimum amount of connections required to satisfy
    all connections and the maximum allowed amount of 
    connections.
- Picks per route an arbitrary maximum duration between 
    the duration of the longest connection and the 
    maximum duration of a route.
- Attempts to fill the route by performing random 
    legal moves untill the route has the new arbitrary   
    duration or untill the route can no longer make any
    legal moves.
- A new route is then only accepted if it would result 
    in a nett point gain in an isolated network. (Ergo, 
    if it were the first route in a network, it would 
    result in a positive amount of points.)
- Multile random solutions can be made in series after
    which the highest score is taken.

### Greedy Hillclimber
- Finn

### Snake Hillclimber
- Simon

### Simulated Annealing
- Hajo
    - Based on random algorithm
    - Short overview simulated Annealing
        - Hillclimber
        - Accepts all score improvements and accepts 
        worse scoring states based on an annealing 
        function based on Temperature
        - Different cooling schemes
    - Every Step:
        - 12.5% chance to remove a random route
        - 12.5% chance to add a random route
        - 75% chance to replace a random route

#### cooling schemes
- Hillclimber
    - Always returns false
- Logarithmic
    - Cooling formula
    - One parameter -> Tinit = C / log(2)
- Linear
    - Cooling formula
    - Two parameters
    - T < 0 -> Returns false
- Geometric
    - Cooling formula
    - Two parameters
    - Return false as T approaches 0

---

## Tuning
As the simulated annealing algorithm can make use of 
multiple cooling schemes and is heavily influenced 
by it's initial temperature and cooling constant.
In order to more effectively apply the algorithm on the problem, the simulated annealing algorithm had to be tuned.

### Convergence
In order to find the best convergence limit, 8 batches of 10 runs were done with the simulated annealing algorithm in hillclimber mode with varying convergence limits, as seen below (note that the x-axis is not to scale).

![annealing_convergence](docs/annealing_convergence.png)

From these runs, it was determined accepting runs 
with maximum convergence of 10 000, 20 000  and 
50 000 all yielded similar results. Therefore 10 000
was chosen, as it gives good scores in an acceptable timeframe.

### Logarithmic Cooling
As the logarithmic cooling scheme is relatively simple, with one parameter that both determines cooling speed and starting temperature, 7 batches of 10 runs were done with the simulated annealing algorithm with the logarithmic cooling scheme and different logarithmic cooling constants, as seen below (note that the x-axis is not to scale).

![annealing_logCooling](docs/annealing_logCooling.png)

The cooling scheme with cooling constant 10 seemed 
to perform the best out of all the cooling 
constants, with both the highest average as well as 
the highest overall score. As this corresponds to an 
initial temperature of 32, it was used as initial 
guess temperature for the linear cooling scheme.

### Linear Cooling
With an initial guess for the initial temperature, it was decided that the linear constant should be the initial temperature times a power of 10. To find the best power, 4 batches of 10 runs were done with varying linear constants, as seen below (Note that the x-axis has a logarithmic scale)

![annealing_linConstant](docs/annealing_linConstant.png)

From this, 0.0032 (or initial temp * 10^-4) was 
chosen as best linear constant, as it had both the 
highest average score, as well as the best overall 
score.

Next, 3 batches of 10 runs were done with varying initial temperatures with proportionate linear constants were done as seen below (Note that the axis has a logarithmic scale).

![annealing_linTemp](docs/annealing_linTemp.png)

From this, it was taken that initial temperature 64 had a more variable spread, yielding the best scoring solution that had thus yet been found, and was therefore taken as the best initial temperature for the linear cooling scheme.

### Geometric Cooling
The final cooling scheme to be tuned was the geometric cooling scheme. 64 was taken as initial temperature, as it performed well with the linear cooling scheme. It was decided that the geometric cooling constant should be of nines. Therefore 4 batches of 10 runs were done with varying geometric constants as seen below (Note that the x-axis has a logarithmic scale)

![annealing_geometic](docs/annealing_geoConstant.png)

The geometric cooling scheme was taken to be outperformed by the linear cooling scheme, with initial temperature 64 and linear cooling constant 64 * 10^-4, in all cases. For this reason, the linear cooling scheme was chosen as the best suitable for this problem.

---

## Experiments
### Holland
- Optimized route for Holland with highest score takes 
    all trainRoutes.
- Figure of railNetwork with score.

### Random Baseline
- 1.6 mil random solutions
- Figure of histogram

#### Snake
- Baseline fig
- Hoogste score

#### GreedyHill
- Baseline fig
- Hoogste score

#### Anneal
- Baseline fig
- Hoogste score

### Station Removal
#### Utrecht Centraal
- National junction
- Counter intuitively leads to higher overall scores as 
    defined by our score function

#### Den Helder
- Often missing connection
- Does not result in major score differences with
    simulated annealing algorithm

#### Vlissingen
- Often missing connection
- Does not result in major score differences with
    simulated annealing algorithm

#### Groningen
- Reccommended
- Does not result in major score differences with
    simulated annealing algorithm

## 