import copy
import queue

humansChar = 'X'
computersChar = 'O'

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

#Find a winner for the entire board
#Simplify the large board down into a regular sized board
def getWinner(board):
    bigMiniBoard = [' ' for i in range(0, 9)]
    for miniBoardIndex in range(0, 9) :
        bigMiniBoard[miniBoardIndex] = miniBoardWinner(board[miniBoardIndex])
    #print("The overall winners are:")
    #printMiniBoard(bigMiniBoard)
    overallWinner = miniBoardWinner(bigMiniBoard)
    return overallWinner

def oppositeChar(XorO):
    if(XorO == 'X'):
        return 'O'
    else:
        return 'X'

def getMiniBoardHeuristic(miniBoard):
    heuristic = 0

    #opposite corners
    if(miniBoard[0] == miniBoard[8] and miniBoard[0] == computersChar):
        heuristic += 2
    if(miniBoard[0] == miniBoard[8] and miniBoard[0] == humansChar):
        heuristic -= 2
    if(miniBoard[2] == miniBoard[6] and miniBoard[2] == computersChar):
        heuristic += 2
    if(miniBoard[2] == miniBoard[6] and miniBoard[2] == humansChar):
        heuristic -= 2

    #TODO
    return heuristic


def getHeuristic(board, debuggingOutput):
    winner = getWinner(board)
    if(debuggingOutput):
        print("It thinks the winner is", winner)
    if( winner == computersChar ):
        return 99999
    if( winner == humansChar ):
        return -99999
        
    heuristic = 0
    for i in range(0, 9) :
        miniBoardWinLose = miniBoardWinner(board[i])
        if( computersChar == miniBoardWinLose):
            if(debuggingOutput):
                print("The computer has won board", i)
            heuristic += 100
        elif ( humansChar == miniBoardWinLose):
            if(debuggingOutput):
                print("The human has won board", i)
            heuristic -= 100
        else:
            heuristic += getMiniBoardHeuristic(board[i])
            printMiniBoard(miniBoardWinLose)
            heuristic += getMiniBoardHeuristic(miniBoardWinLose)
    #keep it simple for now. later we can do fancy things like check the number of forced wins/losses
    return heuristic

# Makes one move. (expands all children to depth - 1
# Inputs: whole board state
#         number index of mini board
#         character 'X' or 'O' representing whos turn it is in the round
def getSuccessors(board, whichMiniBoard, whosTurn):
    successors = []
    for space in range(0, 9):
        if (board[whichMiniBoard][space] == ' '):
            newBoard = copy.deepcopy(board)
            newBoard[whichMiniBoard][space] = whosTurn
            successors.append((newBoard, space)) #space becomes new miniBoard index
    return successors

def simulateRound(board, whichMiniGame, depth, computersTurn):
    #base case. Using depth-limited search. 0 is deepest.
    if (depth <= 0 ):
        return getHeuristic(board, False)

    if(not computersTurn):
        #human move
        lowestHumanMove = 99999
        successorsHuman = getSuccessors(board, whichMiniGame, humansChar)
        for successorHuman in successorsHuman :
            (newBoard, humanMove) = successorHuman
            nextLevelVal = simulateRound(newBoard, humanMove, (depth-1), (not computersTurn))
            lowestHumanMove = min(lowestHumanMove, nextLevelVal)
        return lowestHumanMove
            
        
    if( computersTurn ):
        #computer move
        hightestComputerMove = -99999
        possibleComputerMoves = getSuccessors(board, whichMiniGame, computersChar)
        for successorComputer in successorComputer :
            (newBoard, computerMove) = successorComputer
            printWholeBoard(newBoard)
            nextLevelVal = simulateRound(newBoard, computerMove, (depth-1), (not computersTurn))
            hightestComputerMove = max(highestComputerMove, nextLevelVal)
        return hightestComputerMove

    
##
##    XorO = oppositeChar(oldXorO)
##    successors = getSuccessors(previousBoard, whichMiniGame, XorO)
##    maximin = 99999
##    bestMove = -1
##    for successor in successors :
##        (board, moveIndex) = successor
##        (heuristic, newMoveIndex) = simulateMove(board, moveIndex, XorO, (not computersTurn), (depth-1), beta, alpha)
####        if (heuristic > alpha):
####            alpha = heuristic
####        if (heuristic < beta):
####            beta = heuristic
####        if (beta > alpha): #prune
####            return
##        if (heuristic < maximin):
##            maximin = heuristic
##            bestMove = moveIndex
##    return (maximin, bestMove)

def nextComputerMove(board, whichMiniGame, depth):
    nextMoves = queue.Queue()
    successors = getSuccessors(board, whichMiniGame, computersChar)
    for successor in successors :
        (newBoard, move) = successor
        minimax = simulateRound(newBoard, move, (depth-1), False)
        nextMoves.put((minimax, copy.deepcopy(newBoard), copy.deepcopy(move)))
        print("Added move", move, "with minimax", minimax)
    #print("next moves are:", nextMoves.queue)

    #if weights are equal, run the heuristic again
    bestNextMoves = queue.Queue()
    while(True):
        (firstWeight, firstBoard, firstMove) = nextMoves.get()
        (secondWeight, secondBoard, secondMove) = nextMoves.get() #second on the list, first after pop
        nextMoves.put((secondWeight, secondBoard, secondMove)) #reattach it, we want it again
        print("secondWeight is", secondWeight, "secondMove is", secondMove)
        if(firstWeight < secondWeight or secondMove == None or nextMoves.qsize() <= 1): #done, they differ. pick the better one
            bestNextMoves.put(firstWeight, firstBoard, firstMove)
            break
        heuristic = getHeuristic(firstBoard, False)
        bestNextMoves.put((heuristic, firstBoard, firstMove))
        
    return bestNextMoves.get()
def miniBoardFull(miniBoard):
    for i in range(0, 9):
        if( miniBoard[i] == ' '):
            return False
    return True

def nextMiniBoardToPlayOn(board, move):
    #which board do we play on next? is there a draw anywhere?
    targetBoardFull = miniBoardFull(board[move])
    if(not targetBoardFull):
        return move
    print("Board", move, "is full. Finding a suitable board")
    for i in range(0, 9):
        if( not miniBoardFull(board[i])):
            print("We will play on board", i, "since it is not full")
            return i
    print("All boards are full. No one won, it was a Draw. :/")
    return -1
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

def updateOverallBoardWins(overallBoardWins, board):
    for i in range(0, 9):
        if(overallBoardWins[i] == ' '):
            overallBoardWins[i] = miniBoardWinner(board[i])
    return overallBoardWins
        

def initNewEmptyMiniBoard():
    return [' ' for i in range(0, 9)]
        
def playGame():
    maxDepth = 5 #depth limited search
    #emptyMiniBoard = (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')
    #emptyMiniBoard = initNewEmptyMiniBoard
    #board = [emptyMiniBoard, emptyMiniBoard, emptyMiniBoard, emptyMiniBoard, emptyMiniBoard, emptyMiniBoard, emptyMiniBoard, emptyMiniBoard, emptyMiniBoard]
    board = [initNewEmptyMiniBoard() for i in range(0, 9)]
    overallBoardWins = initNewEmptyMiniBoard()

    nextMiniBoard = 0
    while (miniBoardWinner(overallBoardWins) == ' '):
        #humans turn
        print("Overall board wins:")
        printMiniBoard(overallBoardWins)
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
        board[nextMiniBoard][humansMove] = humansChar
        nextMiniBoard = nextMiniBoardToPlayOn(board, humansMove)
        if (nextMiniBoard == -1):
            return #draw
        updateOverallBoardWins(overallBoardWins, board)

        #computers turn
        #(minimax, computersMove) = simulateMove(board, nextMiniBoard, computersChar, True, maxDepth, -99999, 99999)
        computersChoice = nextComputerMove(board, nextMiniBoard, 2)
        (minimaxVal, computersMove) = computersChoice
        print("minimax value is", minimaxVal)
        print("minimax value is", minimaxVal)
        #do error checking
        printMiniBoard(board[nextMiniBoard])
        if( computersMove < 0 or computersMove > 8 or (not (board[nextMiniBoard][computersMove] == ' '))):
            printMiniBoard(board[nextMiniBoard])
            print("^^ O to space", computersMove)
            print("ERROR! Computer tried to make an illegal move")
            assert(0)
        print("")
        board[nextMiniBoard][computersMove] = computersChar
        nextMiniBoard = nextMiniBoardToPlayOn(board, computersMove)
        if (nextMiniBoard == -1):
            return #draw
        updateOverallBoardWins(overallBoardWins, board)

    print("Overall board wins:")
    printMiniBoard(overallBoardWins)
    printWholeBoard(board)
    print("The winner is", getWinner(board), "!!!")

playGame()
#print("mini board winner ", miniBoardWinner([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']))
#print("mini board winner ", miniBoardWinner(['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ']))
#getMiniBoardHeuristic(['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '!'])
