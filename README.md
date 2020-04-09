# AI
My basic approach is to use a Expectimax to get 2048 about 40-50% of the time.  

I've included 4 heuristics I use to determine the state of the grid:

The weight of the board at any given point.
The empty cells.
if the board is monotonic.
How smooth the board is.

I've also created heuristic weights for everyhting but the weight of the board to increase my chances at getting 2048.

 I've referenced a few sources in creating this in comments in the code.
