from colorama import Fore, Style, Back, init
from os import system, name
class Piece:
    def __init__(self,owner,color,position):
        self.color=color
        self.position=position
        self.hasMoved=False
        self.owner=owner
class Pawn(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=Fore.BLUE+" P "
        else:           
            self.symbol=Fore.RED+" P "
        self.name="Pawn"
        self.points=1
    def isValidMove(self,position,positionSymbol,b):           
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
                return True
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
            self.symbol=Fore.BLUE+" R "
        else:           
            self.symbol=Fore.RED+" R "
        self.name="Rook"
        self.points=5
    def isValidMove(self,position,positionSymbol,board):           
        increment=1
        if position[1]==self.position[1]:#horizontal
            if "ABCDEFGH".index(position[0])>"ABCDEFGH".index(self.position[0]):
                increment=-1            
            for i in range("ABCDEFGH".index(self.position[0]),"ABCDEFGH".index(position[0]),increment):
                if board.getCoordinateSign("ABCDEFGH"[i]+position[1])!="   ":
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
            self.symbol=Fore.BLUE+" N "
        else:           
            self.symbol=Fore.RED+" N "
        self.name="Knight"
        self.points=3
    def isValidMove(self,position,positionSymbol,board):           
        validMoves=[[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]] #list of moves in terms of [h,v], horizontal movement, vertical movement
        for move in validMoves:
            if position=="ABCDEFGH"["ABCDEFGH".index(self.position[0])+move[0]]+str(int(self.position[1])+move[1]):
                return True
        return False
class Bishop(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=Fore.BLUE+" B "
        else:           
            self.symbol=Fore.RED+" B "
        self.name="Bishop"
        self.points=3
    def isValidMove(self,position,positionSymbol,board):           
        direction=[[1],[1]]#increment in [h,v] horizontal, vertical
        direction[0]=-("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))/abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))
        direction[1]=-(int(self.position[1])-int(position[1]))/abs(int(self.position[1])-int(position[1]))
        if abs(int(self.position[1])-int(position[1]))==abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0])):
            for i in range(1,abs(int(self.position[1])-int(position[1]))):
                if board.getCoordinateSign("ABCDEFGH"["ABCDEFGH".index(self.position[0])+(i*direction[0])]+str(int(self.position[1])+(i*direction[1])))!="   ":
                    return False
            return True
        return False
            
class Queen(Piece):
    def __init__(self,owner,color,position):
        Piece.__init__(self,owner,color,position)
        if self.color=="White":
            self.symbol=Fore.BLUE+" Q "
        else:           
            self.symbol=Fore.RED+" Q "
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
            self.symbol=Fore.BLUE+" K "
        else:           
            self.symbol=Fore.RED+" K "
        self.name="King"
        self.points=100
    def isValidMove(self,position,positionSymbol,board):           
        if (abs("ABCDEFGH".index(self.position[0])-"ABCDEFGH".index(position[0]))<=1) and (abs(int(self.position[1])-int(position[1]))<=1):
            for player in board.players:
                if player.color!=self.color:
                    for piece in player.pieces:
                        try:
                            if piece.name!="King" and piece.isValidMove(position," K ",board):
                                return False
                        except (IndexError,ZeroDivisionError):
                            pass                         
            return True
        return False
#For king, use board to look through other players pieces to find out if his position is a valid move for them
class Player:               
    def __init__(self,color):
        self.turnComplete=False
        self.color=color
        self.points=0
        self.capturedPieces=[]
        if self.color=="White":
            self.pieces=[Pawn(self,self.color,"A2"),Pawn(self,self.color,"B2"),Pawn(self,self.color,"C2"),Pawn(self,self.color,"D2"),Pawn(self,self.color,"E2"),Pawn(self,self.color,"F2"),Pawn(self,self.color,"G2"),Pawn(self,self.color,"H2"),Rook(self,self.color,"A1"),Knight(self,self.color,"B1"),Bishop(self,self.color,"C1"),Queen(self,self.color,"D1"),King(self,self.color,"E1"),Bishop(self,self.color,"F1"),Knight(self,self.color,"G1"),Rook(self,self.color,"H1")]
        else:
            self.pieces=[Pawn(self,self.color,"A7"),Pawn(self,self.color,"B7"),Pawn(self,self.color,"C7"),Pawn(self,self.color,"D7"),Pawn(self,self.color,"E7"),Pawn(self,self.color,"F7"),Pawn(self,self.color,"G7"),Pawn(self,self.color,"H7"),Rook(self,self.color,"A8"),Knight(self,self.color,"B8"),Bishop(self,self.color,"C8"),Queen(self,self.color,"D8"),King(self,self.color,"E8"),Bishop(self,self.color,"F8"),Knight(self,self.color,"G8"),Rook(self,self.color,"H8")]
class Board:    
    def __init__(self):
        self.board=[]
        self.players=[Player("White"),Player("Black")]

        self.boardDict={}
        self.NoTheWorldMustBePeopled()
    def printBoard(self):
        for i in range(len(self.board)-1):
            print colorRow(self.board[i],i)
        print "".join(self.board[8])
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
        while True:
            for player in self.players:
                while True:
                    try:
                        clear()
                        self.printBoard()
                        print player.color +"'s Turn"                        
                        piecePosition=raw_input("Please choose one of your pieces(ex:a2)\n->").rstrip("\r").upper()
                        if self.boardDict[piecePosition].color!=player.color:
                            raise ValueError
                        correctPiece=raw_input("You have chosen your "+self.boardDict[piecePosition].name+" at "+piecePosition+". Is this correct(y/n)?\n->")
                        if correctPiece[0].upper()=="Y":
                            newPiecePosition=raw_input("Where would you like to move it(ex:a3)?\n->").rstrip("\r").upper()
                            correctPieceMove=raw_input("You have chosen to move your "+self.boardDict[piecePosition].name+" from "+piecePosition+" to "+newPiecePosition+". Is this correct(y/n)?\n->")
                            if correctPieceMove[0].upper()=="Y" and self.boardDict[piecePosition].isValidMove(newPiecePosition,self.getCoordinateSign(newPiecePosition),self):
                                if newPiecePosition in self.boardDict.keys():
                                    if self.boardDict[newPiecePosition].owner==player:
                                        raise ValueError
                                    self.boardDict[newPiecePosition].owner.pieces.remove(self.boardDict[newPiecePosition])
                                    
                                self.boardDict[piecePosition].hasMoved=True
                                self.boardDict[piecePosition].position=newPiecePosition
                                self.NoTheWorldMustBePeopled() 
                                
                            else:
                                raise ValueError
                        else:
                            raise ValueError
                        
                    except (ValueError, KeyError) as e:
                        #print e
                       # raw_input(2)
                        pass

                    else:
                        break
                            
                            
                player.turnComplete=False        
    def rotateBoard(self):
        pass
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
      
      
def main():
    init()
    board=Board()
    board.takeTurns()
main()