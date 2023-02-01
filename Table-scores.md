| **Algorithm**           | **lowest score** | **average score** | **highest score** | **runs**    |
|:-----------------------:|:----------------:|:-----------------:|:-----------------:|:-----------:|
| **Random**              | 300              | 2212,11           | 4000              | 1.6 million |
| **snakeClimber**        | 4215.2           | 5155.15           | 5991.76           | 100         |
| **snakeClimber1**       | 4304             | 5487.20           | 6546.76           | 100         |
| **snakeClimber2**       | 4445.92          | 5528.73           | 6468.20           | 100         |
| **greedy hillclimber**  | 4449,12          | 5354,58           | 6274,28           | 350         |
| **routeSnakeClimber**   | 4650.12          | 5690.78           | 6468.20           | 1000        |
| **hillclimber_hajo**    |                  | 6165,99           |                   | 100         |
| **Simulated Annealing** |                  | 6050,45           | 6605              | 100         |

This table shows the range and the average of every algorithm. It is obvious that all the algorithms are an improvement on the random. What is also clear, is that the original snakeClimber - which eliminates only 1 station - does not show the best results. But with the adjustment of removing and adding more stations at the same time does improve the algorithm and gives higher scores.
An interesting observation is that the routeSnakeClimber (a combination of the snakeClimber and greedy hillclimber) does give a high average, with a smaller range than the other algorithm.
The simulated annealing-algorithm does give the highest score for railNL in our runs.
## TODO ##
Klein beetje over de score van de annealing( maar die staan er nog niet geheel op.)
