# File: proj2.py
# Author: Johnlemuel Casilag
# Date: 11/30/2016
# Section: 24
# E-mail: cas6@umbc.edu
# Description: Solves a maze from another file by creating a path if it exists.
# Collaboration: Collaboration was not allowed on this assignment.



# Opens the maze file for reading and returns the different values
# needed to create the maze. Also casts every element into an integer.
# Input: user input of which file they want to open
# Output: dimensions of the maze, finish position, and actual maze as a list
def readMaze(fileName):
    mazeFile = open(fileName, "r")
    fileString = mazeFile.readlines()
    mazeFile.close()

    # white space at the end of each line is removed
    for i in range(0, len(fileString)):
        fileString[i] = fileString[i][:-1]

    # first line is the maze dimensions. it is first split into a list,
    # then both elements are casted as integers
    mazeDims = fileString[0].split()
    for i in range(0, 2):
        mazeDims[i] = int(mazeDims[i])

    # next line is the finish position in the maze. it is first split into
    # a list, then bot elements are casted as integers
    finPosition = fileString[1].split()
    for i in range(0, 2):
        finPosition[i] = int(finPosition[i])

    # first two lines are removed of the file list are removed, as they
    # are no longer needed
    fileString.remove(fileString[0])
    fileString.remove(fileString[0])

    # maze list and a temporary list for each row are initialized. first
    # each element in the file string is split to remove the spaces between,
    # then casting each element as an integer. thus, 'fileString' is now a
    # two dimensional list
    mazeList = []
    tempRowList = []
    for i in range(0, len(fileString)):
        fileString[i] = fileString[i].split()
        for j in range(0, 4):
            fileString[i][j] = int(fileString[i][j])

    # each 'square', first counted by columns, is then appended into the
    # temporary row list, which is then appended into the maze list, thus
    # creating a three dimensional list. i.e. a 3 row by 4 column example:
        # [ [ [walls], [walls], [walls], [wallls] ],
        #   [ [walls], [walls], [walls], [walls] ],
        #   [ [walls], [walls], [walls], [walls] ] ]
    for i in range(0, mazeDims[0]):
        for j in range(0, mazeDims[1]):
            tempRowList.append(fileString[j])
        mazeList.append(tempRowList)
        tempRowList = []

        # it was necessary to clear the row list each time because the entirety
        # of it is appended into the maze list.
        # the file string is also manipulated such that the first row was removed
        fileString = fileString[mazeDims[1]:]

        # this is repeated for each row in the file string
    # maze dimensions, finish position, and the maze as a list are returned
    return mazeDims, finPosition, mazeList




# Asks the user where their starting position will be. Does not accept values
# outside of the range of the maze dimensions.
# Input: maze dimensions
# Output: user inputted starting row and column
def startCoords(mazeDims):
    maxRow = mazeDims[0] - 1
    maxCol = mazeDims[1] - 1
    message = "Please enter the starting"
    invalidMsg = "Invalid, please enter a number between 0 and "

    # uses a loop to ask the user for valid inputs. if the user enters
    # a number out of range, it prompts the user again
    startRow = int(input(message + " row: "))
    while startRow < 0 or startRow > maxRow:
        startRow = int(input(invalidMsg + str(maxRow) + " (inclusive): "))
    startCol = int(input(message + " column: "))
    while startCol < 0 or startCol > maxCol:
        startCol = int(input(invalidMsg + str(maxCol) + " (inclusive): "))

    # returns the user inputted starting row and column
    return startRow, startCol




# global variables are initialized. the coordinates found on the maze list
# '[x, x, x, x]', the first element represents the right side of the square,
# second element representing the bottom, third the left, and fourth the
# top. if the element is 0, there is no wall. if the element is 1, there is
# a wall, meaning the path finder cannot pass through that way.
# these variables are made so that instead of checking mazeList[i][j]['number'],
# it checks specifically the right, bottom, left, or top.
RIGHT = 0
BOT = 1
LEFT = 2
TOP = 3
NO_MOVE = -1




# Recursive function that finds a path from the starting point to the given
# end point.
# Input: current row, current column, the maze as a list, the last move taken
#        (as in, if it moved left, right, up, down, or not at all in the
#        (previous call of the function), the current path it has, and the 
#        final position it is searching for
# Output: the result in the form of the path it took to reach the goal
def searchMaze(row, col, maze, lastMove, searchList, finish):
    # a deep copy is made in order to add on to the list
    searchList = searchList[:]

    # the temporary coordinate is saved as a tuple because it shouldn't be
    # mutable when added to the search list
    tempCoordinate = (row, col)
    searchList.append(tempCoordinate)

    # starting coordinate was saved in order to conclude whether or not a
    # path was found
    startCoordinate = searchList[0]

    # if at any point the last element in the searchList is equal to the 
    # finish, the searchList is returned to the main()
    if searchList[-1] == tuple(finish):
            return searchList

    # a check whether or not if the pathfinder can move in any direction
    if maze[row][col][RIGHT] == 0 and lastMove != LEFT:
        canMove = RIGHT
    elif maze[row][col][BOT] == 0 and lastMove != TOP:
        canMove = BOT
    elif maze[row][col][LEFT] == 0 and lastMove != RIGHT:
        canMove = LEFT
    elif maze[row][col][TOP] == 0 and lastMove != BOT:
        canMove = TOP

    # if there is no possible move, it makes more checks below
    else:
        canMove = NO_MOVE

    # when the pathfinder CAN move, it moves (priority: right -> bottom -> left
    # -> top) by calling the function again and adding 1 to the current
    # position based on which direction it is moving
    if canMove != NO_MOVE:
        if canMove == RIGHT:
            return searchMaze(row, col + 1, maze, RIGHT, searchList, finish)
        elif canMove == BOT:
            return searchMaze(row + 1, col, maze, BOT, searchList, finish)
        elif canMove == LEFT:
            return searchMaze(row, col - 1, maze, LEFT, searchList, finish)
        elif canMove == TOP:
            return searchMaze(row - 1, col, maze, TOP, searchList, finish)

    # if the pathfinder CANNOT move, it checks whether or not it's current
    # position is on either the the starting coordinate or
    # simply a dead end.
    else:

        # if the pathfinder lands on its starting coordinate with no other
        # possible moves, it returns "None" back to main()
        if startCoordinate == tempCoordinate:
            return "None"

        # if the pathfinder simply lands on a deadend which happens most of
        # the time, the pathfinder manipulates the maze in that it "adds a wall"
        # so that it cannot go there again. where it places the wall depends on
        # the last move. furthermore, the searchMaze() function is called again,
        # but with an empty path list
        else:
            if lastMove == RIGHT:
                maze[row][col - 1][RIGHT] = 1
            elif lastMove == BOT:
                maze[row - 1][col][BOT] = 1
            elif lastMove == LEFT:
                maze[row][col + 1][LEFT] = 1
            elif lastMove == TOP:
                maze[row + 1][col][TOP] = 1
            return searchMaze(startCoordinate[0], startCoordinate[1], maze, NO_MOVE, [startCoordinate], finish)

        # virtually, what this pathfinder does is find a path, and if it results in a fail,
        # it manipulates the maze so that it doesn't take that path again.




# Main function that pulls all functions together, asks the user which file
# they want to open, and prints the solution to the maze.
# Input: None
# Output: None
def main():
    print("Welcome to the Maze Solver!")
    whatFileMsg = "Please enter the file name of the maze: "
    mazeDims, finPosition, mazeList = readMaze(input(whatFileMsg))
    startRow, startCol = startCoords(mazeDims)

    # searchList must be initialized outside of the recursive function so that
    # it doesn't keep clearing every time it is called
    searchList = []
    result = searchMaze(startRow, startCol, mazeList, NO_MOVE, searchList, finPosition)

    # if no solution was found, prints that there was no solution found
    if result == "None":
        print("No solution found!")
    else:
        print("Solution found!")

        # the following if statement would not apply if the user chose the finish position as
        # the starting position
        if len(result) > 1:

            # sometimes the path would keep the first position saved, so if it's doubled,
            # it is simply removed
            if result[0] == result[1]:
                result.remove(result[0])
        for i in result:
            print(i)

main()
