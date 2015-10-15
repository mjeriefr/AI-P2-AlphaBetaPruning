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

def getSuccessors(board, move):
    print("not implemented")
    assert(0)

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
