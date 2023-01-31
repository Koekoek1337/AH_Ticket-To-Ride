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
* []

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

### Simulated Annealing Hillclimber
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

## Experiments

### Holland
- Optimized route for Holland with highest score takes 
    all trainRoutes.
- Figure of railNetwork with score.

### Tuning
- Simulated Annealing
- Started by tuning convergence

### Baseline

#### Random
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