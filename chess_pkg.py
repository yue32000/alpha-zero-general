import chess
from numpy import array
import numpy as np
def print_moves(board):
	print(board)
	print(board.board_fen())
	for i in board.legal_moves:
		print (i)
		sq = i.from_square
		print (sq)
		# print (i.to_square)
# board = chess.Board()

def move_board(board):
	for i in board.legal_moves:
		move = i
	board2 = board.copy()
	board2.push(move)
	print(board2)
	return board2

# def current_state(board):
#     s = []
#     for i in str(board):

#         if i != " ":

#             y = ' '.join(format(ord(i), 'b'))
#             print (y)
#             x = ""
#             for i in y:
#                 if i != " ": x += i
#             x = int(x)
#             s.append(x)
#     s.append(1)
#     a = array( s )
#     return a


board = chess.Board()
print(board)
print(id(board))
board2 = move_board(board)
print(board)
print(id(board2))

l = np.array([1,2,3])
print (l[0])
print (l[:-1])
# print(board.legal_moves)
# print (board.unicode)
# print (current_state(board))

# print (board.piece_at(0))
# print_moves(board)

# # for i in range(0,8):
# # 	for j in range(0,8):
# # 		if (board.piece_at(i*8+j) is not None):
# # 			print (board.piece_at(i*8+j))

# move = chess.Move.from_uci("g1h3")
# board.push(move)

# print_moves(board)



