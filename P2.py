import copy

def printMiniBoard(miniBoard):
    print( miniBoard[0], "|", miniBoard[1], "|", miniBoard[2])
    print( "--+---+--" )
    print( miniBoard[3], "|", miniBoard[4], "|", miniBoard[5])
    print( "--+---+--" )
    print( miniBoard[6], "|", miniBoard[7], "|", miniBoard[8])
    print("")

def printWholeBoard(board):
    for boardRow in range(0, 3):
        for innerRow in range(0, 3):
            print( board[(boardRow*3)+0][innerRow*3+0], " ", board[(boardRow*3)+0][innerRow*3+1], " ", board[(boardRow*3)+0][innerRow*3+2], " | ", board[(boardRow*3)+1][innerRow*3+0], " ", board[(boardRow*3)+1][innerRow*3+1], " ", board[(boardRow*3)+1][innerRow*3+2], " | ", board[(boardRow*3)+2][innerRow*3+0], " ", board[(boardRow*3)+2][innerRow*3+1], " ", board[(boardRow*3)+2][innerRow*3+2])
            if (boardRow < 2 and innerRow == 2):
                print("-----------+-------------+-------------")
    print("")

def miniBoardWinner(miniBoard):
    #printMiniBoard(miniBoard)
    #rows
    for row in range(0, 3):
        if(miniBoard[row*3+0] == miniBoard[row*3+1] and miniBoard[row*3+1] == miniBoard[row*3+2] and (miniBoard[row*3+0] == 'X' or miniBoard[row*3+0] == 'O')):
            #print("Found a winner on row", row)
            return miniBoard[row*3+0]
    #columns
    for col in range(0, 3):
        if(miniBoard[0+col] == miniBoard[3+col] and miniBoard[3+col] == miniBoard[6+col] and (miniBoard[0+col] == 'X' or miniBoard[0+col] == 'O')):
            #print("Found a winner on column", col)
            return miniBoard[0+col]
    #diagonals
    if(miniBoard[0] == miniBoard[4] and miniBoard[4] == miniBoard[8] and (miniBoard[0] == 'X' or miniBoard[0] == 'O')):
        #print("Found a winner on a diagonal")
        return miniBoard[0]
    if(miniBoard[2] == miniBoard[4] and miniBoard[4] == miniBoard[6] and (miniBoard[2] == 'X' or miniBoard[2] == 'O')):
        #print("Found a winner on a diagonal")
        return miniBoard[2]
    #check for empty squares still available
    for square in miniBoard :
        if (square == ' '):
            #print("There is no winner yet")
            return ' '
    #draw/tied board
    #print("Board is tied")
    return '-'

###Find a winner for the entire board
###Simplify the large board down into a regular sized board
##def getWinner(board):
##    bigMiniBoard = [' ' for i in range(0, 9)]
##    for miniBoardIndex in range(0, 9) :
##        bigMiniBoard[miniBoardIndex] = miniBoardWinner(board[miniBoardIndex])
##    #print("The overall winners are:")
##    #printMiniBoard(bigMiniBoard)
##    overallWinner = miniBoardWinner(bigMiniBoard)
##    return overallWinner

def oppositeChar(XorO):
    if(XorO == 'X'):
        return 'O'
    else:
        return 'X'

def findTwoOfThree(first, second, third):
    nWins = 0
    if(first == second and third == ' '):
        if(first == 'O'):
            nWins += 1
        elif(first == 'X'):
            nWins -= 1
    elif(first == third and second == ' '):
        if(first == 'O'):
            nWins += 1
        elif(first == 'X'):
            nWins -= 1
    elif(second == third and first == ' '):
        if(second == 'O'):
            nWins += 1
        elif(second == 'X'):
            nWins -= 1
    return nWins

def getMiniBoardHeuristic(miniBoard):
    nWins = 0
    #rows
    nWins += findTwoOfThree(miniBoard[0], miniBoard[1], miniBoard[2])
    nWins += findTwoOfThree(miniBoard[3], miniBoard[4], miniBoard[5])
    nWins += findTwoOfThree(miniBoard[6], miniBoard[7], miniBoard[8])
    #columns
    nWins += findTwoOfThree(miniBoard[0], miniBoard[3], miniBoard[6])
    nWins += findTwoOfThree(miniBoard[1], miniBoard[4], miniBoard[7])
    nWins += findTwoOfThree(miniBoard[2], miniBoard[5], miniBoard[8])
    #diagonals
    nWins += findTwoOfThree(miniBoard[0], miniBoard[4], miniBoard[8])
    nWins += findTwoOfThree(miniBoard[6], miniBoard[4], miniBoard[2])
    #count number of wins and make it exponential
    heuristic = 0
    if(nWins <= -2):
        heuristic = -900
    elif(nWins == -1):
        heuristic = -100
    elif(nWins == 0):
        heuristic = 0
    elif(nWins == 1):
        heuristic = 100
    elif(nWins >= 2):
        heuristic = 900
    return heuristic

def getHeuristic(board, overallBoardWinner):
##    #Note: this block of code could slow things down more than it speeds things up
##    winner = getWinner(board)
##    if( winner == 'O' ):
##        return 99999
##    if( winner == 'X' ):
##        return -99999

    newOverallBoardWinners = copy.deepcopy(overallBoardWinner)
        
    heuristic = 0
    for i in range(0, 9) :
        #How many mini boards are won/lost?
        if(newOverallBoardWinners[i] == ' '):
            newOverallBoardWinners[i] = miniBoardWinner(board[i])
        if( 'O' == newOverallBoardWinners[i]):
            heuristic += 1000
        elif( 'X' == newOverallBoardWinners[i]):
            heuristic -= 1000
        #Are we about to win on any mini boards?
        else:
            heuristic += getMiniBoardHeuristic(board[i])

    if(miniBoardWinner(newOverallBoardWinners) != ' '):
        if(miniBoardWinner(newOverallBoardWinners) == 'X'):
           return -99999
        else:
           return 99999

    overallBoardHeuristic = getMiniBoardHeuristic(newOverallBoardWinners)
    heuristic += overallBoardHeuristic * 3
    return heuristic

#which board do we play on next? is there a draw anywhere?
def getNextBoardDuringFullOrDraw(whichMiniBoard, overallBoardWinners):
    if(overallBoardWinners[whichMiniBoard] != ' '):
        for i in range(0, 9):
            if(overallBoardWinners[i] == ' '):
                return i
        return '-' #game over
    return whichMiniBoard

#GUI for getNextBoardDuringFullOrDraw
def getNextBoardDuringFullOrDrawWithPrint(whichMiniBoard, overallBoardWinners):
    newMiniBoard = getNextBoardDuringFullOrDraw(whichMiniBoard, overallBoardWinners)
    if(newMiniBoard == '-'):
        print("All boards are full. No one won, it was a Draw. :/")
    if(whichMiniBoard != newMiniBoard):
        print("Board", whichMiniBoard, "is full. Finding a suitable board")
        print("We will play on board", newMiniBoard, "since it is not full")
    return newMiniBoard

# Makes one move. (expands all children to depth - 1
# Inputs: whole board state
#         number index of mini board
#         character 'X' or 'O' representing whos turn it is in the round
def getSuccessors(board, whichMiniBoard, computersTurn, overallBoardWinners):
    #If the board is already full or won, go to another board
    if(overallBoardWinners[whichMiniBoard] != ' '):
        nextBoard = getNextBoardDuringFullOrDraw(whichMiniBoard, overallBoardWinners)
        return getSuccessors(board, nextBoard, computersTurn, overallBoardWinners)
    
    playerChar = ' '
    if (computersTurn):
        playerChar = 'O'
    else:
        playerChar = 'X'
    successors = []
    for space in range(0, 9):
        if (board[whichMiniBoard][space] == ' '):
            newBoard = copy.deepcopy(board)
            newBoard[whichMiniBoard][space] = playerChar
            successors.append((newBoard, space)) #space becomes new miniBoard index
    return successors

def simulateMove(previousBoard, whichMiniGame, computersTurn, overallBoardWinners, depth, alpha, beta):
    #base case. Using depth-limited search. 0 is deepest.
    if (depth <= 0 ):
        #printWholeBoard(previousBoard)
        #print("Reached max depth")
        #print("")
        return (getHeuristic(previousBoard, overallBoardWinners), -1)

    successors = getSuccessors(previousBoard, whichMiniGame, computersTurn, overallBoardWinners)
    maximin = -99999
    bestMove = -1
    for successor in successors :
        (board, moveIndex) = successor
        #printWholeBoard(board)
        (heuristic, newMoveIndex) = simulateMove(board, moveIndex, (not computersTurn), overallBoardWinners, (depth-1), beta, alpha)
##        if (heuristic > alpha):
##            alpha = heuristic
##        if (heuristic < beta):
##            beta = heuristic
##        if (beta > alpha): #prune
##            return
        if (heuristic > maximin):
            maximin = heuristic
            bestMove = moveIndex
    return (maximin, bestMove)

##def miniBoardFull(miniBoard):
##    for i in range(0, 9):
##        if( miniBoard[i] == ' '):
##            return False
##    return True

##def nextMiniBoardToPlayOn(board, move, overallBoardWinners):
##    #which board do we play on next? is there a draw anywhere?
##    getNextBoardDuringFullOrDraw #CALL THIS METHOD!!!
##    if(not targetBoardFull):
##        return move
##    print("Board", move, "is full. Finding a suitable board")
##    for i in range(0, 9):
##        if( not miniBoardFull(board[i])):
##            print("We will play on board", i, "since it is not full")
##            return i
##    print("All boards are full. No one won, it was a Draw. :/")
##    return -1
##    print("miniBoardWinner(board[move]) =", miniBoardWinner(board[move]), ".")
##    if( miniBoardWinner(board[move]) != ' '):
##        print("Draw!")
##    if( miniBoardWinner(board[move]) == ' '):
##        #play on the board corresponding with the last move
##        return move
##    print("Board", move, "is drawn. Finding a suitable board")
##    for i in range(0, 9):
##        print("Trying board", i)
##        if( not miniBoardWinner(board[i])):
##            print("We will play on board", i, "since it is not drawn")
##            return i
##    print("All boards are in a draw. No one won.")
##    return -1

def initNewEmptyMiniBoard():
    return [' ' for i in range(0, 9)]
        
def playGames():
    maxDepth = 5 #depth limited search
    board = [initNewEmptyMiniBoard() for i in range(0, 9)]
    overallBoardWinners = initNewEmptyMiniBoard()

    nextMiniBoard = 0
    while (miniBoardWinner(overallBoardWinners) == ' '):
        #humans turn
        print("Overall board winners:")
        printMiniBoard(overallBoardWinners)
        print("")
        printWholeBoard(board)
        print("")
        print("You are playing on board", nextMiniBoard)
        printMiniBoard(board[nextMiniBoard])
        print("")
        invalidMove = True
        while( invalidMove ):
            humansMoveString = input("Your move: ")
            humansMove = int(humansMoveString)
            if( humansMove >= 0 and humansMove <=8 and board[nextMiniBoard][humansMove] == ' '):
                invalidMove = False
            else:
                print("Enter a number 0 to 8, which hasn't already been taken.")
        board[nextMiniBoard][humansMove] = 'X'
        if(overallBoardWinners[nextMiniBoard] == ' '):
            overallBoardWinners[nextMiniBoard] = miniBoardWinner(board[nextMiniBoard])
            if(miniBoardWinner(overallBoardWinners) != ' '):
                print("The winner is", miniBoardWinner(overallBoardWinners), "!!!")
                return miniBoardWinner(overallBoardWinners) #someone won the game
        nextMiniBoard = getNextBoardDuringFullOrDrawWithPrint(humansMove, overallBoardWinners)
        if (nextMiniBoard == -1):
            return #draw

        #computers turn
        (heuristic, computersMove) = simulateMove(board, nextMiniBoard, True, overallBoardWinners, maxDepth, -99999, 99999)
        #do error checking
        if( computersMove >= 0 and computersMove <=8 and board[nextMiniBoard][computersMove] == ' '):
            print("Computer chose", computersMove)
            print("")
        else:
            print("ERROR! Computer tried to make an illegal move to square", computersMove, "in board", nextMiniBoard)
            assert(0)
        board[nextMiniBoard][computersMove] = 'O'
        if(overallBoardWinners[nextMiniBoard] == ' '):
            overallBoardWinners[nextMiniBoard] = miniBoardWinner(board[nextMiniBoard])
            if(miniBoardWinner(overallBoardWinners) != ' '):
                print("The winner is", miniBoardWinner(overallBoardWinners), "!!!")
                return miniBoardWinner(overallBoardWinners) #someone won the game
        nextMiniBoard = getNextBoardDuringFullOrDrawWithPrint(computersMove, overallBoardWinners)
        if (nextMiniBoard == -1):
            return #draw

    printWholeBoard(board)
    print("The winner is", miniBoardWinner(overallBoardWinners), "!!!")

playGames()
#print("mini board winner ", miniBoardWinner([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ']))
#getMiniBoardHeuristic([' ', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' '])
#mb = ['O', ' ', ' ', ' ', ' ', 'O', ' ', 'O', ' ']
#printMiniBoard(mb)
#print("mini board heuristic", getMiniBoardHeuristic(mb))
