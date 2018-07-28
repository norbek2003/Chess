from colorama import Fore, Style, Back, init
from os import system, name
import random
#Take turn calls itself recursion times, then returns outcome
#resizing cmd screws with colorama board
whiteColor=Fore.BLUE
blackColor=Fore.RED
class Piece:
    def __init__(self,owner,color,position):
        self.color=color
        self.position=position
        self.hasMoved=False
        self.owner=owner
    def controlOrInCenter(self,board):
        centerTier2=['D4', 'E4', 'D5', 'E5']
        centerTier1=['C3', 'D3', 'E3', 'F3', 'C6', 'D6', 'E6', 'F6',"C4","C5","F4","F5"]
        centerData={"ControlCenterTier2":False,"ControlCenterTier1":False,"InCenterTier2":(self.position in centerTier2),"InCenterTier1":(self.position in centerTier1)}
        for pos in centerTier2:
            if self.isValidMove(pos," x ",board):
                centerData["ControlCenterTier2"]=True
                break
        for pos in centerTier1:
            if self.isValidMove(pos," x ",board):
                centerData["ControlCenterTier1"]=True
                break
        return centerData    
class Pawn(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=whiteColor+" P "
        else:           
            self.symbol=blackColor+" P "
        self.name="Pawn"
        self.points=1
    def isValidMove(self,position,positionSymbol,board):           
        spotIsOccupied=False
        if positionSymbol!="   ":
            spotIsOccupied=True
        if self.color=="White":
            if self.hasMoved==False:
                if position==self.position[0]+str(int(self.position[1])+2) and not spotIsOccupied:
                    return True
            if (position==self.position[0]+str(int(self.position[1])+1)) and not spotIsOccupied:
                return True       
            if position in ("ABCDEFGH"["ABCDEFGH".index(self.position[0])+1]+str(int(self.position[1])+1),"ABCDEFGH"["ABCDEFGH".index(self.position[0])-1]+str(int(self.position[1])+1)) and spotIsOccupied:
                return True,# board.boardDict[]]
            return False 
        
        else:
            if self.hasMoved==False:
                if position==self.position[0]+str(int(self.position[1])-2) and not spotIsOccupied:
                    return True
            if position==self.position[0]+str(int(self.position[1])-1) and not spotIsOccupied:
                return True      
            #p=("ABCDEFGH"["ABCDEFGH".index(self.position[0])+1]+str(int(self.position[1])-1),"ABCDEFGH"["ABCDEFGH".index(self.position[0])-1]+str(int(self.position[1])-1))
            #if position in p and spot is occupied:
           
            if self.position[0]!="H" and position in ("ABCDEFGH"["ABCDEFGH".index(self.position[0])+1]+str(int(self.position[1])-1),"ABCDEFGH"["ABCDEFGH".index(self.position[0])-1]+str(int(self.position[1])-1)) and spotIsOccupied:
                return True            
            return False
class Rook(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=whiteColor+" R "
        else:           
            self.symbol=blackColor+" R "
        self.name="Rook"
        self.points=5
    def isValidMove(self,position,positionSymbol,board):           
        increment=1
        if position[1]==self.position[1]:#horizontal
            if "ABCDEFGH".index(position[0])<"ABCDEFGH".index(self.position[0]):
                increment=-1         
            for i in range("ABCDEFGH".index(self.position[0]),"ABCDEFGH".index(position[0]),increment):
                if board.getCoordinateSign("ABCDEFGH"[i]+position[1])!="   ":
                    if ("ABCDEFGH"[i]+position[1])!=self.position and ("ABCDEFGH"[i]+position[1])!=position:
                        return False            
            return True
        if position[0]==self.position[0]:#vertical
            if int(position[1])>int(self.position[1]):
                increment=-1
            
            for i in range(int(position[1]),int(self.position[1]),increment):
                #print i
                #raw_input(1)
                if board.getCoordinateSign(position[0]+str(i))!="   ":
                    return False 
            return True
        return False

class Knight(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=whiteColor+" N "
        else:           
            self.symbol=blackColor+" N "
        self.name="Knight"
        self.points=3
    def isValidMove(self,position,positionSymbol,board):           
        if abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))==1 and abs(int(self.position[1])-int(position[1]))==2:
            return True
        if abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))==2 and abs(int(self.position[1])-int(position[1]))==1:
            return True
        return False

class Bishop(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=whiteColor+" B "
        else:           
            self.symbol=blackColor+" B "
        self.name="Bishop"
        self.points=3
    def isValidMove(self,position,positionSymbol,board):           
        try:
            direction=[1,1]#increment in [h,v] horizontal, vertical
            direction[0]=-("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))/abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))
            direction[1]=-(int(self.position[1])-int(position[1]))/abs(int(self.position[1])-int(position[1]))
            if abs(int(self.position[1])-int(position[1]))==abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0])):
                for i in range(1,abs(int(self.position[1])-int(position[1]))):
                    if board.getCoordinateSign("ABCDEFGH"["ABCDEFGH".index(self.position[0])+(i*direction[0])]+str(int(self.position[1])+(i*direction[1])))!="   ":
                        return False
                return True
            return False
        except ZeroDivisionError:
            return False
            
class Queen(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=whiteColor+" Q "
        else:           
            self.symbol=blackColor+" Q "
        self.name="Queen"
        self.points=9
    def isValidMove(self,position,positionSymbol,board):           
        rookQueen=Rook(self.owner,self.color,self.position)
        bishopQueen=Bishop(self.owner,self.color,self.position)
        if rookQueen.isValidMove(position,"   ",board) or bishopQueen.isValidMove(position,"   ",board):
            return True
        return False
class King(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=whiteColor+" K "
        else:           
            self.symbol=blackColor+" K "
        self.name="King"
        self.points=100
        self.InCheckCurrently=False
    def isValidMove(self,position,positionSymbol,board):           
        inCheck=False
        for player in board.players:
            if player.color!=self.color:
                for piece in player.pieces:
                    try:
                        if piece.name!="King" and piece.isValidMove(position," K ",board):
                            inCheck=True
                    except (IndexError,ZeroDivisionError):
                        pass 
        if (abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))<=1) and (abs(int(self.position[1])-int(position[1]))<=1) and not inCheck:                    
            return True
        if position=="C1" and self.color=="White" and not inCheck and not self.hasMoved and not board.boardDict["A1"].hasMoved:
            board.boardDict["A1"].position="D1"
            return True
        if position=="G1" and self.color=="White" and not inCheck and not self.hasMoved and not board.boardDict["H1"].hasMoved:
            board.boardDict["H1"].position="F1"
            return True
        if position=="C8" and self.color=="Black" and not inCheck and not self.hasMoved and not board.boardDict["A8"].hasMoved:
            board.boardDict["A8"].position="D8"
            return True
        if position=="G8" and self.color=="Black" and not inCheck and not self.hasMoved and not board.boardDict["H8"].hasMoved:
            board.boardDict["H1"].position="F8"
            return True        
        
        #g1if (abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))<=1) and (abs(int(self.position[1])-int(position[1]))<=1):
         #   return True
        return False
    def isInCheck(self,board):
        for player in board.players:
            if player.color!=self.color:
                for piece in player.pieces:
                    try:
                        if piece.name!="King" and piece.isValidMove(self.position," K ",board):
                            return True       
                    except (IndexError,ZeroDivisionError):
                        pass 
        return False
    def inCheckMate(self,board):
        positions=[letter + number for number in "12345678" for letter in "ABCDEFGH"]
        
        for piece in [item for item in self.owner.pieces if item != self]:
            for position in positions:
                
                try:    
                    if board.tryTurn(self.owner,piece.position,position,self,False,True)[0]:
                        #raw_input(position)
                        return False
                except ValueError:
                    pass
        return True
class Player:               
    def __init__(self,board,color,human):
        self.color=color
        self.points=0
        self.capturedPieces=[]
        self.AI=not human  
        if self.color=="White":
            self.pieces=[Pawn(self,self.color,"A2"),Pawn(self,self.color,"B2"),Pawn(self,self.color,"C2"),Pawn(self,self.color,"D2"),Pawn(self,self.color,"E2"),Pawn(self,self.color,"F2"),Pawn(self,self.color,"G2"),Pawn(self,self.color,"H2"),Rook(self,self.color,"A1"),Knight(self,self.color,"B1"),Bishop(self,self.color,"C1"),Queen(self,self.color,"D1"),King(self,self.color,"E1"),Bishop(self,self.color,"F1"),Knight(self,self.color,"G1"),Rook(self,self.color,"H1")]
            #self.pieces=[King(self,self.color,"H5"),Rook(self,self.color,"D8"),Pawn(self,self.color,"D1")]
        else:
            self.pieces=[Pawn(self,self.color,"A7"),Pawn(self,self.color,"B7"),Pawn(self,self.color,"C7"),Pawn(self,self.color,"D7"),Pawn(self,self.color,"E7"),Pawn(self,self.color,"F7"),Pawn(self,self.color,"G7"),Pawn(self,self.color,"H7"),Rook(self,self.color,"A8"),Knight(self,self.color,"B8"),Bishop(self,self.color,"C8"),Queen(self,self.color,"D8"),King(self,self.color,"E8"),Bishop(self,self.color,"F8"),Knight(self,self.color,"G8"),Rook(self,self.color,"H8")]
            #self.pieces=[Rook(self,self.color,"A4"),Rook(self,self.color,"A6"),Queen(self,self.color,"E1"),King(self,self.color,"A1")]
        self.king=[p for p in self.pieces if p.name=="King"][0]
    def loadOtherPlayer(self,board):
        self.otherPlayer=[p for p in board.players if p!=self][0]
    def findBestMove(self,board):
        positions=[letter + number for number in "12345678" for letter in "ABCDEFGH"]        
        pointsArray={}
        maxPointsArray=[]
        bestMove=[]#piece,moveTo
        for piece in self.pieces:
            pointsArray[piece.position]={}
            for position in positions:
                try:
                    if piece.isValidMove(position,"   ",board):                    
                        #clear()
                        #board.printBoard()
                        turnResults=board.tryTurn(self,piece.position,position,self.king,False,True)[1]
                        
                        #board.printBoard()
                        raw_input(piece.position + "   "+ position )
                        #if turnResults["otherKingInCheck"]!=False or turnResults["pointsGained"]!=0:
                        pointsArray[piece.position][position]=turnResults
                except (ValueError,KeyError):
                    pass
            
            try:
                if not bool(pointsArray[piece.position]):
                    del pointsArray[piece.position]
            except KeyError:
                pass
        #print 2
        for piece in pointsArray:
            maxPointsArray.append({"piece":piece,"move":max(pointsArray[piece], key=lambda v: getRawMoveScore(pointsArray[piece][v])),"rawPoints":max(getRawMoveScore(move) for move in pointsArray[piece].values())})
        piece= max(maxPointsArray, key=lambda d: d["rawPoints"])["piece"]
        position=max(maxPointsArray, key=lambda d: d["rawPoints"])["move"]

        board.tryTurn(self,piece,position,[p for p in self.pieces if p.name=="King"][0],False,False)
        #clear()
        #board.printBoard()
        
        print "a"
      
class Board:    
    def __init__(self):
        self.gameWon=False
        self.board=[]
        self.players=[]
        self.boardDict={}
        self.setPreferences()
        self.NoTheWorldMustBePeopled()
    def setPreferences(self):
        print "Please choose a play style: \n[1]  Player vs Player\n[2]  Player(White) vs AI\n[3]  Player(Black) vs AI"
        while True:
            try:
                pref=raw_input("\n->")
                if int(pref) not in [1,2,3]:
                    raise ValueError
                if int(pref)==1:
                    self.players=[Player(self,"White",True),Player(self,"Black",True)]
                elif int(pref)==2:
                    self.players=[Player(self,"White",True),Player(self,"Black",False)]
                else:
                    self.players=[Player(self,"White",False),Player(self,"Black",True)]
                for player in self.players:
                    player.loadOtherPlayer(self)
            except ValueError:
                pass
            else:
                break
        #raw_input("Press enter to continue\n->")
    def printBoard(self):
        for i in range(len(self.board)-1):
            print colorRow(self.board[i],i)
        print "".join(self.board[8]).encode("utf-8")
    def NoTheWorldMustBePeopled(self):#much ado about nothing -benedick
        self.boardDict={}
        self.board=[]
        for i in range(8,0,-1):
            if i<10:
                row=["["+str(i)+" ]"]
            else:
                row=["["+str(i)+"]"]
            for x in range(0,8):
                row.append( "   " )
            self.board.append(row)
        self.board.append(["[  ]", "[A]","[B]","[C]","[D]","[E]","[F]","[G]","[H]"])
        for player in self.players:
            for piece in player.pieces:
                self.changeCoordinateSign(piece.position,piece.symbol)
                self.boardDict[piece.position]=piece
    def getCoordinateSign(self,spot):
        return self.board[8-int(spot[1:])][self.board[8].index("["+str(spot[0]).upper()+"]")]
    def changeCoordinateSign(self,spot,sign):
        #print spot,sign
        self.board[8-int(spot[1:])][self.board[8].index("["+str(spot[0]).upper()+"]")] = sign

    def takeTurns(self):
        while self.gameWon==False:
            for player in self.players:
                if player.AI==False:
                    while self.gameWon==False:
                        try:
                            clear()
                            self.printBoard()
                            print "\nCaptured Pieces:" 
                            for p in self.players:
                                print p.color+" : Captured Pieces = "+str(p.capturedPieces)+" | Points = "+str(p.points)
                            print "\n"+player.color +"'s Turn!"
                            print "In Check: "+str([piece for piece in player.pieces if piece.name=="King"][0].isInCheck(self))
                            king=[piece for piece in player.pieces if piece.name=="King"][0]
                                    
                            if king.isInCheck(self) and king.inCheckMate(self):
                                otherPlayer=[p for p in self.players if p !=player][0]
                                print "\n ***************************\n * Checkmate! "+otherPlayer.color+" wins ! *\n ***************************"
                                raw_input("\nPress enter to continue!\n->")
                                self.gameWon=True
                                break
                            piecePosition=raw_input("Please choose one of your pieces(ex:A2)\n->").rstrip("\r").upper()
                            if self.boardDict[piecePosition].color!=player.color:
                                raise ValueError
                            correctPiece=raw_input("You have chosen your "+self.boardDict[piecePosition].name+" at "+piecePosition+". Is this correct(y/n)?\n->")
                            if correctPiece[0].upper()=="Y":
                                newPiecePosition=raw_input("Where would you like to move it?\n->").rstrip("\r").upper()
                                correctPieceMove=raw_input("You have chosen to move your "+self.boardDict[piecePosition].name+" from "+piecePosition+" to "+newPiecePosition+". Is this correct(y/n)?\n->")
                                if correctPieceMove[0].upper()=="Y" and self.boardDict[piecePosition].isValidMove(newPiecePosition,self.getCoordinateSign(newPiecePosition),self):
                                    raw_input(str(self.boardDict[piecePosition].isValidMove(newPiecePosition,self.getCoordinateSign(newPiecePosition),self)))
                                    self.tryTurn(player,piecePosition,newPiecePosition,king,True,False)
                                    #clear()
                                    #self.printBoard()
                                    #self.tryTurn(player.otherPlayer,"D7","D6",king,True,False)
                                    #self.printBoard()
                                    #raw_input("next->")
                                    #clear()
                                else:
                                    raise ValueError
                            else:
                                raise ValueError
                        except (ValueError, KeyError) as e:
                            pass
                        else:
                            break
                                
                else:
                    player.findBestMove(self)
    def rotateBoard(self):
        pass
    def tryTurn(self,player,piecePosition,newPiecePosition,king,check4Check,resetMoves):
        if piecePosition=="G8":
            pass
            #raw_input("G8 " + newPiecePosition + str(resetMoves))
            #raise ValueError
        otherPlayer=[p for p in self.players if p!=player][0]
        otherKing=[p for p in otherPlayer.pieces if p.name=="King"][0]
        savedPoints=player.points
        savedCapturedPieces=player.capturedPieces[:]
        capturedPiece=False
        if newPiecePosition in self.boardDict.keys() and self.boardDict[newPiecePosition].name == "King":
            raise ValueError
        if newPiecePosition in self.boardDict.keys() and self.boardDict[newPiecePosition].name != "King":
            if self.boardDict[newPiecePosition].owner==player:
                raw_input(piecePosition+" "+newPiecePosition)
                raise ValueError
            capturedPiece=True
            savedPiece = self.boardDict[newPiecePosition]
            player.points+=self.boardDict[newPiecePosition].points
            player.capturedPieces.append(self.boardDict[newPiecePosition].symbol[len(self.boardDict[newPiecePosition].symbol)-2])
            self.boardDict[newPiecePosition].owner.pieces.remove(self.boardDict[newPiecePosition])
            
        self.boardDict[piecePosition].hasMoved=True
        self.boardDict[piecePosition].position=newPiecePosition
        self.NoTheWorldMustBePeopled() 
        turnData={"pointsGained":(player.points-savedPoints),"otherKingInCheck":otherKing.isInCheck(self),"centerData":self.boardDict[newPiecePosition].controlOrInCenter(self)}
        if king.isInCheck(self) and check4Check:
            if capturedPiece:
                player.points=savedPoints
                player.capturedPieces=savedCapturedPieces
                self.boardDict[newPiecePosition].owner.pieces.append(savedPiece)
            self.boardDict[newPiecePosition].hasMoved=False
            self.boardDict[newPiecePosition].position=piecePosition
            self.NoTheWorldMustBePeopled()      
            raise ValueError
        if resetMoves:
            #raw_input(piecePosition+"  "+newPiecePosition)
            self.boardDict[newPiecePosition].position=piecePosition   
            self.NoTheWorldMustBePeopled() 
        else:
            raw_input(piecePosition+"  "+newPiecePosition)
        return [True,turnData]
def getRawMoveScore(move):
    rawPoints=move["pointsGained"]
    for info in move["centerData"]:
        if move["centerData"][info]:
            rawPoints+=3
    if move["otherKingInCheck"]:
        rawPoints+=3
    return rawPoints
def colorRow(row,rowNum):
    colorRowList=[]
    colorRowList.append(row[0])
    for i in range(1,len(row),2):
        try:
            if (rowNum % 2==0):
                colorRowList.append(Back.WHITE+row[i]+Style.RESET_ALL)
                colorRowList.append(Back.BLACK+row[i+1]+Style.RESET_ALL)
            else:
                colorRowList.append(Back.BLACK+row[i]+Style.RESET_ALL)
                colorRowList.append(Back.WHITE+row[i+1]+Style.RESET_ALL)       
        except IndexError:
            pass

    return "".join(colorRowList)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
      
      
def printBanner():
    f = open('banner.txt', 'r')
    for line in f:
        colorLine=[]
        stripLine=line.rstrip("\n")
        for i in stripLine:
            if i=="_":
                colorLine.append(Fore.BLACK+i+Style.RESET_ALL)
            else: 
                colorLine.append(Fore.WHITE+i+Style.RESET_ALL)
        
        print "".join(colorLine)
    
def main():
    if name == 'nt':
        init()
    printBanner()
    board=Board()
    board.takeTurns()
main()