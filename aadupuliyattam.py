import random
from copy import deepcopy
import time
import math

class BaghChal:
    def __init__(self, a1, a2):

        # Create a 5x5 board filled with None
        self.board = [['*' for _ in range(5)] for _ in range(5)]

        # Place the tigers at the four corners
        self.board[0][0] = 'T'
        self.board[0][4] = 'T'
        self.board[4][0] = 'T'
        self.board[4][4] = 'T'

        # Initialize the number of goats
        self.goats = 20
        self.goats_captured = 0
        
        # Initialize the current player
        self.current_player = 'G'
        if a1.player=='G':
            self.goat_player=a1
            self.tiger_player=a2
        else:
            self.goat_player=a2
            self.tiger_player=a1
        
        self.game_winner=None
        
    def print_board(self):
        print("    0      1      2      3      4")
        print("  -----------------------------------")
        for row in range(5):
            print(row, end='')
            for col in range(5):
                if self.board[row][col] is None:
                    print("|   ", end='\t')
                else:
                    print("|  " + self.board[row][col], end='   ')
            print("|")
            print("  -----------------------------------")
        
        print("Goats Captured: "+str(self.goats_captured))
        print("Goats Remaining: "+str(self.goats))  
        print()
    
    def get_state(self):
        return {'board':self.board,'goats':self.goats,'goats_captured':self.goats_captured,'current_player':self.current_player}
        
    def game(self):
        iter=0
        while(iter<100):
            self.print_board()
            
            if self.current_player == 'G':
                choice = self.goat_player.next_move(deepcopy(self.get_state()))
            else:         
                choice = self.tiger_player.next_move(deepcopy(self.get_state()))
           
            if len(choice)==2:
                start_row, start_col, end_row, end_col = choice[0],choice[1],None,None
            else:
                start_row, start_col, end_row, end_col = choice[0],choice[1],choice[2],choice[3]
            
            # print("before game update")
            # self.print_board()
            # if self.current_player == 'T':
            #     print("Tiger's Move")
            # else:
            #     print("Goat's Move")
            # print(start_row,start_col,end_row,end_col)
            
            if end_row==None:
                if self.goats<0:
                    print("Invalid move. Try again.")
                else: 
                    self.board[start_row][start_col] == '*'
                    self.board[start_row][start_col] = 'G'
                    self.goats -= 1
                    self.current_player = 'T' if self.current_player == 'G' else 'G'
            else:
                if self.valid_move(start_row, start_col, end_row, end_col):
                    self.result([start_row, start_col, end_row, end_col])
                    
                    # Account for tigers capturing goats
                    self.current_player = 'T' if self.current_player == 'G' else 'G'
                else:
                    print("Invalid move. Try again.")
                    
            if self.end_state()==True: 
                self.print_board()      
                # Display Winner
                if self.game_winner == 'T':
                    print("Tigers win!")
                elif self.game_winner == 'G':
                    print("Goats win!")
                return self.game_winner
            iter+=1
        print("Draw")
        return "Draw"
                   
    
    def valid_move(self, start_row, start_col, end_row, end_col,current_player=None):
        if current_player==None:
            current_player=self.current_player
        # Check if the start and end squares are on the board
        if not (0 <= start_row < 5 and 0 <= start_col < 5 and 0 <= end_row < 5 and 0 <= end_col < 5):
            return False

        # Check if the start square contains the current player's piece
        if self.board[start_row][start_col] != current_player:
            return False

        # Check if the end square is empty
        if self.board[end_row][end_col] !='*':
            return False

        if current_player == 'G':
            # Goats can only move to adjacent squares
            if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
                return False
        else:
            # Tigers can move to adjacent squares or jump over goats
            if abs(start_row - end_row) > 2 or abs(start_col - end_col) > 2:
                return False
            if abs(start_row - end_row) == 2 or abs(start_col - end_col) == 2:
                # If the tiger is jumping, there must be a goat in between
                if self.board[(start_row + end_row) // 2][(start_col + end_col) // 2] != 'G':
                    return False
                

        return True
    def result(self,move):
        
        if move[2]==None:
            self.board[move[0]][move[1]] = 'G'
            self.goats -= 1
            return
            
        else:
            if self.current_player=='G':
                self.board[move[2]][move[3]] = 'G'
            else:
                self.board[move[2]][move[3]] = 'T'
            self.board[move[0]][move[1]] = '*'
            
            # Check if the tiger captured a goat
            if abs(move[0] - move[2]) == 2 or abs(move[1] - move[3]) == 2:
                self.goats_captured += 1
                self.board[(move[0] + move[2]) // 2][(move[1] + move[3]) // 2] = '*'  # Remove the goat from the board
            return
            
    def end_state(self):
        # Check if 5 or more goats have been captured
        if self.goats_captured >= 5:
            self.game_winner='T'  # Tigers win
            return True

        # Check if the tigers can make a move
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == 'T':
                    # Check all adjacent squares and jumps
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
                        new_row, new_col = row + dr, col + dc
                        if self.valid_move(row, col, new_row, new_col,'T'):
                            return False  # Game continues

        self.game_winner='G' # Goats win
        return True  

class human_agent():
    def __init__(self,player):
        self.player=player
    
    def get_move(self):
        move = input("Enter your move (row, col): ")
        row, col = map(int, move.split(','))               
        return (row, col)
    
    def next_move(self,state):
        start_row, start_col, end_row, end_col = None, None, None, None
        if self.player == 'G':
            if state['goats'] > 0:
                # If there are still goats to be placed
                print("Goat's turn. Choose a square to place a new goat.")
                while(True):
                    start_row, start_col = self.get_move()
                    if state['board'][start_row][start_col] == '*':
                        break
                    else:
                        print("Invalid move. Try again.")
            else:
                # If all goats have been placed, they can move
                while(True):
                    print("Goat's turn. Choose a goat to move.")
                    start_row, start_col = self.get_move()
                    print("Choose a square to move to.")
                    end_row, end_col = self.get_move()
                    if self.valid_move(start_row, start_col, end_row, end_col,state['board'],'G'):
                        break
                    else:
                        print("Invalid move. Try again.")
        else:
            # Code for the tigers' turn
            while(True):
                print("Tiger's turn. Choose a tiger to move.")
                start_row, start_col = self.get_move()
                print("Choose a square to move to.")
                end_row, end_col = self.get_move()
                if self.valid_move(start_row, start_col, end_row, end_col,state['board'],'T'):
                    break
                else:
                        print("Invalid move. Try again.")
                         
        return (start_row, start_col, end_row, end_col)
                 
    def valid_move(self, start_row, start_col, end_row, end_col,board,current_player=None):
        if current_player==None:
            current_player=self.player
        # Check if the start and end squares are on the board
        if not (0 <= start_row < 5 and 0 <= start_col < 5 and 0 <= end_row < 5 and 0 <= end_col < 5):
            return False

        # Check if the start square contains the current player's piece
        if board[start_row][start_col] != current_player:
            return False

        # Check if the end square is empty
        if board[end_row][end_col] !='*':
            return False

        if current_player == 'G':
            # Goats can only move to adjacent squares
            if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
                return False
        else:
            # Tigers can move to adjacent squares or jump over goats
            if abs(start_row - end_row) > 2 or abs(start_col - end_col) > 2:
                return False
            if abs(start_row - end_row) == 2 or abs(start_col - end_col) == 2:
                # If the tiger is jumping, there must be a goat in between
                if board[(start_row + end_row) // 2][(start_col + end_col) // 2] != 'G':
                    return False

        return True

class random_agent():
    def __init__(self,player):
        self.player=player
    
    def next_move(self,state):
        valid_moves=self.get_valid_moves(state)
        choice=random.choice(valid_moves)
        return (choice[0],choice[1],choice[2],choice[3])
    
    def get_valid_moves(self,state,current_player=None):
        if current_player==None:
            current_player=self.player
        valid_moves=[]
        board=state['board']
        if current_player == 'G':
            if state['goats'] > 0:
                # If there are still goats to be placed
                for row in range(5):
                    for col in range(5):
                        if board[row][col] == '*':
                            valid_moves.append((row,col,None,None))
            else:
                # If all goats have been placed, they can move
                for row in range(5):
                    for col in range(5):
                        if board[row][col] == current_player:
                            # Check all adjacent squares
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = row + dr, col + dc
                                if self.valid_move(row, col, new_row, new_col,board,'G'):
                                    valid_moves.append((row,col,new_row,new_col))
                                    
        elif current_player == 'T':
            for row in range(5):
                for col in range(5):
                    if board[row][col] == current_player:
                        # Check all adjacent squares and jumps
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
                            new_row, new_col = row + dr, col + dc
                            if self.valid_move(row, col, new_row, new_col,board,'T'):
                                valid_moves.append((row,col,new_row,new_col))
        return valid_moves
    
    def valid_move(self, start_row, start_col, end_row, end_col,board,current_player=None):
        if current_player==None:
            current_player=self.player
        # Check if the start and end squares are on the board
        if not (0 <= start_row < 5 and 0 <= start_col < 5 and 0 <= end_row < 5 and 0 <= end_col < 5):
            return False

        # Check if the start square contains the current player's piece
        if board[start_row][start_col] != current_player:
            return False

        # Check if the end square is empty
        if board[end_row][end_col] !='*':
            return False

        if current_player == 'G':
            # Goats can only move to adjacent squares
            if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
                return False
        else:
            # Tigers can move to adjacent squares or jump over goats
            if abs(start_row - end_row) > 2 or abs(start_col - end_col) > 2:
                return False
            if abs(start_row - end_row) == 2 or abs(start_col - end_col) == 2:
                # If the tiger is jumping, there must be a goat in between
                if board[(start_row + end_row) // 2][(start_col + end_col) // 2] != 'G':
                    return False

        return True
    
class alphabeta():
    def __init__(self,player,dynamic=False,depth=4):
        self.player=player
        self.depth=depth
        self.dynamic=dynamic
    
    def next_move(self,state):
        if self.dynamic==True:
            if self.heuristic(state,self.player)>300:
                self.depth=4
            elif self.heuristic(state,self.player)<0:
                self.depth=8
            else:
                self.depth=6
        score,choice=self.max_value(state,self.depth,-1e10,1e10)
        # print(score)
        return choice
    
    def get_valid_moves(self,state,current_player=None):
        if current_player==None:
            current_player=self.player
        valid_moves=[]
        board=state['board']
        if current_player == 'G':
            if state['goats'] > 0:
                # If there are still goats to be placed
                for row in range(5):
                    for col in range(5):
                        if board[row][col] == '*':
                            valid_moves.append((row,col,None,None))
            else:
                # If all goats have been placed, they can move
                for row in range(5):
                    for col in range(5):
                        if board[row][col] == current_player:
                            # Check all adjacent squares
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = row + dr, col + dc
                                if self.valid_move(row, col, new_row, new_col,board,'G'):
                                    valid_moves.append([row,col,new_row,new_col])
                                    
        elif current_player == 'T':
            for row in range(5):
                for col in range(5):
                    if board[row][col] == current_player:
                        # Check all adjacent squares and jumps
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
                            new_row, new_col = row + dr, col + dc
                            if self.valid_move(row, col, new_row, new_col,board,'T'):
                                valid_moves.append([row,col,new_row,new_col])
        return valid_moves
    
    def valid_move(self, start_row, start_col, end_row, end_col,board,current_player=None):
        if current_player==None:
            current_player=self.player
        # Check if the start and end squares are on the board
        if not (0 <= start_row < 5 and 0 <= start_col < 5 and 0 <= end_row < 5 and 0 <= end_col < 5):
            return False

        # Check if the start square contains the current player's piece
        if board[start_row][start_col] != current_player:
            return False

        # Check if the end square is empty
        if board[end_row][end_col] !='*':
            return False

        if current_player == 'G':
            # Goats can only move to adjacent squares
            if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
                return False
        else:
            # Tigers can move to adjacent squares or jump over goats
            if abs(start_row - end_row) > 2 or abs(start_col - end_col) > 2:
                return False
            if abs(start_row - end_row) == 2 or abs(start_col - end_col) == 2:
                # If the tiger is jumping, there must be a goat in between
                if board[(start_row + end_row) // 2][(start_col + end_col) // 2] != 'G':
                    return False

        return True 
    
    def end_state(self,state):
        # Check if 5 or more goats have been captured
        if state['goats_captured'] >= 5:  # Tigers win
            return True

        # Check if the tigers can make a move
        for row in range(5):
            for col in range(5):
                if state['board'][row][col] == 'T':
                    # Check all adjacent squares and jumps
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
                        new_row, new_col = row + dr, col + dc
                        if self.valid_move(row, col, new_row, new_col,state['board'],'T'):
                            return False  # Game continues

        return True
    
    def result(self,state,move):
        board=state['board']
        if move[2]==None:
            board[move[0]][move[1]] = 'G'
            state['goats'] -= 1
            state['board']=board
            return state
        else:
            temp=board[move[0]][move[1]]
            board[move[2]][move[3]] = temp
            board[move[0]][move[1]] = '*'
            state['board']=board
            # Check if the tiger captured a goat
            if abs(move[0] - move[2]) == 2 or abs(move[1] - move[3]) == 2:
                state['goats_captured'] += 1
                state['board'][(move[0] + move[2]) // 2][(move[1] + move[3]) // 2] = '*'  # Remove the goat from the board
            return state
    
    def heuristic(self,state,current_player):
        board=state['board']
        # Number of goats captured
        gc=state['goats_captured']
        # Number of goats remaining
        gr=state['goats']
        # Number of valid moves
        vm=len(self.get_valid_moves(state,current_player))
        # Number of tigers hemmed without any valid moves
        useless_tigers=0
        safe_goats=0
        vulnerable_goats=0
        for row in range(5):
                    for col in range(5):
                        if board[row][col] == current_player:
                            # Check all adjacent squares
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = row + dr, col + dc
                                if self.valid_move(row, col, new_row, new_col,board,'T'):
                                    useless_tigers+=1
        
        # Number of goats that cannot be captured
        for row in range(5):
                    for col in range(5):
                        if board[row][col] == 'G':
                            # Check all adjacent squares
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = row + dr, col + dc
                                if self.valid_move(row, col, new_row, new_col,board,'G'):
                                    safe_goats+=1
        
        # Number of goats that can be captured
        for row in range(5):
                    for col in range(5):
                        if board[row][col] == 'G':
                            # Check all adjacent squares
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = row + dr, col + dc
                                # Check if new square is on the board
                                if (0 <= new_row < 5 and 0 <= new_col < 5):
                                    # Check if this square has tiger
                                    if board[new_row][new_col] == 'T':
                                        # Check if the tiger can jump over the goat
                                        # If the tiger has to jump over the goat at row col, then the move to 2*row-new_row,2*col-new_col should be valid
                                        if self.valid_move(new_row, new_col, 2*row-new_row, 2*col-new_col,board,'T'):
                                            vulnerable_goats+=1
        if current_player=='G':
            heuristic=(-gc*1000)+(gr*10)+(vm*10)+(useless_tigers*1000)+(safe_goats*10)+(-vulnerable_goats*100)
        else:
            heuristic=(gc*1000)+(-gr*10)+(vm*10)+(-useless_tigers*1000)+(-safe_goats*10)+(vulnerable_goats*100)                        
        
        return heuristic
    
    def undo_move(self,state,move):
        board=state['board']
        if move[2]==None:
            board[move[0]][move[1]] = '*'
            state['goats'] += 1
            state['board']=board
            return 
        else:
            temp=board[move[2]][move[3]]
            board[move[0]][move[1]] = temp
            board[move[2]][move[3]] = '*'
            state['board']=board
            # Check if the tiger captured a goat
            if abs(move[0] - move[2]) == 2 or abs(move[1] - move[3]) == 2:
                state['goats_captured'] -= 1
                state['board'][(move[0] + move[2]) // 2][(move[1] + move[3]) // 2] = 'G'  # Add the goat back to the board
            return   
    def max_value(self,state,curr_depth,alpha,beta):
        if self.player=='G':
            curr_player='G'
        else:
            curr_player='T'
        if self.end_state(state)==True:
            return self.heuristic(state,curr_player),[None,None,None,None]
        if curr_depth==0:
            return self.heuristic(state,curr_player),[None,None,None,None]
        v=-1e10 # Negative Infinity
        valid_moves=self.get_valid_moves(state,curr_player)
        if len(valid_moves)==0:
            return self.heuristic(state,curr_player),[None,None,None,None]
        for move in valid_moves:
            v2,a2=self.min_value(self.result(state,move),curr_depth-1,alpha,beta)
            self.undo_move(state,move)
            if v2>v:
              v=v2
              final_move=move
              alpha=max(alpha,v)
              if v>= beta:
                  return v,final_move
        return v,final_move
    
    def min_value(self,state,curr_depth,alpha,beta):
        if self.player=='G':
            curr_player='T'
        else:
            curr_player='G'
        if self.end_state(state)==True:
            return self.heuristic(state,curr_player),[None,None,None,None]
        
        if curr_depth==0:
            return self.heuristic(state,curr_player),[None,None,None,None]
        v=1e10 # Positive Infinity
        valid_moves=self.get_valid_moves(state,curr_player)
        if len(valid_moves)==0:
            return self.heuristic(state,curr_player),[None,None,None,None]
        for move in valid_moves:
            v2,a2=self.max_value(self.result(state,move),curr_depth-1,alpha,beta)
            self.undo_move(state,move)
            if v2<v:
              v=v2
              final_move=move
              beta=min(beta,v)
              if v<=alpha:
                  return v,final_move
        return v,final_move
    
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_fully_expanded(self):
        return len(self.children) == len(get_valid_moves(self.state))

    def select_child(self):
        return max(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))

    def add_child(self, state):
        child = Node(state, self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

def get_score(state):
    # Return the score of the terminal state
    if state['goats_captured'] >= 5:  # Tigers win
        if state['current_player']=='T':
            return 1
        else:
            return -1
    else:
        if len(get_valid_moves(state))==0:
            if state['current_player']=='T':
                return -1
            else:
                return 1
            
def perform_mcts(state, iterations):
    root = Node(state)

    for _ in range(iterations):
        node = root
        current_state = deepcopy(state)

        # Selection
        while not is_terminal(current_state) and node.is_fully_expanded():
            if get_valid_moves(current_state)==[]:
                break
            node = node.select_child()
            current_state = node.state

        # Expansion
        if not is_terminal(current_state) and len(get_valid_moves(current_state))>0:
            untried_moves = [move for move in get_valid_moves(current_state) if move not in [child.state for child in node.children]]
            selected_move = random.choice(untried_moves)
            current_state = make_move(deepcopy(current_state), selected_move)
            node = node.add_child(deepcopy(current_state))

        # Simulation
        simulation_state = deepcopy(current_state)
        while not is_terminal(simulation_state):
            if get_valid_moves(simulation_state)==[]:
                break
            random_move = random.choice(get_valid_moves(simulation_state))
            simulation_state = make_move(deepcopy(simulation_state), random_move)

        # Backpropagation
        score = simulate(simulation_state)
        while node is not None:
            node.update(score)
            node = node.parent

    return max(root.children, key=lambda c: c.wins / c.visits).state

def get_valid_moves(state,current_player=None):
        if current_player==None:
            current_player=state['current_player']
        valid_moves=[]
        board=state['board']
        if current_player == 'G':
            if state['goats'] > 0:
                # If there are still goats to be placed
                for row in range(5):
                    for col in range(5):
                        if board[row][col] == '*':
                            valid_moves.append((row,col,None,None))
            else:
                # If all goats have been placed, they can move
                for row in range(5):
                    for col in range(5):
                        if board[row][col] == current_player:
                            # Check all adjacent squares
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = row + dr, col + dc
                                if valid_move(row, col, new_row, new_col,board,'G'):
                                    valid_moves.append([row,col,new_row,new_col])
                                    
        elif current_player == 'T':
            for row in range(5):
                for col in range(5):
                    if board[row][col] == current_player:
                        # Check all adjacent squares and jumps
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
                            new_row, new_col = row + dr, col + dc
                            if valid_move(row, col, new_row, new_col,board,'T'):
                                valid_moves.append([row,col,new_row,new_col])
        return valid_moves
    
def is_terminal(state):
    # Check if 5 or more goats have been captured
    if state['goats_captured'] >= 5:  # Tigers win
        return True
    # check if goats have a valid move
    

    # Check if the tigers can make a move
    for row in range(5):
        for col in range(5):
            if state['board'][row][col] == 'T':
                # Check all adjacent squares and jumps
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
                    new_row, new_col = row + dr, col + dc
                    if valid_move(row, col, new_row, new_col,state['board'],'T'):
                        return False  # Game continues
            elif state['board'][row][col] == 'G':
                # Check all adjacent squares
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if valid_move(row, col, new_row, new_col,state['board'],'G'):
                        return False  # Game continues

    return True

def valid_move(start_row, start_col, end_row, end_col,board,current_player=None):
    if current_player==None:
        current_player='G'
    # Check if the start and end squares are on the board
    if not (0 <= start_row < 5 and 0 <= start_col < 5 and 0 <= end_row < 5 and 0 <= end_col < 5):
        return False

    # Check if the start square contains the current player's piece
    if board[start_row][start_col] != current_player:
        return False

    # Check if the end square is empty
    if board[end_row][end_col] !='*':
        return False

    if current_player == 'G':
        # Goats can only move to adjacent squares
        if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
            return False
    else:
        # Tigers can move to adjacent squares or jump over goats
        if abs(start_row - end_row) > 2 or abs(start_col - end_col) > 2:
            return False
        if abs(start_row - end_row) == 2 or abs(start_col - end_col) == 2:
            # If the tiger is jumping, there must be a goat in between
            if board[(start_row + end_row) // 2][(start_col + end_col) // 2] != 'G':
                return False

    return True

def make_move(state,move):
    board=state['board']
    if move[2]==None:
        board[move[0]][move[1]] = 'G'
        state['goats'] -= 1
        state['board']=board
        state['current_player']='T'
        return state
    else:
        temp=board[move[0]][move[1]]
        board[move[2]][move[3]] = temp
        board[move[0]][move[1]] = '*'
        state['board']=board
        # Check if the tiger captured a goat
        if abs(move[0] - move[2]) == 2 or abs(move[1] - move[3]) == 2:
            state['goats_captured'] += 1
            state['board'][(move[0] + move[2]) // 2][(move[1] + move[3]) // 2] = '*'  # Remove the goat from the board
        if state['current_player']=='T':
            state['current_player']='G'
        else:
            state['current_player']='T'
        return state
def simulate(state):
    # Simulation strategy: randomly simulate until the game ends and return the score
    while not is_terminal(state):
        if get_valid_moves(state)==[]:
            break
        random_move = random.choice(get_valid_moves(state))
        state=make_move(deepcopy(state),random_move)

    return get_score(state)  # Return the score of the terminal state

def get_move_from_states(state, optimal_state):
    valid_moves=get_valid_moves(state)
    for move in valid_moves:
        temp=make_move(deepcopy(state),move)
        # Check if every element in the board is same as temp
        if all([temp['board'][i][j] == optimal_state['board'][i][j] for i in range(5) for j in range(5)]):
            return move
    return None  # This should never happen
        
def mcts_agent(state,iter):
    optimal_state = perform_mcts(state, iter)  # Perform 1000 MCTS iterations
    return get_move_from_states(state, optimal_state)  # Assuming you have a function to get the move that led to a state

class mcts():
    def __init__(self,player,iter=100):
        self.player=player
        self.iter=100
        
    def next_move(self,state):
        move = mcts_agent(deepcopy(state),self.iter)
        return move
if __name__ == "__main__":
    # Agent Initialization examples
    # Random Agent: random_agent('G')
    # Human Agent: human_agent('G')
    # Alpha Beta Agent: alphabeta('G',Dynamic=True,Depth=4)
    # MCTS Agent: mcts('G',Iteration=1000)
    
    # In the current setup, you play as tiger and alphabeta agent plays as goat
    p1=alphabeta('G',True)
    p2=human_agent('T')
    start_time=time.time()
    game = BaghChal(p1,p2)
    end_time=time.time()
    winner=game.game()
    print("Time taken: "+str(end_time-start_time))
    