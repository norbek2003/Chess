import time
from os import system, name
from copy import deepcopy
from pprint import pprint
from colorama import Fore, Style, Back, init
whiteColor = Fore.BLUE
blackColor = Fore.RED
class Piece:
    """ Class dealing with default methods across all pieces. """
    def __init__(self, owner, color, position):
        self.color = color
        self.position = position
        self.hasMoved = False
        self.owner = owner
        self.piecesDefendingThisPiece = 0
    def controlOrInCenter(self, board):
        """ Checks if the piece controls the center or is in the center. """
        centerTier2 = ['D4', 'E4', 'D5', 'E5']
        centerTier1 = ['C3', 'D3', 'E3', 'F3', 'C6', 'D6', 'E6', 'F6', "C4", "C5", "F4", "F5"]
        centerData = {"ControlCenterTier2":[False,0], "ControlCenterTier1":[False,0], "InCenterTier2":(self.position in centerTier2), "InCenterTier1":(self.position in centerTier1)}
        for pos in centerTier2:
            if self.isValidMove(pos, " x ", board):
                centerData["ControlCenterTier2"][0] = True
                centerData["ControlCenterTier2"][1] += 1
                #break
        for pos in centerTier1:
            if self.isValidMove(pos, " x ", board):
                centerData["ControlCenterTier1"][0] = True
                centerData["ControlCenterTier1"][1] += 1
                #break
        return centerData
    def movePiece(self, position, board):
        " Moves the piece."
        self.position = position
        board.NoTheWorldMustBePeopled()
    def numPiecesDefendingThisPiece(self, board):
        " Returns the number of pieces defending the piece. "
        if self.color == "White":
            self.color = "Black"
        else:
            self.color = "White"
        piecesDefendingThisPiece = 0
        for piece in self.owner.pieces:
            if piece.isValidMove(self.position, board.getCoordinateSign(self.position), board):
                piecesDefendingThisPiece += 1
        if self.color == "White":
            self.color = "Black"
        else:
            self.color = "White"
        return piecesDefendingThisPiece
    def numPiecesAttackingThisPiece(self, board):
        """ Returns the number of pieces attacking this piece. """
        numPiecesAttacking = 0
        for piece in self.owner.otherPlayer.pieces:
            if piece.isValidMove(self.position, board.getCoordinateSign(self.position), board):
                #raw_input(piece.position+" "+newPiecePosition)
                numPiecesAttacking += 1
        return numPiecesAttacking
    def numPiecesDefendedByPiece(self, board):
        pass
    def numPiecesAttackedByPiece(self, board):
        " Return the number of pieces that can be attacked by this piece and their total value. "
        count = 0
        valuesTotal = 0
        for piece in self.owner.otherPlayer.pieces:
            if self.isValidMove(piece.position, board.getCoordinateSign(piece.position), board):
                count += 1
                valuesTotal += piece.points
        return (count, valuesTotal)
class Pawn(Piece):
    """ Class that extends piece that deals with the pawn's capabilities. """
    def __init__(self, owner, color, position):
        Piece.__init__(self, owner, color, position)
        if self.color == "White":
            self.symbol = whiteColor+" P "
        else:
            self.symbol = blackColor+" P "
        self.name = "Pawn"
        self.points = 1
    def isValidMove(self, position, positionSymbol, board):
        """ Checks if the inputted position is a valid move. """
        if position in board.boardDict.keys() and self.color == board.boardDict[position].color:
            return False
        spotIsOccupied = False
        if positionSymbol != "   ":
            spotIsOccupied = True
        try:
            if self.color == "White":
                if self.hasMoved is False:
                    if position == self.position[0]+str(int(self.position[1])+2) and not spotIsOccupied and self.position[0]+str(int(self.position[1])+1) not in board.boardDict.keys():
                        return True
                if (position == self.position[0]+str(int(self.position[1])+1)) and not spotIsOccupied:
                    return True
                if position in ("ABCDEFGH"["ABCDEFGH".index(self.position[0])+1]+str(int(self.position[1])+1), "ABCDEFGH"["ABCDEFGH".index(self.position[0])-1]+str(int(self.position[1])+1)) and spotIsOccupied:
                    return True, # board.boardDict[]]
                return False
            
            else:
                
                if self.hasMoved is False:
                    if position == self.position[0]+str(int(self.position[1])-2) and not spotIsOccupied and self.position[0]+str(int(self.position[1])-1) not in board.boardDict.keys():
                        return True
                if position == self.position[0]+str(int(self.position[1])-1) and not spotIsOccupied:
                    return True                     
                if self.position[0] != "H" and position in ("ABCDEFGH"["ABCDEFGH".index(self.position[0])+1]+str(int(self.position[1])-1), "ABCDEFGH"["ABCDEFGH".index(self.position[0])-1] + str(int(self.position[1])-1)) and spotIsOccupied:
                    return True            
                return False
        except IndexError:
            return False
    def movePiece(self, position, board):
        " Moves the piece and promotes if needed."
        self.position = position   
        if self.color == "White" and int(self.position[1]) == 8 or self.color == "Black" and int(self.position[1]) == 1:
            self.promote()
        board.NoTheWorldMustBePeopled()
    def promote(self):
        """ Promotes the pawn after reaching other side of board. """
        if not self.owner.AI:
        
            while True:
                try:
                    piece = raw_input("Which piece would you like to promote to Queen, Knight, Bishop, or Rook? [Q, N, B, R]\n->")[0].upper()
                    if piece not in ["Q", "N", "B", "R"]:
                        raise ValueError
                    if piece == "Q":
                        self.owner.pieces.append(Queen(self.owner, self.color, self.position))
                        self.owner.pieces.remove(self)
                    if piece == "N":
                        self.owner.pieces.append(Knight(self.owner, self.color, self.position))
                        self.owner.pieces.remove(self)
                    if piece == "B":
                        self.owner.pieces.append(Bishop(self.owner, self.color, self.position))
                        self.owner.pieces.remove(self)
                    if piece == "R":
                        self.owner.pieces.append(Rook(self.owner, self.color, self.position))
                        self.owner.pieces.remove(self)                            
                except ValueError:
                    pass
                else:
                    break
        else:
            self.owner.pieces.append(Queen(self.owner, self.color, self.position))
            self.owner.pieces.remove(self)             
class Rook(Piece):
    """ Class that extends piece that deals with the rook's capabilities. """
    def __init__(self, owner, color, position):
        Piece.__init__(self, owner, color, position)
        if self.color == "White":
            self.symbol = whiteColor+" R "
        else:           
            self.symbol = blackColor+" R "
        self.name = "Rook"
        self.points = 5
    def isValidMove(self, position, positionSymbol, board):           
        """ Checks if the inputted position is a valid move. """
        increment = 1
        
        if position in board.boardDict.keys() and self.color == board.boardDict[position].color:
            return False
        if position[1] == self.position[1]:#horizontal
            if "ABCDEFGH".index(position[0]) < "ABCDEFGH".index(self.position[0]):
                increment = -1         
            for i in range("ABCDEFGH".index(self.position[0]), "ABCDEFGH".index(position[0]), increment):
                if board.getCoordinateSign("ABCDEFGH"[i]+position[1]) != "   ":
                    if ("ABCDEFGH"[i]+position[1]) != self.position and ("ABCDEFGH"[i]+position[1]) != position:
                        return False            
            #raw_input(self.position+" "+position)
            return True
        if position[0] == self.position[0]:#vertical
            if int(position[1]) > int(self.position[1]):
                increment = -1
            
            for i in range(int(position[1]), int(self.position[1]), increment):
                #print i
                #raw_input(1)
                if board.getCoordinateSign(position[0]+str(i)) != "   ":
                    return False 
            return True
        return False
class Knight(Piece):
    """ Class that extends piece that deals with the knight's capabilities. """
    def __init__(self, owner, color, position):
        Piece.__init__(self, owner, color, position)
        if self.color == "White":
            self.symbol = whiteColor+" N "
        else:           
            self.symbol = blackColor+" N "
        self.name = "Knight"
        self.points = 3
    def isValidMove(self, position, positionSymbol, board):           
        """ Checks if the inputted position is a valid move. """
        if position in board.boardDict.keys() and self.color == board.boardDict[position].color:
            return False
        if abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0])) == 1 and abs(int(self.position[1])-int(position[1])) == 2:
            return True
        if abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0])) == 2 and abs(int(self.position[1])-int(position[1])) == 1:
            return True
        return False
class Bishop(Piece):
    """ Class that extends piece that deals with the bishops's capabilities. """
    def __init__(self, owner, color, position):
        Piece.__init__(self, owner, color, position)
        if self.color == "White":
            self.symbol = whiteColor+" B "
        else:           
            self.symbol = blackColor+" B "
        self.name = "Bishop"
        self.points = 3
    def isValidMove(self, position, positionSymbol, board):           
        """ Checks if the inputted position is a valid move. """       
        try:
            if position in board.boardDict.keys() and self.color == board.boardDict[position].color:
                return False
            direction = [1, 1]#increment in [h, v] horizontal, vertical
            direction[0] = -("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))/abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))
            direction[1] = -(int(self.position[1])-int(position[1]))/abs(int(self.position[1])-int(position[1]))
            if abs(int(self.position[1])-int(position[1])) == abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0])):
                for i in range(1, abs(int(self.position[1])-int(position[1]))):
                    if board.getCoordinateSign("ABCDEFGH"["ABCDEFGH".index(self.position[0])+(i*direction[0])]+str(int(self.position[1])+(i*direction[1]))) != "   ":
                        return False
                return True
            return False
        except ZeroDivisionError:
            return False
            
class Queen(Piece):
    """ Class that extends piece that deals with the queens's capabilities. """
    def __init__(self, owner, color, position):
        Piece.__init__(self, owner, color, position)
        if self.color == "White":
            self.symbol = whiteColor+" Q "
        else:           
            self.symbol = blackColor+" Q "
        self.name = "Queen"
        self.points = 9
    def isValidMove(self, position, positionSymbol, board):           
        """ Checks if the inputted position is a valid move. """
        rookQueen = Rook(self.owner, self.color, self.position)
        bishopQueen = Bishop(self.owner, self.color, self.position)
        if rookQueen.isValidMove(position, "   ", board) or bishopQueen.isValidMove(position, "   ", board):
            return True
        return False
class King(Piece):
    """ Class that extends piece that deals with the kings's capabilities. """        
    def __init__(self, owner, color, position):
        Piece.__init__(self, owner, color, position)
        if self.color == "White":
            self.symbol = whiteColor+" K "
        else:           
            self.symbol = blackColor+" K "
        self.name = "King"
        self.points = 100
        self.InCheckCurrently = False
    def isValidMove(self, position, positionSymbol, board):           
        """ Checks if the inputted position is a valid move. """
        if position in board.boardDict.keys() and self.color == board.boardDict[position].color:
            return False
        inCheck = False
        for piece in self.owner.otherPlayer.pieces:
            try:
                if piece.name != "King" and piece.isValidMove(position, " K ", board):
                    inCheck = True
            except (IndexError, ZeroDivisionError):
                pass 
        if (abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0])) <= 1) and (abs(int(self.position[1])-int(position[1])) <= 1) and not inCheck:                    
            return True       
        if position == "C1" and self.color == "White" and not inCheck and not self.hasMoved and "A1" in board.boardDict.keys() and not board.boardDict["A1"].hasMoved:
            return True
        if position == "G1" and self.color == "White" and not inCheck and not self.hasMoved and "H1" in board.boardDict.keys() and not board.boardDict["H1"].hasMoved:
            return True
        if position == "C8" and self.color == "Black" and not inCheck and not self.hasMoved and "A8" in board.boardDict.keys() and not board.boardDict["A8"].hasMoved:
            return True
        if position == "G8" and self.color == "Black" and not inCheck and not self.hasMoved and "H8" in board.boardDict.keys() and not board.boardDict["H8"].hasMoved:
            return True                
        return False
    def movePiece(self, position, board):
        "Moves the piece, and moves other pieces based on if the move is castling. "
        inCheck = False
        for piece in self.owner.otherPlayer.pieces:
            try:
                if piece.name != "King" and piece.isValidMove(position, " K ", board):
                    inCheck = True
            except (IndexError, ZeroDivisionError):
                pass         
        if position == "C1" and self.color == "White" and not inCheck and not self.hasMoved and not board.boardDict["A1"].hasMoved and board.boardDict["A1"].isValidMove("D1", "   ", board) and "D1" not in board.boardDict.keys():
            board.boardDict["A1"].movePiece("D1", board)#.position = "D1"
            self.position = position
            
        if position == "G1" and self.color == "White" and not inCheck and not self.hasMoved and not board.boardDict["H1"].hasMoved and board.boardDict["H1"].isValidMove("F1", "   ", board) and "F1" not in board.boardDict.keys():
            board.boardDict["H1"].movePiece("F1", board)#position = "F1"
            self.position = position
            
        if position == "C8" and self.color == "Black" and not inCheck and not self.hasMoved and not board.boardDict["A8"].hasMoved and board.boardDict["A8"].isValidMove("D8", "   ", board) and "D8" not in board.boardDict.keys():
            board.boardDict["A8"].movePiece("D8", board)#position = "D8"
            self.position = position
            
        if position == "G8" and self.color == "Black" and not inCheck and not self.hasMoved and not board.boardDict["H8"].hasMoved and board.boardDict["H8"].isValidMove("F8", "   ", board) and "F8" not in board.boardDict.keys():
            board.boardDict["H8"].movePiece("F8", board)#position = "F8"
            self.position = position
        board.NoTheWorldMustBePeopled()
    def isInCheck(self, board):
        """ Checks if the king is in check. """
        for player in board.players:
            if player.color != self.color:
                for piece in player.pieces:
                    try:
                        if piece.name != "King" and piece.isValidMove(self.position, " K ", board):
                            return True       
                    except (IndexError, ZeroDivisionError):
                        pass 
        return False
    def inCheckMate(self, board):
        """ Checks if the player is in checkmate. """
        positions = [letter + number for number in "12345678" for letter in "ABCDEFGH"]
        
        for piece in [item for item in self.owner.pieces if item != self]:
            for position in positions:
                
                try:    
                    if board.tryTurn(self.owner, piece.position, position, self, False, True, True)[0]:
                        #raw_input(position)
                        return False
                except ValueError:
                    pass
        return True
class Player:                         
    """ Class that deals with player data. """
    def __init__(self, board, color, human):
        self.color = color
        self.points = 0
        self.board = board
        self.capturedPieces = []
        self.otherPlayer = False
        self.AI = not human  
        if self.color == "White":
            self.pieces = [Pawn(self, self.color, "A2"), Pawn(self, self.color, "B2"), Pawn(self, self.color, "C2"), Pawn(self, self.color, "D2"), Pawn(self, self.color, "E2"), Pawn(self, self.color, "F2"), Pawn(self, self.color, "G2"), Pawn(self, self.color, "H2"), Rook(self, self.color, "A1"), Knight(self, self.color, "B1"), Bishop(self, self.color, "C1"), Queen(self, self.color, "D1"), King(self, self.color, "E1"), Bishop(self, self.color, "F1"), Knight(self, self.color, "G1"), Rook(self, self.color, "H1")]
            #self.pieces = [Pawn(self, self.color, "A2"), Pawn(self, self.color, "B2"), Pawn(self, self.color, "C2"), Pawn(self, self.color, "D2"), Pawn(self, self.color, "E2"), Pawn(self, self.color, "F2"), Pawn(self, self.color, "G2"), Pawn(self, self.color, "H2"), Rook(self, self.color, "A1"), King(self, self.color, "E1"), Rook(self, self.color, "H1")]
            
            #self.pieces = [King(self, self.color, "H5"), Rook(self, self.color, "D8"), Pawn(self, self.color, "C7")]
        else:
            self.pieces = [Pawn(self, self.color, "A7"), Pawn(self, self.color, "B7"), Pawn(self, self.color, "C7"), Pawn(self, self.color, "D7"), Pawn(self, self.color, "E7"), Pawn(self, self.color, "F7"), Pawn(self, self.color, "G7"), Pawn(self, self.color, "H7"), Rook(self, self.color, "A8"), Knight(self, self.color, "B8"), Bishop(self, self.color, "C8"), Queen(self, self.color, "D8"), King(self, self.color, "E8"), Bishop(self, self.color, "F8"), Knight(self, self.color, "G8"), Rook(self, self.color, "H8")]
            #self.pieces = [Rook(self, self.color, "A4"), Rook(self, self.color, "A6"), Queen(self, self.color, "E1"), King(self, self.color, "A1"), Pawn(self,self.color, "B2")]
        self.king = [p for p in self.pieces if p.name == "King"][0]
    def loadOtherPlayer(self, board):
        " Initializes the player's other player instance . "
        self.otherPlayer = [p for p in board.players if p != self][0]
    def findBestMove(self, board, carryOutMove, original, depth):
        """ Checks if the inputted position is a valid move. """
        board.count += 1            
        print "    AI RUNNING >> CALCULATING POSSIBILITY : "+str(board.count)+". ELAPSED TIME : "+str(time.strftime("%M:%S", time.gmtime(time.time()-board.startTime)))+" MINUTES.\r",
        positions = [letter + number for number in "12345678" for letter in "ABCDEFGH"]        
        pointsArray = []
        for piece in self.pieces:
            for position in positions:
                try:
                    if piece.isValidMove(position, board.getCoordinateSign(position), board) and piece.position != position:                    
                        pointsArray.append(board.tryTurn(self, piece.position, position, self.king, False, True, original, depth)[1])
                except (ValueError, KeyError):
                    pass
        bestMove = max(pointsArray, key=lambda d: d["totalRawPoints"])
        if depth < board.depth and not carryOutMove:
            return bestMove
        if depth == board.depth:
            print 1       
        if carryOutMove:
            board.tryTurn(self, bestMove["piece"], bestMove["move"], self.king, False, False, True, 1)
        clear()

        board.count=0
        print "a"
      
class Board:    
    """ The board. """
    def __init__(self):
        self.gameWon = False
        self.board = []
        self.players = []
        self.boardDict = {}
        self.setPreferences()
        self.NoTheWorldMustBePeopled()
        self.depth = 3
        self.count = 0
    def setPreferences(self):
        """ Initializes the game preferences. """
        print "Please choose a play style: \n[1]  Player vs Player\n[2]  Player(White) vs AI\n[3]  Player(Black) vs AI"
        while True:
            try:
                pref = raw_input("\n->")
                if int(pref) not in [1, 2, 3]:
                    raise ValueError
                if int(pref) == 1:
                    self.players = [Player(self, "White", True), Player(self, "Black", True)]
                elif int(pref) == 2:
                    self.players = [Player(self, "White", True), Player(self, "Black", False)]
                else:
                    self.players = [Player(self, "White", False), Player(self, "Black", True)]
                for player in self.players:
                    player.loadOtherPlayer(self)
            except ValueError:
                pass
            else:
                break
        #raw_input("Press enter to continue\n->")
    def printBoard(self):
        """ Prints out the chess board. """
        for i in range(len(self.board)-1):
            print colorRow(self.board[i], i)
        print "".join(self.board[8]).encode("utf-8")
    def NoTheWorldMustBePeopled(self):#much ado about nothing -benedick
        """ Updates the player positions on the board. """
        self.boardDict = {}
        self.board = []
        for i in range(8, 0, -1):
            if i < 10:
                row = ["["+str(i)+" ]"]
            else:
                row = ["["+str(i)+"]"]
            for x in range(0, 8):
                row.append("   ")
            self.board.append(row)
        self.board.append(["[  ]", "[A]", "[B]", "[C]", "[D]", "[E]", "[F]", "[G]", "[H]"])
        for player in self.players:
            for piece in player.pieces:
                self.changeCoordinateSign(piece.position, piece.symbol)
                self.boardDict[piece.position] = piece
    def getCoordinateSign(self, spot):
        """ Gets the coordinate sign of the inputted spot. """
        return self.board[8-int(spot[1:])][self.board[8].index("["+str(spot[0]).upper()+"]")]
    def changeCoordinateSign(self, spot, sign):
        """ Change the coordinate sign of the inputted spot. """
        self.board[8-int(spot[1:])][self.board[8].index("["+str(spot[0]).upper()+"]")] = sign

    def takeTurns(self):
        """ 
        Alternate between the players and moves.
        
        Accepts input from human players and runs the chess AI for the AI players. 
        """
        while self.gameWon is False:
            for player in self.players:
                if player.AI is False:
                    while self.gameWon is False:
                        try:
                            clear()
                            self.printBoard()
                            print "\nCaptured Pieces:" 
                            for p in self.players:
                                print p.color+" : Captured Pieces  =  "+str(p.capturedPieces)+" | Points  =  "+str(p.points)
                            print "\n"+player.color +"'s Turn!"
                            print "In Check: "+str([piece for piece in player.pieces if piece.name == "King"][0].isInCheck(self))
                            king = [piece for piece in player.pieces if piece.name == "King"][0]
                                    
                            if king.isInCheck(self) and king.inCheckMate(self):
                                otherPlayer = [p for p in self.players if p != player][0]
                                print "\n ***************************\n * Checkmate! "+otherPlayer.color+" wins ! *\n ***************************"
                                raw_input("\nPress enter to continue!\n->")
                                self.gameWon = True
                                break
                            piecePosition = raw_input("Please choose one of your pieces(ex:A2)\n->").rstrip("\r").upper()
                            if self.boardDict[piecePosition].color != player.color:
                                raise ValueError
                            correctPiece = raw_input("You have chosen your "+self.boardDict[piecePosition].name+" at "+piecePosition+". Is this correct(y/n)?\n->")
                            if correctPiece[0].upper() == "Y":
                                newPiecePosition = raw_input("Where would you like to move it?\n->").rstrip("\r").upper()
                                correctPieceMove = raw_input("You have chosen to move your "+self.boardDict[piecePosition].name+" from "+piecePosition+" to "+newPiecePosition+". Is this correct(y/n)?\n->")
                                if correctPieceMove[0].upper() == "Y" and self.boardDict[piecePosition].isValidMove(newPiecePosition, self.getCoordinateSign(newPiecePosition), self):
                                    self.tryTurn(player, piecePosition, newPiecePosition, king, True, False, True, 1)
                                else:
                                    raise ValueError
                            else:
                                raise ValueError
                        except (ValueError, KeyError):
                            pass
                        else:
                            break
                                
                else:
                    self.startTime=time.time()
                    player.findBestMove(self, True, True, self.depth)
    def tryTurn(self, player, piecePosition, newPiecePosition, king, check4Check, resetMoves, original, depth):
        """ Performs the inputted move, returns information about the move, and undoes the move if a test move. """

        thePiece = self.boardDict[piecePosition]
        savedHasMoved = thePiece.hasMoved
        savedPoints = player.points
        savedCapturedPieces = player.capturedPieces[:]
        capturedPiece = False
        if newPiecePosition in self.boardDict.keys() and self.boardDict[newPiecePosition].name == "King":
            raise ValueError
        if newPiecePosition in self.boardDict.keys() and self.boardDict[newPiecePosition].name != "King" and self.boardDict[newPiecePosition].owner != player:
            capturedPiece = True
            savedPiece=self.boardDict[newPiecePosition]
            #savedPiece = deepcopy(self.boardDict[newPiecePosition])
            player.points += self.boardDict[newPiecePosition].points
            player.capturedPieces.append(self.boardDict[newPiecePosition].symbol[len(self.boardDict[newPiecePosition].symbol)-2])
            player.otherPlayer.pieces.remove(self.boardDict[newPiecePosition])
        thePiece.movePiece(newPiecePosition, self)#.position = newPiecePosition
        thePiece.hasMoved = True
        #self.NoTheWorldMustBePeopled()             
        turnData = {
            "piece":piecePosition, 
            "move":newPiecePosition, 
            "pointsGained":(player.points-savedPoints), 
            "otherKingInCheck":player.otherPlayer.king.isInCheck(self), 
            "centerData":thePiece.controlOrInCenter(self), 
            "firstMove":not savedHasMoved, 
            "pieceWorth":thePiece.points, 
            "colorMove":player.color, 
            "rawPoints":0, 
            "totalRawPoints":0,
            "piecesAttackingThisPiece":thePiece.numPiecesAttackingThisPiece(self),
            "piecesAttackedByThisPiece":thePiece.numPiecesAttackedByPiece(self),
            "piecesDefendingThisPiece":thePiece.numPiecesDefendingThisPiece(self)}
        
        if depth > 1:
            turnData["otherPlayerBestMove"] = player.otherPlayer.findBestMove(self, False, False, depth-1)                    
        if check4Check and king.isInCheck(self):
            if capturedPiece:
                player.points = savedPoints
                player.capturedPieces = savedCapturedPieces
                player.otherPlayer.pieces.append(savedPiece)
            self.boardDict[newPiecePosition].hasMoved = savedHasMoved
            self.boardDict[newPiecePosition].movePiece(piecePosition, self)#.position = piecePosition
            #self.NoTheWorldMustBePeopled()      
            raise ValueError
        if resetMoves:
            thePiece.hasMoved = savedHasMoved      

            thePiece.movePiece(piecePosition, self)#.position = piecePosition   
         
            if capturedPiece:
                player.points = savedPoints
                player.capturedPieces = savedCapturedPieces
                player.otherPlayer.pieces.append(savedPiece)
            self.NoTheWorldMustBePeopled() 

        getRawMoveScore(turnData) 
          
        
        return [True, turnData]

def getRawMoveScore(move):
    """ Returns the raw score of the move based on randomly assigned weights. """
    rawPoints = move["pointsGained"]
    if move["centerData"]["ControlCenterTier1"][0]:
        rawPoints += 1 + move["centerData"]["ControlCenterTier1"][1]
    if move["centerData"]["ControlCenterTier2"][0]:
        rawPoints += 2*(1 + move["centerData"]["ControlCenterTier2"][1])  
    if move["centerData"]["InCenterTier1"]:
        rawPoints += 1     
    if move["centerData"]["InCenterTier2"]:
        rawPoints += 2       
    if move["otherKingInCheck"]:
        rawPoints += 3
    if move["firstMove"]:
        rawPoints += 1
    if move["piecesAttackingThisPiece"]+1 >= move["piecesDefendingThisPiece"]:
        rawPoints -= (move["piecesAttackingThisPiece"]+1-move["piecesDefendingThisPiece"])*move["pieceWorth"]
    if "piecesAttackedByThisPiece" in move.keys():
        rawPoints += move["piecesAttackedByThisPiece"][0] + (move["piecesAttackedByThisPiece"][1]/2)
    move["rawPoints"] = rawPoints
    move["totalRawPoints"] = rawPoints
    if "otherPlayerBestMove" in move.keys():
        move["totalRawPoints"] -= move["otherPlayerBestMove"]["totalRawPoints"]
    return rawPoints
def colorRow(row, rowNum):
    """ Returns a colored version of the inputted row. """
    colorRowList = []
    colorRowList.append(row[0])
    for i in range(1, len(row), 2):
        try:
            if rowNum % 2 == 0:
                colorRowList.append(Back.WHITE+row[i]+Style.RESET_ALL)
                colorRowList.append(Back.BLACK+row[i+1]+Style.RESET_ALL)
            else:
                colorRowList.append(Back.BLACK+row[i]+Style.RESET_ALL)
                colorRowList.append(Back.WHITE+row[i+1]+Style.RESET_ALL)       
        except IndexError:
            pass

    return "".join(colorRowList)

def clear():
    """ Clears the screen. """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
      
      
def printBanner():
    """ Prints the banner, a 3D version of the word chess. """
    f = open('banner.txt', 'r')
    for line in f:
        colorLine = []
        stripLine = line.rstrip("\n")
        for i in stripLine:
            if i == "_":
                colorLine.append(Fore.BLACK+i+Style.RESET_ALL)
            else: 
                colorLine.append(Fore.WHITE+i+Style.RESET_ALL)
        
        print "".join(colorLine)
    
def main():
    """ The main program. """
    if name == 'nt':
        init()
    printBanner()
    board = Board()
    board.takeTurns()
if __name__ == "__main__":
    main()
