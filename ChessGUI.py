#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from Chess import *


class Application(Frame):
    def pieceClicked(self,coord):
        if coord in self.board.boardDict.keys() and self.board.boardDict[coord].color == self.board.currentPlayer:
            if self.firstClick and self.buttons[coord]["bg"] != "green":
                self.buttons[coord]["relief"] = "sunken"
                self.buttons[coord]["bg"] = "green"
                self.firstClick = False
                self.selectedPiece = coord
                if self.showMoves:
                    for iterPosition in [letter + str(number) for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] for letter in "ABCDEFGH"]:         
                        if self.board.boardDict[self.selectedPiece].isValidMove(iterPosition, self.board.getCoordinateSign(iterPosition), self.board):
                            self.buttons[iterPosition]["bg"] = "yellow"
            else:
                self.buttons[coord]["relief"] = "raised"
                self.buttons[coord]["bg"] = self.buttonsLastColor[coord]
                self.firstClick = True
                self.selectedPiece = ""
                for position in self.buttons:
                    if self.buttons[position]["bg"] == "yellow":
                        self.buttons[position]["bg"] = self.buttonsLastColor[position]
        if not self.firstClick:
            if self.board.boardDict[self.selectedPiece].isValidMove(coord, self.board.getCoordinateSign(coord), self.board):
                self.board.tryTurn(self.board.boardDict[self.selectedPiece].owner, self.selectedPiece, coord, self.board.boardDict[self.selectedPiece].owner.king, True, False, True, 1)
                if self.board.currentPlayer == "White":
                    self.board.currentPlayer = "Black"
                else:
                    self.board.currentPlayer = "White"
                self.createWidgets()  
                self.firstClick = True
            
            
    def createWidgets(self):        
        self.buttons = {}
        self.buttonsLastColor = {}
        self.board.NoTheWorldMustBePeopled()
        turnDisplayText= "   " + self.board.currentPlayer + "'s turn!\n"
        for p in self.board.players:
            turnDisplayText += p.color+"'s Points  =  "+str(p.points)+"\n"    
        self.playerTurnDisplay=Label(self, text= turnDisplayText, font="TkFixedFont")
        self.playerTurnDisplay["borderwidth"] = 10
        self.playerTurnDisplay.grid(row=0, column=2, columnspan=7, sticky=N+E+S+W)        
        for i in range(len(self.board.board)-1):
            b = Button(self, text=self.board.board[i][0], font='TkFixedFont', borderwidth=4, relief="groove")
            b.grid(row=i+1, column=1)             
            for j in range(1, len(self.board.board[i])):
                coord = "ABCDEFGH"[j-1]+str(int(self.board.board[i][0][1:3]))
                b = Button(self, text= self.board.getCoordinateSign(coord) ,font='TkFixedFont', borderwidth=4, relief="groove", command=lambda coord=coord:self.pieceClicked(coord))
                #b.bind("<Enter>", self.pieceClicked)
                if coord in self.board.boardDict.keys() and self.board.boardDict[coord].color == "Black":
                    b["fg"] = "red"
                if coord in self.board.boardDict.keys() and self.board.boardDict[coord].color == "White":
                    b["fg"] = "blue"
                blackCheckers=["ABCDEFGH".index(coord[0]) % 2 != 0 and int(coord[1:]) % 2 == 0, "ABCDEFGH".index(coord[0]) % 2 == 0 and int(coord[1:]) % 2 != 0]
                if any(blackCheckers) and not all(blackCheckers):
                    b["bg"] = "black"
                if self.board.getCoordinateSign(coord) == " X ":
                    b["bg"] = "red"
                    b["fg"] = "black"     
                b.grid(row=i+1, column=j+1) 
                self.buttons[coord] = b
                self.buttonsLastColor[coord] = b["bg"]
        for i in range(len(self.board.board[-1])):
            b = Button(self, text=self.board.board[-1][i], font='TkFixedFont', borderwidth=4, relief="groove")
            b.grid(row=len(self.board.board), column=i+1)     

 
  
    def swapShowMoves(self):
        self.showMoves = not self.showMoves
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.buttons={}
        self.board=Board()
        #self.board.useUnicodePieces()
        self.board.currentPlayer="White"
        self.title="Thud!"
        self.createWidgets()
        self.showMoves=False
        self.showMovesButton = Checkbutton(self,text="Show avilable moves on piece selection.", borderwidth=4 ,relief="sunken",command=self.swapShowMoves )
        self.showMovesButton.grid(row=17, column=2, columnspan=14, sticky=N+E+S+W) 
        self.firstClick=True
        self.selectedPiece=""
        


#board = Board()
if __name__ == "__main__":
    root = Tk()   
    root.geometry="2000x1500"
    app = Application(master=root)
    app.mainloop()
    root.destroy()
