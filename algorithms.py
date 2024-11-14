import random

from sprites import Spaceship
import config

class Algorithm:
    def get_path(self, state):
        pass
    


class ExampleAlgorithm(Algorithm):
    def get_path(self, state):
        path = []
        while not state.is_goal_state():
            possible_actions = state.get_legal_actions()
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
            path.append(action)
            state = state.generate_successor_state(action)
        return path
    
class Blue(Algorithm):
    def get_path(self, state):
        stack = [(state, [])]
        explored = []  
        while stack:
            curr, path = stack.pop()
            spaceship = curr.spaceships
            if spaceship not in explored:
                explored.append(spaceship)
                possible_actions = curr.get_legal_actions()
                possible_actions.reverse()
                for action in possible_actions:
                    successor = curr.generate_successor_state(action)
                    successor_spaceship = successor.spaceships
                    if successor_spaceship not in explored:
                        stack.append((successor, path + [action]))
            if curr.is_goal_state():
                    return path
        return []  


class Red(Algorithm):
    def get_path(self, state):
        queue = [(state, [])] 
        explored = []  
        while queue:
            curr, path = queue.pop(0) 
            spaceship = curr.spaceships 
            if spaceship not in explored:
                explored.append(spaceship)
                possible_actions = curr.get_legal_actions()
                for action in possible_actions:
                    successor = curr.generate_successor_state(action)
                    successor_spaceship = successor.spaceships
                    if successor_spaceship not in explored:
                        queue.append((successor, path + [action]))  
            if curr.is_goal_state():
                return path
        return [] 


class Black(Algorithm):
    def get_path(self, state):
        queue = [(state, [], 0)] 
        explored = []  
        while queue:
            queue.sort(key=lambda q: q[2])
            curr, path, cost = queue.pop(0)  
            spaceship = curr.spaceships 
            if spaceship not in explored:
                explored.append(spaceship)
                possible_actions = curr.get_legal_actions()
                for action in possible_actions:
                    successor = curr.generate_successor_state(action)
                    successor_spaceship = successor.spaceships
                    if successor_spaceship not in explored:
                        action_cost = curr.get_action_cost(action)
                        queue.append((successor, path + [action], cost + action_cost))  
            if curr.is_goal_state():
                return path
        return []  


class White(Algorithm):
    def int_to_coordinates(self, grid, rows, columns):
        coordinates = []
        for index in range(rows * columns):
            if grid & (1 << index):
                row = index // columns
                col = index % columns
                coordinates.append((row, col))
        return coordinates
    
    
    def distances(self,state):
        goals = self.int_to_coordinates(state.get_state('G'), config.N, config.M)
        
        distances = []
        for i in range(config.N):
            row = []
            for j in range(config.M):
                row.append(0)
            distances.append(row)   
            
        for i in range(config.N):
            for j in range(config.M):
                distances[i][j] = min([abs(i - goal[0]) + abs(j - goal[1]) for goal in goals])
        return distances
    
    def get_path(self, state):
        queue = [(state, [], 0, 0)] 
        explored = []  
        
        distances = self.distances(state)
        
        while queue:
            queue.sort(key=lambda q: q[2] + q[3])
            curr, path, cost, heuristic = queue.pop(0) 
            spaceship = curr.spaceships 
            
            if spaceship not in explored:
                explored.append(spaceship)
                possible_actions = curr.get_legal_actions()
                for action in possible_actions:                    
                    
                    successor = curr.generate_successor_state(action)
                    successor_spaceship = successor.spaceships
                    ships = self.int_to_coordinates(successor_spaceship, config.N, config.M)

                    heuristic = sum([distances[ship[0]][ship[1]] for ship in ships])                    
                    
                    if successor_spaceship not in explored:
                        action_cost = curr.get_action_cost(action)
                        queue.append((successor, path + [action], cost + action_cost, heuristic))  
            if curr.is_goal_state():
                return path
        return []  
    
    
# def sort_legal_actions(state, actions):
#     def sort_key(action):
#         spaceship_pos, move_pos = action
        
#         direction = (move_pos[0] - spaceship_pos[0], move_pos[1] - spaceship_pos[1])
        
#         if direction[0] < 0:  
#             direction2 = (-1, 0)
#         elif direction[0] > 0:  
#             direction2 = (1, 0)
#         elif direction[1] > 0:
#             direction2 = (0, 1)
#         else: 
#             direction2 = (0, -1)
        
#         direction_priority = {
#             (-1, 0): 1, 
#             (0, 1): 2, 
#             (1, 0): 3, 
#             (0, -1): 4 
#         }
        
#         action_cost = state.get_action_cost(action)
#         return (spaceship_pos, direction_priority.get(direction2, 5), action_cost)

#     return sorted(actions, key=sort_key)