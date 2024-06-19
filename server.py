import socket             
import threading
import time
from random import randint


# store board's state of the current game
# and provide helper functions...
class Play :
	def __init__(self, size, turn = 'X') -> None:
		self.turn = turn
		self.size = size
		# e : empty
		# x : player X
		# o : player O
		self.board = ['e'] * (size ** 2)
		self.active = True

	# check board to make new sent move!
	def new_move(self, move) -> bool :
		print("MOVE : " , move)
		cell = int(move[1:])
		if(self.board[cell] == 'e') :
			self.board[cell] = move[0]
			return True
		return False

	# checks that the current state is a win state or not
	# does this work using 3 other functions for each size of board
	def check_win(self) -> str :
		if (self.size == 3) :
			return self.win3()
		elif (self.size == 4) :
			return self.win4()
		elif (self.size == 5) :
			return self.win5()

	# 3*3 game winning rulse
	def win3(self) -> str:
		for i in range(3) :
			if(self.board[i] == self.board[i+3] and self.board[i+3] == self.board[i+6]) :
				if(self.board[i] != 'e') :
					return (self.board[i] + ",wins!")
			if(self.board[i*3] == self.board[i*3+1] and self.board[i*3] == self.board[i*3+2]) :
				if(self.board[i*3] != 'e') :
					return (self.board[i] + ",wins!")
		if(self.board[0] == self.board[4] and self.board[0] == self.board[8]) :
			if(self.board[0] != 'e') :
					return (self.board[0] + ",wins!")
		if(self.board[2] == self.board[4] and self.board[0] == self.board[6]) :
			if(self.board[2] != 'e') :
					return (self.board[2] + ",wins!")
		return "NO"
	
	# 4*4 game winning rulse
	def win4(self) -> str:
		for i in range(4) :
			if(self.board[i] == self.board[i+4] and self.board[i+4] == self.board[i+8]) :
				if(self.board[i] != 'e') :
					print(1111111)
					return (self.board[i] + ",wins!")
			if(self.board[i+4] == self.board[i+8] and self.board[i+8] == self.board[i+12]) :
				if(self.board[i+4] != 'e') :
					print(2222222)
					return (self.board[i+4] + ",wins!")
		for i in range(4) :
			if(self.board[i*4] == self.board[i*4+1] and self.board[i*4] == self.board[i*4+2]) :
				if(self.board[i*4] != 'e') :
					print(3333333)
					return (self.board[i*4] + ",wins!")
			if(self.board[i*4+1] == self.board[i*4+2] and self.board[i*4+1] == self.board[i*4+3]) :
				if(self.board[i*4+1] != 'e') :
					print(44444444444)
					return (self.board[i*4+1] + ",wins!")
		return "NO"

	# 5*5 game winning rulse
	def win5(self) -> str:
		for i in range(5) :
			if(self.board[i] == self.board[i+5] and self.board[i+5] == self.board[i+10] and self.board[i+5] == self.board[i+15]) :
				if(self.board[i] != 'e') :
					return (self.board[i] + ",wins!")
			if(self.board[i+5] == self.board[i+10] and self.board[i+5] == self.board[i+15] and self.board[i+5] == self.board[i+20]) :
				if(self.board[i+5] != 'e') :
					return (self.board[i+5] + ",wins!")
		for i in range(4) :
			if(self.board[i*5] == self.board[i*5+1] and self.board[i*5] == self.board[i*5+2] and self.board[i*5] == self.board[i*5+3]) :
				if(self.board[i*5] != 'e') :
					return (self.board[i*5] + ",wins!")
			if(self.board[i*5+1] == self.board[i*5+2] and self.board[i*5+1] == self.board[i*5+3] and self.board[i*5+1] == self.board[i*5+4]) :
				if(self.board[i*5+1] != 'e') :
					return (self.board[i] + ",wins!")
		return "NO"


# controls the new clients and match them for new games
class Server :
	def __init__(self) -> None :
		# temp variables for storing clients (to match them when new client connects)
		self.name3 = None
		self.name4 = None
		self.name5 = None
		self.wait3socket = None
		self.wait4socket = None
		self.wait5socket = None
		
		self.host = socket.gethostname()
		self.port = 12345
		self.BUFFER_SIZE = 1024
		self.accepter_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

	# bind socker to port 12345
	def bindd(self) -> None :
		self.accepter_socket.bind(("", self.port))  

	# socket listening on port 12345
	def listenn(self) -> None :
		self.accepter_socket.listen(10)

	# accept new connection to server and store them in waiting variables
	# if there
	def acceptt(self) -> None :
		print("server starts!\n")
		while True :
			c, addr = self.accepter_socket.accept()   
			print(c, addr)  
			print ('Got connection from', addr)
			t = threading.Thread(target = self.assign_client, args=(c,))
			t.start()

	def assign_client(self, client) -> None :

		# Receive the board size
		message = client.recv(self.BUFFER_SIZE).decode()
		print(message)
		# First message from server to client
		client.send("waiting for opponent...".encode())
		
		if (message[0] == '3') :
			if (self.name3 != None) :
				t = threading.Thread(target = self.start_game, args=(self.wait3socket, self.name3, client, message,))
				t.start()
				self.name3 = None
				self.wait3socket = None
			else :
				self.name3 = message[1:]
				self.wait3socket = client
		if (message[0] == '4') :
			if (self.name4 != None) :
				t = threading.Thread(target = self.start_game, args=(self.wait4socket, self.name4, client, message,))
				t.start()
				self.name4 = None
				self.wait4socket = None
			else :
				self.name4 = message[1:]
				self.wait4socket = client
		if (message[0] == '5') :
			if (self.name5 != None) :
				t = threading.Thread(target = self.start_game, args=(self.wait5socket, self.name5, client, message,))
				t.start()
				self.name5 = None
				self.wait5socket = None
			else :
				self.name5 = message[1:]
				self.wait5socket = client
		return
	
	# starts the game and manage it until someone wins
	# receive new choices and update the state of board
	# send new state and moves to clients...
	def start_game(self, x_socket, x_name, o_socket, o_name) :
		size = int(o_name[0])
		o_name = o_name[1:]

		time.sleep(1)
		
		print("a new game starting...")
		x_socket.send(("Found").encode())
		o_socket.send(("Found").encode())

		# Specify whose Turn
		a = randint(0,1)
		
		if(a == 1) :
			turn = 'X'
			b = 0
			board = Play(size, 'X')
		else :
			turn = 'O'
			b = 1
			board = Play(size, 'O')

		x_socket.send((o_name + "," + "X" + "," + str(a)).encode())
		o_socket.send((x_name + "," + "O" + "," + str(b)).encode())
		
		while True :
			if(turn == 'X') :
				# print("waiting for X")
				move = x_socket.recv(1024).decode()
				# print("move : " ,move)
				if(board.new_move(move)) :
					turn = 'O'
					x_socket.send((move + ",OK").encode())
					o_socket.send((move + ",OK").encode())
					who_win = board.check_win()
					if(who_win == "NO") :
						pass
					else :
						x_socket.send(who_win.encode())
						o_socket.send(who_win.encode())
						x_socket.shutdown(socket.SHUT_RDWR)
						o_socket.shutdown(socket.SHUT_RDWR)
						break
				else :
					x_socket.send(("0,invalid").encode())

			else :
				# print("waiting for O")
				move = o_socket.recv(1024).decode()
				if(board.new_move(move)) :
					turn = 'X'
					o_socket.send((move + ",OK").encode())
					x_socket.send((move + ",OK").encode())
					who_win = board.check_win()
					if(who_win == "NO") :
						pass
					else :
						x_socket.send(who_win.encode())
						o_socket.send(who_win.encode())
						x_socket.shutdown(socket.SHUT_RDWR)
						o_socket.shutdown(socket.SHUT_RDWR)
						break
				else :
					o_socket.send(("0,invalid").encode())

if __name__ == '__main__':
	s = Server()
	s.bindd()
	s.listenn()
	s.acceptt()