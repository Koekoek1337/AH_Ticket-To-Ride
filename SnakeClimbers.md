## Hillclimber Algorithm [Snake Hillclimber](#snake-hillclimber)
## explaining the algoritm
This algorthm is a hill climber that seeks to optimize the score of a traject within the
totally of the railNetwork.
Here for it takes a random generated railNetwork. Next it chooses for every traject if the first
or last station needs to be removed. This happens randomly. Next it will add a station to the
begin or the end of the traject.
The goal is that every time a traject improves when in finds a better path to take.
It calculates the totally of the scores before it approves if every single traject is indeed an improvement.
Because it is possible that a new path taken optimalizes the score of the singe traject, but downgrades
the score of the totally of the railNetwork.

I noticed that this method has mainly effect on the outer stations of every single traject, but does not
easily/often lead to changes in the middle of the traject. To resolves this problem, there are two algorithms
with a small change. [SnakeHillClimber1] removes the first two or the last two stations of the traject, and adds
two.
[SnakeHillClimber2] removes the stations at the beginning or the end of a traject and replaces them next.
This is done so that the middle section of traject will easily be changed as well.


##Comparing scores
To start with the comparison with the random baseline. The 'snakeClimber' already improves this.
With results ranging from 4500 toward 5990 points. With a average of 5614. This is way above

'snakeClimber1' has an average of 5456, with a broader range. But interesting to see is that it turns out
that it gives more results on the higher end of the spectrum, even with results over the 6000 points.
Therefore it gives faster better results than the 'snakeClimber'.

'snakeClimber2' has an average of 5515 with a the same minimun as 'snakeClimber', but it gives higher
results. It even reaches the 6500. This is probably due the fact that it has a higher probability
to change middle route. So the adjustments on the algoritm generated the expected changes.

It is interesting for further studies to see what will happen when we elimante 4, 5 or even 6 stations,
but this will probably redo a total route. Therefore the choice has been made to combine this algoritm 'snakeClimber2'
with routeReplace algoritm. This is another algorithm that replaces the route with the lowest score.

The results of this algorithm (routeSnakeClimber) is as follows: it has an average of 5636 and the range is from 4700 to 6300.
This means that this algorithm has not gave a higher score than 'snakeClimber2', but it did gave a more usefull range.
