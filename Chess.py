from colorama import Fore, Style, Back, init
from os import system, name
class Piece:
    def __init__(self,name,color,symbol,moves,position):
        self.name=name
        self.color=color
        self.symbol=symbol
        self.moves=moves
        self.position=position
    def move(self):
        if self.name=="Pawn":
            pass#self.position
class player:
    def __init__(self,color):
        self.color=color
        #pieces=[Piece("pawn",color,p,)]
class Board:    
    def __init__(self):
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
        self.timesHit=0
        self.shipsCovering=17
    def printBoard(self):
        for i in range(len(self.board)-1):
            print colorRow(self.board[i],i)
        print "".join(self.board[8])
    def addShip(self,spot,direction,ship):      
        if (direction.upper()=="R"):
            if (self.board[0].index("["+str(spot[0]).upper()+"]")+self.Ships[ship].length<10):
                for i in range(0,self.Ships[ship].length):
                    self.changeCoordinateSign(self.incrementCoordinate(spot,direction,i),"[+]")
                    self.Ships[ship].updateSpotsOccupied(str(self.board[0][self.board[0].index("["+str(spot[0]).upper()+"]")+i][1]+spot[1:])[:-1])
            else:
                for i in range(0,self.Ships[ship].length):
                    self.changeCoordinateSign(self.incrementCoordinate((" ABCDEFGHIJ"[11-self.Ships[ship].length]+spot[1:]),direction,i),"[+]")
                    
                    self.Ships[ship].updateSpotsOccupied(str(self.board[0][11-self.Ships[ship].length+i][1]+spot[1:])[:-1])
        else:
            if ((int(spot[1:])+self.Ships[ship].length)<10):
                for i in range(0, self.Ships[ship].length):
                    self.changeCoordinateSign(self.incrementCoordinate(spot,direction,i),"[+]")
                    self.Ships[ship].updateSpotsOccupied(str(spot[0]).upper()+str(int(spot[1:])+i))
            else:
                for i in range(0, self.Ships[ship].length):
                    self.changeCoordinateSign(self.incrementCoordinate(str(spot[0]).upper()+str(int(11-self.Ships[ship].length)),direction,i),"[+]")                    
                    self.Ships[ship].updateSpotsOccupied(str(spot[0]).upper()+str(11-self.Ships[ship].length+i))



    def youSunkMyBattleShip(self):
        for ship in self.Ships:
            sunk=True
            for spot in self.Ships[ship].spotsOccupied:
                if self.getCoordinateSign(spot)=="[+]":
                    sunk=False
            if sunk:
                return True               
    def getCoordinateSign(self,spot):
        return self.board[int(spot[1:])][self.board[0].index("["+str(spot[0]).upper()+"]")]
    def changeCoordinateSign(self,spot,sign):
        self.board[int(spot[1:])][self.board[0].index("["+str(spot[0]).upper()+"]")] = sign
    def incrementCoordinate(self,spot,direction,increment):
        alphabet=" ABCDEFGHIJ"
        if direction.upper()=="R":
            return alphabet[alphabet.index(spot[0].upper())+increment]+spot[1:]
        else:
            return spot[0]+str(int(spot[1:])+increment)


def colorRow(row,rowNum):
    colorRowList=[]
    colorRowList.append(row[0])
    for i in range(1,len(row),2):
        try:
            if (rowNum % 2==0):
                colorRowList.append(Back.BLACK+row[i]+Style.RESET_ALL)
                colorRowList.append(Back.WHITE+row[i+1]+Style.RESET_ALL)
                
            else:
            
                colorRowList.append(Back.WHITE+row[i]+Style.RESET_ALL)
                colorRowList.append(Back.BLACK+row[i+1]+Style.RESET_ALL)        
        except IndexError:
            pass
    """
    for i in row:
        if(i=="[x]"):
            colorRowList.append(Fore.RED+i+Fore.RESET)
        elif(i=="[+]"):
            colorRowList.append(Fore.GREEN+i+Fore.RESET)
        elif(i=="[0]"):
            colorRowList.append(Fore.YELLOW+i+Fore.RESET)
        elif(i=="[o]"):
            colorRowList.append(Fore.BLUE+i+Fore.RESET)
        elif(i=="[?]"):
            colorRowList.append(Fore.CYAN+i+Fore.RESET)
        else:
            colorRowList.append(Fore.WHITE+i+Fore.RESET)
    """
    return "".join(colorRowList)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
      
      
def main():
    init()
    board=Board()
    board.printBoard()
main()