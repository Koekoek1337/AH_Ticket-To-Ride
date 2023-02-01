## Hillclimber Algorithm [Snake Hillclimber](#snake-hillclimber)
* explaining the algorithm

This algorithm is a hill climber that seeks to optimize the score of a traject within the totally of the railNetwork.
Here for it takes a random generated railNetwork. Next it chooses for every traject if the first or last station needs to be removed. This happens randomly. Next it will add a station to the begin or the end of the traject. The goal is that every time a traject improves when in finds a better path to take. There is also the option the the traject adds another route. It calculates the totally of the scores before it approves if every single traject is indeed an improvement. Because it is possible that a new path taken optimizes the score of the singe traject, but downgrades the score of the totally of the railNetwork.

* Adjustments to the algorithm
I noticed that this method has mainly effect on the outer stations of every single traject, but does not easily/often lead to changes in the middle of the traject. To resolves this problem, there are two algorithms with a small change. 'SnakeHillClimber1' removes the first two or the last two stations of the traject, and adds two.
'SnakeHillClimber2' removes the stations at the beginning or the end of a traject and replaces them next. This is done so that the middle section of traject will easily be changed as well.


##Comparing scores
# snakeClimber
To start with the comparison with the random baseline. The 'snakeClimber' already improves this. With results ranging from 4212.20 towards 5991.76 points. With a average of 5155.15. This is above random, but can be improved.
[Solution](/docs/railNetwork-snakeClimber.png)
[Hist](//docs/hist-SnakeClimber.png)

#snakeClimber1
'snakeClimber1' has an average of 5487.20, with a broader range; the lowest is 4304.12. But interesting to see is that it turns out that it gives more results on the higher end of the spectrum, with a highest result of 6536.76 points.
Therefore it gives faster better results than the 'snakeClimber'.
[Solution](/docs/railNetwork-snakeClimber1.png)
[Hist](/docs/hist-snakeClimber1.png)

#snakeClimber2
'snakeClimber2' has an average of 5528.73 with a minimum of 4445.92, but it gives more higher
results. It even reaches the 6500.28. This is probably due the fact that it has a higher probability
to change middle route. So the adjustments on the algorithm generated the expected changes.
[Solution](/docs/railNetwork-snakeClimber2.png)
[Hist](/docs/hist-SnakeClimber2.png)

It is interesting for further studies to see what will happen when we eliminate 4, 5 or even 6 stations,
but this will probably re-do a total route. Therefore the choice has been made to combine this algorithm 'snakeClimber2'
with routeReplace algorithm. This is another algorithm that replaces the route with the lowest score.

#routesnakeclimber
The results of this algorithm (routeSnakeClimber) is as follows: it has an average of 5690.80 and the range is from 4650.12 to 6468.20.
This means that this algorithm has not gave a higher score than 'snakeClimber1', but it did gave a more useful range.
[Solution](/docs/railNetwork-routeSnakeClimber.png)
[Hist](/docs/hist-routeSnakeClimber.png)

#snakeClimber2-WithoutUtrecht
The 'snakeClimber2'- algorithm has run without the station Utrecht. This gave a surprising result: the scores were generally higher than that of the complete railNetwork. With an average of 5768.85 and an highest score of 6563.0. Which gives surprisingly a higher score than the runs with Utrecht.
[Hist](/docs/hist-SnakeClimberUtrecht2.png)
