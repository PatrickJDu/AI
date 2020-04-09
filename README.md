# AI
To run this, run GameManager_3 using:

python GameManager_3 on windows

My basic approach is to use a Expectimax to get 2048 about 40-50% of the time.  

I've included 4 heuristics I use to determine the state of the grid:

The weight of the board at any given point.
The empty cells.
if the board is monotonic.
How smooth the board is.

I've also created heuristic weights for everyhting but the weight of the board to increase my chances at getting 2048.

https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
This helped me with understanding the heuristics of this game!
