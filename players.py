import random
import time
import pygame
import math
import copy
from connect4 import connect4

board_scores = [[3, 4, 5, 9, 5, 4, 3], 
				[4, 6, 7, 15, 7, 6, 4],
				[5, 7, 15, 20, 15, 7, 5],
				[5, 7, 15, 20, 15, 7, 5],
				[4, 6, 7, 15, 7, 6, 4],
				[3, 4, 5, 9, 5, 4, 3]]



class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		maxDepth = 2
		board = env.board
		player_1_played = 0
		firstRow = env.board[5]
		for col_id, element in enumerate(firstRow):
			if element == 1:
				player_1_played = col_id
		if not board.any():
			move[:] = [3]
		else:
			if self.position == 1:
				value = self.Max(env, 3, maxDepth)
			else:
				value = self.Min(env, player_1_played, maxDepth)
			move[:] = [value]

	def Max(self, env: connect4, move: int, depth: int):
		if env.gameOver(move, 2):
			return -math.inf
		if depth == 0:
			return self.evaluationFunction(env.board)
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)
		value = -math.inf
		for column in indices:
			envCopy = copy.deepcopy(env)
			self.simulateMove(envCopy, column, 1)
			new_value = self.Min(envCopy, column, depth - 1)
			if new_value > value:
				value = new_value
				end_column = column
		if depth == 2:
			return end_column
		return value
	def Min(self, env: connect4, move: int, depth: int):
		end_column = move
		if env.gameOver(move, 1):
			return math.inf
		if depth == 0:
			return self.evaluationFunction(env.board)
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)
		value = math.inf
		for column in indices:
			envCopy = copy.deepcopy(env)
			self.simulateMove(envCopy, column, 2)
			new_value = self.Max(envCopy, column, depth - 1)
			if new_value < value:
				value = new_value
				end_column = column
		if depth == 2:
			return end_column
		return value

	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
	
	def evaluationFunction(self, board) -> int:
		playerOneCount = 0
		playerTwoCount = 0
		for row_id, row in enumerate(board):
			for col_id, element in enumerate(row):
				if element == 1:
					playerOneCount = playerOneCount + board_scores[row_id][col_id]
				elif element == 2:
					playerTwoCount = playerTwoCount + board_scores[row_id][col_id]
		return playerOneCount - playerTwoCount
		

class alphaBetaAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		maxDepth = 0
		if self.position == 2:
			maxDepth = 4
		if self.position == 1:
			maxDepth = 4
		board = env.board
		player_1_played = 0
		firstRow = env.board[5]
		for col_id, element in enumerate(firstRow):
			if element == 1:
				player_1_played = col_id
		if not board.any():
			move[:] = [3]
			time.sleep(7)
		else:
			value = 0
			if self.position == 1:
				_, value = self.Max(env, 3, maxDepth, -math.inf, math.inf)
			else:
				_, value = self.Min(env, player_1_played, maxDepth, -math.inf, math.inf)
			move[:] = [value]
	def Max(self, env: connect4, move: int, depth: int, alpha: int, beta: int):
		end_column = move
		if env.gameOver(move, 2):
			return -math.inf, move
		if depth == 0:
			return self.evaluationFunction(env.board), move
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)
		value = -math.inf
		ordered_indices = []
		best_moves = []
		# order = [3, 2, 4, 1, 5, 0, 6]
		# for i in order:
		# 	if i in indices:
		# 		ordered_indices.append(i)
		for i in indices:
			top_move = env.topPosition[i]
			move_score = board_scores[top_move][i]
			best_moves.append([move_score, i])
		sorted_moves = sorted(best_moves, key=lambda x: x[0], reverse = True)
		for i in sorted_moves:
			ordered_indices.append(i[1])
		for column in ordered_indices:
			envCopy = copy.deepcopy(env)
			self.simulateMove(envCopy, column, 1)
			value, _ = self.Min(envCopy, column, depth - 1, alpha, beta)
			if value >= beta:
				return value, column
			if value > alpha:
				alpha = value
				end_column = column

		return alpha, end_column
	def Min(self, env: connect4, move: int, depth: int, alpha: int, beta: int):
		end_column = move
		if env.gameOver(move, 1):
			return math.inf, move
		if depth == 0:
			return self.evaluationFunction(env.board), move
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)
		value = math.inf
		ordered_indices = []
		order = [6, 0, 5, 1, 4, 2, 3]
		best_moves = []
		for i in indices:
			top_move = env.topPosition[i]
			move_score = board_scores[top_move][i]
			best_moves.append([move_score, i])
		sorted_moves = sorted(best_moves, key=lambda x: x[0])
		for i in sorted_moves:
			ordered_indices.append(i[1])
		for column in ordered_indices:
			envCopy = copy.deepcopy(env)
			self.simulateMove(envCopy, column, 2)
			value, _ = self.Max(envCopy, column, depth - 1, alpha, beta)
			if value <= alpha:
				return value, column
			if value < beta:
				beta = value
				end_column = column
		return beta, end_column


	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
	
	def evaluationFunction(self, board) -> int:
		playerOneCount = 0
		playerTwoCount = 0

		for row_id, row in enumerate(board):
			for col_id, element in enumerate(row):
				if element == 1:
					playerOneCount = playerOneCount + board_scores[row_id][col_id]
				elif element == 2:
					playerTwoCount = playerTwoCount + board_scores[row_id][col_id]
		return playerOneCount - playerTwoCount


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)

