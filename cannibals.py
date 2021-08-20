class State():
    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None

## Checks if current state is goal. 
    def is_goal(self):
        if self.cannibalLeft == 0 and self.missionaryLeft == 0:
            return True
        else:
            return False
        
## Checks if current state is valid.
    def is_valid(self): ## Negative numbers not allowed and missionaries always >= cannibals
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0 \
                   and self.cannibalLeft >= 0 and self.cannibalRight >= 0 \
                   and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) \
                   and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
            return True
        else:
            return False
        
## Tests all possible moves from the current state.
def successors(cur_state):
    children = []; ## List of valid moves from the current state
    
    if cur_state.boat == 'left':  ## If boat is on the left side:
        
        ## Try moving 2 missionaries left to right:
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft - 2, 'right',
                                  cur_state.cannibalRight, cur_state.missionaryRight + 2)
        if new_state.is_valid(): ## Tests if new state is valid
            new_state.parent = cur_state ## Sets incoming state as parent of new state
            children.append(new_state) ## Adds new state to list of incoming state's children
        
        ## Try moving 2 cannibals L->R:
        new_state = State(cur_state.cannibalLeft - 2, cur_state.missionaryLeft, 'right',
                                  cur_state.cannibalRight + 2, cur_state.missionaryRight)
        if new_state.is_valid(): ## Validation and parent/child process repeats
            new_state.parent = cur_state
            children.append(new_state)
            
        ## Try moving 1 missionary and 1 cannibal L->R:    
        new_state = State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft - 1, 'right',
                                  cur_state.cannibalRight + 1, cur_state.missionaryRight + 1)
        if new_state.is_valid(): 
            new_state.parent = cur_state
            children.append(new_state)
        
        ## Try moving 1 missionary L->R:
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft - 1, 'right',
                                  cur_state.cannibalRight, cur_state.missionaryRight + 1)
        if new_state.is_valid():
            new_state.parent = cur_state
            children.append(new_state)
            
        ## Try moving 1 cannibal L->R:
        new_state = State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft, 'right',
                                  cur_state.cannibalRight + 1, cur_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = cur_state
            children.append(new_state)
            
    else: ## If boat is on right side:
        
        ## Try moving 2 missionaries R->L:
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft + 2, 'left',
                                  cur_state.cannibalRight, cur_state.missionaryRight - 2)
        if new_state.is_valid(): ## Validation and parent/child process repeats
            new_state.parent = cur_state
            children.append(new_state)
            
        ## Try moving 2 cannibals R->L:
        new_state = State(cur_state.cannibalLeft + 2, cur_state.missionaryLeft, 'left',
                                  cur_state.cannibalRight - 2, cur_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = cur_state
            children.append(new_state)
            
        ## Try moving 1 missionary and 1 cannibal R->L:
        new_state = State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft + 1, 'left',
                                  cur_state.cannibalRight - 1, cur_state.missionaryRight - 1)
        if new_state.is_valid():
            new_state.parent = cur_state
            children.append(new_state)
            
        ## Try moving 1 missionary R->L:
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft + 1, 'left',
                                  cur_state.cannibalRight, cur_state.missionaryRight - 1)
        if new_state.is_valid():
            new_state.parent = cur_state
            children.append(new_state)
            
        ## Try moving 1 cannibal R->L:
        new_state = State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft, 'left',
                                  cur_state.cannibalRight - 1, cur_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = cur_state
            children.append(new_state)
            
    ## Return list of valid states        
    return children

def breadth_first_search(): ## Main search function
    initial_state = State(3,3,'left',0,0) ## Initialize the puzzle with everything on the left
    if initial_state.is_goal(): ## Check the state against the goal
        return initial_state
    frontier = list() ## List of state objects to be explored
    explored = set() ## List of state objects already explored
    frontier.append(initial_state) ## Adds state to list to be explored
    while frontier: ## While there are states left to explore:
        state = frontier.pop(0) ## Take the first state from the 'to-be-explored' list:
        if state.is_goal(): ## Check if it's the goal state
            return state ## Returns goal state object to be used in print_solution() function
        explored.add(state) ## Add state to 'already-explored' list
        children = successors(state) ## Get list of state's children by running state through successors() function
        for child in children: ## For every state in the list of child states:
            if (child not in explored) or (child not in frontier): ## If child state unexplored and not already in frontier:
                frontier.append(child) ## Add child state to frontier list
    return None

def print_solution(solution):
    path = [] ## Creates list of state objects for solving the puzzle 
    path.append(solution) ## Adds the solution state to the list
    parent = solution.parent ## Assigns solution state's parent to variable parent
    while parent: ## For each state object that has a parent
        path.append(parent) ## Add the parent state object to the solution list
        parent = parent.parent ## And assign the parent's parent state to the variable parent

    for t in range(len(path)): ## For each state object in the path list
        state = path[len(path) - t - 1] ## Starting at the end of the list and working backwards
        print ("(" + str(state.cannibalLeft) + "," + str(state.missionaryLeft) \
                          + "," + state.boat + "," + str(state.cannibalRight) + "," + \
                          str(state.missionaryRight) + ")")

def main():
    solution = breadth_first_search()
    print ("Missionaries and Cannibals solution:\n")
    print ("(cannibalLeft,missionaryLeft,boat,cannibalRight,missionaryRight)\n")
    print_solution(solution)
main()