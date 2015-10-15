def printMiniBoard(miniBoard):
    print( miniBoard[0], " | ", miniBoard[1], " | ", miniBoard[2])
    print( "---------" )
    print( miniBoard[3], " | ", miniBoard[4], " | ", miniBoard[5])
    print( "---------" )
    print( miniBoard[6], " | ", miniBoard[7], " | ", miniBoard[8])

def printWholeBoard(board):
        for boardRow in range(0, 3):
            for innerRow in range(0, 3):
                print( board[(boardRow*3)+0][innerRow*3+0], " ", board[(boardRow*3)+0][innerRow*3+1], " ", board[(boardRow*3)+0][innerRow*3+2], " | ", board[(boardRow*3)+1][innerRow*3+0], " ", board[(boardRow*3)+1][innerRow*3+1], " ", board[(boardRow*3)+1][innerRow*3+2], " | ", board[(boardRow*3)+2][innerRow*3+0], " ", board[(boardRow*3)+2][innerRow*3+1], " ", board[(boardRow*3)+2][innerRow*3+2])
                if (boardRow < 2 and innerRow == 2):
                    print("-----------+-------------+-------------")

def heuristic(board):
    print("not implemented")
    assert(0)

# Makes one move. (expands all children to depth + 1
# Inputs: whole board state
#         number index of mini board
#         character 'X' or 'O' representing whos turn it is in the round
def getSuccessors(board, whichMiniBoard, whosTurn):
    miniBoard = board[whichMiniBoard]
    for space in range(0, 9):
        if (miniBoard[space] == ' '):
            newBoard = copy.deepcopy(board)
            newBoard[whichMiniBoard][space] = whosTurn
            successors.append((newBoard, space)) #space becomes new miniBoard index
    return successors

def simulateMove(board, whichMiniGame, whosTurn, depth, alpha, beta):
    print("not implemented")
    assert(0)

def playGames():
    opponentsTurn = False
    while noOneWon:
        if( opponentsTurn == True ):
            #wait for command input from opponent
            assert(0)
        #else if (opponentsTurn == False ):
            #It's the computer's turn
            #assert(0)
