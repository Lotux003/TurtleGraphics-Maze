import turtle as trtl, random

_width, _height = 20, 20
_length = 20
xpos, ypos = -(_width*10), 10*_height
start_xpos, start_ypos = -(_width*10), 10*_height

CurrentXPos = -(_width*10)
CurrentYPos = _width*10
CurrentCoords = (CurrentXPos, CurrentYPos)

endloopBool = True
onFinish = False
pathComplete = False

BeenTo = []
NotBeen = []
Options = []
NotOptions = []
Direction = []
Path = []
FinishPath = []

solverCoords = (0, 0)

def DrawGrid(turtle, wn):
    turtle.penup()
    turtle.goto(xpos, ypos)
    turtle.pendown()
    GridSquare(turtle, wn)    
def GridSquare(turtle, wn):
    wn.tracer(0)
    newypos = ypos
    for i in range(_height - 1):
        for j in range(_width):
            for k in range(4):
                turtle.forward(_length)
                turtle.right(90)
            turtle.forward(_length)
            
        newypos -= _length
        turtle.penup()
        turtle.goto(xpos, newypos)
        turtle.pendown()
        
    for l in range(_width - 1):
        for m in range(4):
            turtle.forward(_length)
            turtle.right(90)
        turtle.forward(_length)
            
    turtle.forward(_length)
    turtle.right(90)
    turtle.forward(_length)
    turtle.right(90)
    turtle.color("white")
    turtle.forward(_length)
    turtle.right(90)
    turtle.color("black")
    turtle.forward(_length)
    turtle.right(90)
    turtle.hideturtle()
    wn.tracer(1)
    wn.update()

def PracticeDict():
    gridValueX = xpos
    gridValueY = ypos
    for k in range(_height):
        for l in range(_width): 
            NotBeen.append((gridValueX, gridValueY))
            gridValueX += _length
        gridValueX = xpos
        gridValueY -= _length
def CheckRoutes(CurrentX, CurrentY):
    global onFinish
    global FinishPath
    global Path
    if CurrentX == _width*10-_length and CurrentY == -(_height*10)+_length and onFinish != True:
        onFinish = True
        FinishPath = Path.copy()
        LastCoords = Path[-1]
        LastX = LastCoords[0]
        LastY = LastCoords[1]

        FinishPath.append((_width*10 - _length, -(_width*10) + _length))
        FinishPath.append((LastX, LastY - _length))
    else:
        UpCoords = (CurrentX, CurrentY + _length)
        DownCoords = (CurrentX, CurrentY - _length)
        RightCoords = (CurrentX + _length, CurrentY)
        LeftCoords = (CurrentX - _length, CurrentY)

        #print("Checking routes from:", CurrentX, CurrentY)
        #print("Up:", UpCoords, "Down:", DownCoords, "Right:", RightCoords, "Left:", LeftCoords)

        # Reset Options before calculating new ones
        Options.clear()

        # Check each direction for valid moves
        CheckPosInDict(UpCoords, 1, CurrentX, CurrentY) # 1 for up, 2 for down, 3 for right, 4 for left
        CheckPosInDict(DownCoords, 2, CurrentX, CurrentY)
        CheckPosInDict(RightCoords, 3, CurrentX, CurrentY)
        CheckPosInDict(LeftCoords, 4, CurrentX, CurrentY)
    
def CheckPosInDict(Coords, direction, CurrentX, CurrentY):
    global CurrentCoords
    # Check if the coordinate is within the bounds of the grid
    if (xpos <= Coords[0] < xpos + (_width * _length)) and \
       (ypos - (_height * _length) < Coords[1] <= ypos):
        
        # If it's a valid move and has not been visited or already in NotOptions, add to Options
        if Coords not in BeenTo and Coords not in Options and Coords not in NotOptions:
            Options.append(Coords)
            Direction.append(direction)
        
    # If it's out of bounds, add to NotOptions (invalid positions)
    elif Coords not in NotOptions:
        NotOptions.append(Coords)
        #print(f"Adding {Coords} to NotOptions")  # Debugging print

    # Once a coordinate is confirmed as visited, it can be added to BeenTo
    if CurrentCoords not in Options and CurrentCoords not in BeenTo:
        #print(f"Adding {CurrentCoords} to (BeenTo)")
        BeenTo.append(CurrentCoords)
        NotBeen.remove(CurrentCoords)  # Remove from NotBeen after visiting

def Move(runner, pathCreator, solver, wn):
    global CurrentXPos
    global CurrentYPos
    global _length
    global CurrentCoords
    global endloopBool
    
    #print(f"Path appending: {(CurrentXPos, CurrentYPos)}")
    Path.append((CurrentXPos, CurrentYPos))
    #print(f"Finish Path: {FinishPath}")

    # Check if there are any valid options to move to
    if Options:
        # Pick a random valid move from Options
        MoveVar = random.randint(0, len(Options) - 1)
        direction = Direction[MoveVar]
        NewCoords = Options[MoveVar]
        runner.goto(NewCoords)
        #print(f"Moving to: {NewCoords}")
                
        # Update the current position
        first_number = NewCoords[0]
        second_number = NewCoords[1]
        CurrentXPos = first_number
        CurrentYPos = second_number

        if direction == 1:
            pathCreator.penup()
            pathCreator.goto(CurrentXPos + 1, CurrentYPos - _length)
            pathCreator.pendown()
            pathCreator.right(90)
            pathCreator.forward(_length - 1)
            pathCreator.right(180)
            pathCreator.forward(_length - 1)
            pathCreator.right(90)
        elif direction == 2:
            pathCreator.penup()
            pathCreator.goto(CurrentXPos + 1, CurrentYPos)
            pathCreator.pendown()
            pathCreator.right(90)
            pathCreator.forward(_length - 1)
            pathCreator.right(180)
            pathCreator.forward(_length - 1)
            pathCreator.right(90)
        elif direction == 3:
            pathCreator.penup()
            pathCreator.goto(CurrentXPos, CurrentYPos - 1)
            pathCreator.pendown()  
            pathCreator.right(180)
            pathCreator.forward(_length - 1)
            pathCreator.right(180)
            pathCreator.forward(_length - 1)
        elif direction == 4:
            pathCreator.penup()
            pathCreator.goto(CurrentXPos + _length, CurrentYPos - 1)
            pathCreator.pendown()  
            pathCreator.right(180)
            pathCreator.forward(_length - 1)
            pathCreator.right(180)
            pathCreator.forward(_length - 1)
        Direction.clear()


        # Add the current position to BeenTo and remove from NotBeen
        BeenTo.append(NewCoords)
        if NewCoords in NotBeen:
            NotBeen.remove(NewCoords)

        # Add the previous position to NotOptions to prevent backtracking
        previous_position = (CurrentXPos, CurrentYPos)
        if previous_position not in NotOptions:
            NotOptions.append(previous_position)

        # After moving, clear Options and recalculate routes
        CheckRoutes(CurrentXPos, CurrentYPos)
    else:
        if len(Path) < 2:
            print("No options available to move.")
        else:
            while len(Options) == 0:
                if len(Path) != 1:
                    # goto last pos
                    runner.goto(Path[-2])
                    # set the new pos
                    Path2bak = Path[-2]
                    CurrentXPos = Path2bak[0]
                    CurrentYPos = Path2bak[1]
                    # check if it can move
                    CheckRoutes(CurrentXPos, CurrentYPos)
                    if len(Options) == 0:
                        del Path[-1]
                    else:
                        Move(runner, pathCreator, solver, wn)
                        #print(f"Path: {Path}")
                else:
                    if endloopBool == True:
                        endloopBool = False
                        runner.pendown()
                        runner.color("white")
                        runner.forward(_length)
                        runner.hideturtle()
                        pathComplete = True
                        Complete(solver, wn)
                        
def Start(runner, pathCreator, solver, wn):
    runner.penup()
    runner.goto(start_xpos, start_ypos)
    #runner.pendown()
    
    solver.penup()
    solver.goto(xpos + 10, ypos+_length)
    solver.pendown()
    
    for _i in range(500):
        # Reinitialize the grid and available routes
        PracticeDict()
        #print(f"Not Been: {NotBeen}")
        CheckRoutes(CurrentXPos, CurrentYPos)  # Update available routes
        #print(f"Options: {Options}")  # Debugging line to track options
        Move(runner, pathCreator, solver, wn)  # Make a move to a valid option
        Options.clear()

        # else:
        #     print("No options available to move.")
        #     break  # Exit if there are no more valid moves
    
def Complete(solver, wn):
    print("Complete!")
    print(f"Finish Path: {FinishPath}")
    AskToSolve(solver, wn)
    
def AskToSolve(solver, wn):
    while True:
        _solve = input("Do you want me to solve it? (y/n) ")
        if _solve == "y":
            # solve it with a turtle that draws the path
            Solve(solver, wn)
            return False
        elif _solve == "n":
            print("Okay... ")
            return False
        else:
            print("I'm sorry but thats not an option... ")
    
def Solve(solver, wn):
    solveValue = 0
    while len(FinishPath) != 0:
        solverCoords = FinishPath[0]
        solverX = solverCoords[0]
        solverY = solverCoords[1]
        solver.goto(solverX + 10, solverY - 10)
        del FinishPath[0]
        solveValue += 1
