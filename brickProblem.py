def make_bricks(small, big, goal):
    big = big*5
    if (small+big)%goal == 0:return(True)
    if small%goal == 0 and small != 0:return(True)
    if big%goal == 0 and big != 0:return(True)
    if goal%5 == 0 and goal%5 <= big/5:return(True)
    if big != 0 and (goal-small)%5 == 0 and (goal-small)%5 <= big:return(True)
    if int(goal/5) <= big/5 and goal%5 <= small:return(True)
    if (goal-big) > 0 and goal-big-small <= 0:return(True)
    else:return(False)