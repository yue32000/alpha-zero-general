from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
# from .chesslogic import Board
import chess
import pygame
import numpy as np


np.set_printoptions(threshold=sys.maxsize)
class chessgame(Game):
    # square_content = {
    #     -1: "X",
    #     +0: "-",
    #     +1: "O"
    # }

    @staticmethod
    def getSquarePiece(piece):
        # return OthelloGame.square_content[piece]
        return 0

    def __init__(self, n):
        self.n = n
        self.T = {}
        self.invT = {}
        i=0
        for n in range(1,8):
            for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
                self.T[(direction, n)] = i
                self.invT[i] = (direction, n)
                i += 1
        for direction in ["N2W1", "N1W2", "N2E1", "N1E2", "S2W1", "S1W2", "S2E1", "S1E2"]:
            self.T[(direction)] = i
            self.invT[i] = (direction, i-56)
            i+=1

        for direction in ["PU", "PL", "PR"]:
            for k in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
                self.T[(direction,k)] = i
                self.invT[i] = (direction, k)
                i+=1
        print(self.T)
        # T[("PU",chess.QUEEN)] = T[("N", 1)]
        # T[("PL",chess.QUEEN)] = T[("NW", 1)]
        # T[("PR",chess.QUEEN)] = T[("NE", 1)]




    def getInitBoard(self):
        # return initial board (numpy board)
        b = chess.Board()
        return b


    def getBoardSize(self):
        # (a,b) tuple
        return (64, 12)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n *76

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # if action == self.n*self.n:
        #     return (board, -player)
        # print("action is ", action)
        from_sq = action //76
        to_sq = 0
        plane = action%76
        if plane<56:
            if self.invT[plane][0] is "N" :
                to_sq =  from_sq + 8*self.invT[plane][1]
            elif self.invT[plane][0] is "NE":
                to_sq =  from_sq + 8*self.invT[plane][1] + self.invT[plane][1]
            elif self.invT[plane][0] is "E":
                to_sq =  from_sq + self.invT[plane][1]
            elif self.invT[plane][0] is "SE":
                to_sq =  from_sq - 8*self.invT[plane][1] + self.invT[plane][1]
            elif self.invT[plane][0] is "S":
                to_sq =  from_sq - 8*self.invT[plane][1]
            elif self.invT[plane][0] is "SW":
                to_sq =  from_sq - 8*self.invT[plane][1] - self.invT[plane][1]
            elif self.invT[plane][0] is "W":
                to_sq =  from_sq - self.invT[plane][1]
            elif self.invT[plane][0] is "NW":
                to_sq =  from_sq + 8*self.invT[plane][1] - self.invT[plane][1]
            else:
                print("ERROR in encode plane<56")
        elif plane < 64:
            # print(plane)
            # print (self.invT[plane][0])
            if self.invT[plane][0] is "N2W1" :
                to_sq =  from_sq + 8*2 - 1
            elif self.invT[plane][0] is "N1W2":
                to_sq =  from_sq + 8 -2 
            elif self.invT[plane][0] is "N2E1":
                to_sq =  from_sq + 8*2 + 1
            elif self.invT[plane][0] is "N1E2":
                to_sq =  from_sq + 8 + 2
            elif self.invT[plane][0] is "S2W1":
                to_sq =  from_sq - 8*2 - 1
            elif self.invT[plane][0] is "S1W2":
                to_sq =  from_sq - 8 - 2
            elif self.invT[plane][0] is "S2E1":
                to_sq =  from_sq - 8*2 + 1
            elif self.invT[plane][0] is "S1E2":
                to_sq =  from_sq - 8 + 2
            else:
                print("ERROR in encode plane<64")
        elif plane < 76:
            if board.turn is chess.WHITE:
                if self.invT[plane][0] is "PU":
                    to_sq =  from_sq + 8
                elif self.invT[plane][0] is "PL":
                    to_sq =  from_sq + 8 - 1
                elif self.invT[plane][0] is "PR":
                    to_sq =  from_sq + 8 + 1
                else:
                    print("ERROR in encode plane<76, white")
            elif board.turn is chess.BLACK:
                if self.invT[plane][0] is "PU":
                    to_sq =  from_sq - 8
                elif self.invT[plane][0] is "PL":
                    to_sq =  from_sq - 8 - 1
                elif self.invT[plane][0] is "PR":
                    to_sq =  from_sq - 8 + 1
                else:
                    print("ERROR in encode plane<76, white")
        else:
                print("ERROR in encode plane, plane exceed 76")





        # print("from_sq  is ", from_sq)
        # print("to_sq is ", to_sq)
        move = None
        for m in board.legal_moves:
            # print(m)
            # print (m.from_square)
            # print (m.to_square)
            if m.from_square == from_sq and m.to_square == to_sq:
                move = m

        # if move is None:
        #     for m in board.legal_moves:
                # print(m)
                # print (m.from_square)
                # print (m.to_square)


        # move = chess.Move.from_uci(action)
        board.push(move)
        return (board, board.turn)






    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        # valids = [0]*self.getActionSize()
        # b = Board(self.n)
        # b.pieces = np.copy(board)
        # legalMoves =  b.get_legal_moves(player)
        # if len(legalMoves)==0:
        #     valids[-1]=1
        #     return np.array(valids)
        # for x, y in legalMoves:
        #     valids[self.n*x+y]=1
        # return np.array(valids)
        return  self.encodemove(board, board.legal_moves)

        # return np.array(board.legalMoves)
    def encodemove(self, board, move):


        encode_m = np.zeros((64,76))
        for m in move:
            f = m.from_square
            t = m.to_square
            # print("f is %s", f)
            # print("t is %s", t)
            if board.piece_at(f).piece_type is chess.KNIGHT: 
                if (f<t):
                    if (f%8- t%8 == 1):
                        d = "N2W1"
                    elif (f%8 - t%8 == 2):
                        d = "N1W2"
                    elif (t%8 - f%8 == 1):
                        d = "N2E1"
                    elif (t%8 - f%8 == 2):
                        d = "N1E2"
                    else:
                        print ("ERROR encode move failed in case 1/1")
                elif (f>t):
                    if (f%8- t%8 == 1):
                        d = "S2W1"
                    elif (f%8 - t%8 == 2):
                        d = "S1W2"
                    elif (t%8 - f%8 == 1):
                        d = "S2E1"
                    elif (t%8 - f%8 == 2):
                        d = "S1E2"
                    else:
                        print ("ERROR encode move failed in case 1/2")
                else:
                        print ("ERROR encode move failed in case 1/3")
                encode_m[f][self.T[d]]=1

            elif m.promotion is not None:
                if (f%8==t%8):
                    d = "PU"
                elif (f%8<t%8):
                    d = "PR"
                elif (f%8 > t%8):
                    d = "PL"
                else:
                    print ("ERROR: encode move failed in case 2")
# chess.KNIGHT: chess.PieceType= 2
# chess.BISHOP: chess.PieceType= 3
# chess.ROOK: chess.PieceType= 4
# chess.QUEEN: chess.PieceType= 5
                encode_m[f][self.T[(d,m.promotion)]] = 1

            else:
                if (f>t and f%8==t%8): #
                    d = "S"
                elif (f<t and f%8 == t%8): #S
                    d = "N"
                elif (f>t and f//8==t//8): #E
                    d = "W"
                elif (f<t and f//8==t//8):
                    d= "E"
                elif (f<t and f%8 > t%8):
                    d = "NW"
                elif (f<t and f%8 < t%8):
                    d = "NE"
                elif (f>t and f%8 > t%8):
                    d = "SW"
                elif (f>t and f%8 < t%8):
                    d = "SE"
                else:
                    print ("ERROR, decodeing move failed")

                if d is "S" or d is "N":
                    sqs = abs(f//8 - t//8)
                else:
                    sqs = abs(f%8 - t%8)
                # print ("d is %s", d)
                # print ("sqs is %s", sqs)
                encode_m[f][self.T[(d,sqs)]] = 1
        # print (encode_m)
        # input("Press Enter to continue...")
        return encode_m.reshape(64*76)



        # print move.uci()
        # if player is white:
        #     piece = board.pieces_at(move.from_square).

    def encodeboard(self, board, curPlayer):
        r=0 #0,1
        b=2 #2,3
        n=4 #4,5
        k=6 #6,7
        q=8 #8,9
        p=10 #10,11
        # p=8 #8-15


        # R=16 #16,17
        # B=18 #18,19
        # N=20 #20,21
        # K=22
        # Q=23
        # P=24 #24-31

        encode_b = np.zeros((64,12))

        for i in range(0,64):
            piece = board.piece_at(i)
            if piece is not None:
                if piece.color is curPlayer:
                    if(piece.piece_type is chess.ROOK):
                        encode_b[i][r]=1
                        
                    elif(piece.piece_type is chess.BISHOP):
                        encode_b[i][b]=1
                        
                    elif(piece.piece_type is chess.KNIGHT):
                        encode_b[i][n]=1
                        
                    elif(piece.piece_type is chess.QUEEN):
                        encode_b[i][q]=1
                    elif(piece.piece_type is chess.KING):
                        encode_b[i][k]=1
                    elif(piece.piece_type is chess.PAWN):
                        encode_b[i][p]=1
    
                # elif piece.color is chess.BLACK:
                else:
                    if(piece.piece_type is chess.ROOK):
                        encode_b[i][r+1]=1
                        
                    elif(piece.piece_type is chess.BISHOP):
                        encode_b[i][b+1]=1
                        
                    elif(piece.piece_type is chess.KNIGHT):
                        encode_b[i][n+1]=1
                    elif(piece.piece_type is chess.QUEEN):
                        encode_b[i][q+1]=1
                    elif(piece.piece_type is chess.KING):
                        encode_b[i][k+1]=1
                    elif(piece.piece_type is chess.PAWN):
                        encode_b[i][p+1]=1
        # print(encode_b)
        # input("Press Enter to continue...")
        return encode_b.reshape(64*12)







    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        # b = Board(self.n)
        # b.pieces = np.copy(board)
        # if b.has_legal_moves(player):
        #     return 0
        # if b.has_legal_moves(-player):
        #     return 0
        # if b.countDiff(player) > 0:
        #     return 1
        # return -1

        # if not board.is_variant_end():
        #     return -2
        # elif board.is_variant_win():
        #     return 1
        # elif board.is_variant_loss():
        #     return -1
        # elif board.is_variant_draw() :
        #     return 0

        status =  board.outcome(claim_draw=True)
        if status is None:
            return -2
        elif status.termination == chess.Termination.CHECKMATE:
            return -1
        else:
            return 0
        # elif status.termination ==  chess.STALEMATE or status.termination ==  chess.STALEMATE
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board

    def getSymmetries(self, board, pi, curPlayer):
        # mirror, rotational
        # assert(len(pi) == self.n**2+1)  # 1 for pass
        # pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        l += [(self.encodeboard(board, curPlayer),pi)]

        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(board, i)
        #         newPi = np.rot90(pi_board, i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(newPi)
        #         l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # print(board.board_fen())
        if (board.turn):
            return board.board_fen()+"w"
        else:
            return board.board_fen()+"b"

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    def updatedisplay(self, board):
        WIN.fill((0,0,0))
        size = 100
        cnt = 0
        for i in range(0,8):
            for z in range(0,8):
            #check if current loop value is even
                if cnt % 2 == 0:
                    pygame.draw.rect(WIN, (0,0,0),[size*z,size*i,size,size])
                else:
                    pygame.draw.rect(WIN, (128,128,128), [size*z,size*i,size,size])
                cnt +=1
            #since theres an even number of squares go back one value
            cnt-=1

        for i in range(0,64):
            piece = board.piece_at(i)
            if piece is not None:
                if piece.color is chess.WHITE:
                    if(piece.piece_type is chess.ROOK):
                        pic = pygame.image.load("pic\\wrook.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))
                        
                        
                    elif(piece.piece_type is chess.BISHOP):
                        pic = pygame.image.load("pic\\wbishop.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                        
                    elif(piece.piece_type is chess.KNIGHT):
                        pic = pygame.image.load("pic\\wknight.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                    
                        
                    elif(piece.piece_type is chess.QUEEN):
                        pic = pygame.image.load("pic\\wqueen.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                    elif(piece.piece_type is chess.KING):
                        pic = pygame.image.load("pic\\wking.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                    elif(piece.piece_type is chess.PAWN):
                        pic = pygame.image.load("pic\\wpawn.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
    
                # elif piece.color is chess.BLACK:
                else:
                    if(piece.piece_type is chess.ROOK):
                        pic = pygame.image.load("pic\\brook.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                        
                    elif(piece.piece_type is chess.BISHOP):
                        pic = pygame.image.load("pic\\bbishop.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                        
                    elif(piece.piece_type is chess.KNIGHT):
                        pic = pygame.image.load("pic\\bknight.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                    elif(piece.piece_type is chess.QUEEN):
                        pic = pygame.image.load("pic\\bqueen.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                    elif(piece.piece_type is chess.KING):
                        pic = pygame.image.load("pic\\bking.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
                    elif(piece.piece_type is chess.PAWN):
                        pic = pygame.image.load("pic\\bpawn.png").convert_alpha()
                        pic = pygame.transform.scale(pic, (100,100))
                        WIN.blit(pic, (100*(i%8),100*(i//8)))                        
        
        # pic = pygame.image.load("pic\\wking.png").convert_alpha()
        # pic = pygame.transform.scale(pic, (100,100))

        # WIN.blit(pic, (0,0))
        pygame.display.update()
        click = False
        while not click:
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONUP:
                    click = True


    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                print(OthelloGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")
