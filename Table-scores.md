The following table shows the highest and lowest scores of every algorithm observed during baselining, as well as their average. 

| **Algorithm**                           | **lowest score** | **average score** | **highest score** | **runs**    |
|:---------------------------------------:|:----------------:|:-----------------:|:-----------------:|:-----------:|
| **Random**                              | -681.52          | 2212.11           | 4677.65           | 1.6 million |
| **snakeClimber**                        | 4215.2           | 5155.15           | 5991.76           | 100         |
| **snakeClimber1**                       | 4304             | 5487.20           | 6546.76           | 100         |
| **snakeClimber2**                       | 4445.92          | 5528.73           | 6468.20           | 100         |
| **greedy hillclimber**                  | 4449,12          | 5354,58           | 6274,28           | 350         |
| **routeSnakeClimber**                   | 4650.12          | 5690.78           | 6468.20           | 1000        |
| **Simulated Annealing (hillclimber)**   | 5886.64          | 6165.99           | 6441.00           | 100         |
| **Simulated Annealing (linear cooling)**| 4709.60          | 6050.45           | 6605.00           | 100         |

All algorithms have shown to be a significant improvement over the random algorithm.  What is also clear, is that the original snakeClimber algorithm - which manipulated only 1 station at a time - shows the worst results of all algorithms. But by adjusting the amount of stations removied and added per iteration improved the algorithm by resulting in higher scores.

An interesting observation is that the routeSnakeClimber (a combination of the snakeClimber and greedy hillclimber) does give a higher average, with a smaller range than the algorithms it consists of.

The simulated annealing-algorithm with linear cooling gave the overall highest scores in our runs. Compared to the same algorithm without annealing, it on average produces solutions with lower scores, but it has greater potential in finding solutions with higher scores, making it a more useful tool for running in batch.
