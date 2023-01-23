"""
random solution with n routes

solve(initialNetwork)
    Gradient(initialSolution) -> 
        best = initial
        
        while not converged:
            randomSolution = solveRandom(deepcopy(initialSolution))

            Tempered() -> find optimized solution for a random solution
                attempt to add a random greedy route or remove a random route
        
"""