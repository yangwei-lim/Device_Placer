import random
import copy
import math
from Device_Placer.BStarTree import BStarTree

def simulated_annealing(modules: list, ports: list, init_temp: int, stop_temp: int, iteration: int=1000) -> BStarTree:
    """
    @brief: Floorplan Simulated Annealing Algorithm
    @param: modules -> modules to be placed
    @param: init_temp  -> initial temperature
    @param: stop_temp  -> stop temperature
    @param: iteration  -> number of iterations
    @return: current_state -> final state of the floorplan
    """
    # initialize the temperature value and cooling rate
    temperature = init_temp
    cooling_rate = (init_temp - stop_temp)/iteration

    # initialize the current state and cost
    current_state = sa_initial_state(modules)
    current_cost  = sa_cost(current_state, ports)

    # iterate for the specified number of iterations
    while temperature > stop_temp:
        # update the state and cost
        new_state = sa_perturb(current_state)
        new_cost  = sa_cost(new_state, ports)

        # calculate the cost difference
        delta = new_cost - current_cost

        # accept the new state based on the probability
        if delta < 0 or random.random() < math.exp(-delta/temperature):
            current_state = new_state
            current_cost  = new_cost

        # cooling schedule
        temperature -= cooling_rate

    # return the current state
    return current_state

def optimal_simulated_annealing(modules: list, ports: dict, init_temp: int, stop_temp: int, iteration: int=1000) -> BStarTree:
    """
    @brief: Floorplan Simulated Annealing Algorithm
    @param: modules -> modules to be placed
    @param: init_temp  -> initial temperature
    @param: stop_temp  -> stop temperature
    @param: iteration  -> number of iterations
    @return: current_state -> final state of the floorplan
    """
    # initialize the temperature value and cooling rate
    temperature = init_temp
    cooling_rate = (init_temp - stop_temp)/iteration
    best_cost = float('inf')

    # initialize the current state and cost
    current_state = sa_initial_state(modules)
    current_cost  = sa_cost(current_state, ports)

    # iterate for the specified number of iterations
    while temperature > stop_temp:  
        # update the state and cost
        new_state = sa_perturb(current_state)
        new_cost  = sa_cost(new_state, ports)

        # calculate the cost difference
        delta = new_cost - current_cost

        # accept the new state based on the probability
        if delta < 0 or random.random() < math.exp(-delta/temperature):
            current_state = new_state
            current_cost  = new_cost
        
        # capture the best state
        if current_cost < best_cost:
            best_state = current_state
            best_cost = current_cost

        # cooling schedule
        temperature -= cooling_rate

    # return the best state
    return best_state


def sa_initial_state(modules: list) -> BStarTree:
    """
    @brief: Initialize the state (initial floorplan)
    @param: modules -> list of modules to be placed
    @return: tree -> initial state of the floorplan
    """
    tree = BStarTree()
    
    # iterate through the modules
    for module in modules:
        # insert the module into the root
        if not tree.root:
            tree.insert_root(module)
        # insert the module into the left node (module[0] is the root)
        else:
            tree.insert_left(modules[0], module)

    return tree


def sa_cost(state: BStarTree, port: dict) -> float:
    """
    @brief: Calculate the cost of the current state
    @param: state -> current state of the floorplan (B*-tree)
    @param: ports -> list of I/O ports constraints
    @return: area -> area of the floorplan
    """
    # update the floorplan
    state.update_floorplan()

    # initialization of the width, height, HPWL
    width, height = 0, 0
    hpwl = []
    
    # get the modules and nets of the floorplan
    modules = state.get_modules()
    net = state.get_nets()

    # iterate through the modules to get the width and height of the floorplan
    for module in modules:
        # if module x1 larger than width, update width
        if module.x + module.width > width:
            width = module.x + module.width
        
        # if module y1 larger than height, update height
        if module.y + module.height > height:
            height = module.y + module.height

    # calculate the area of the floorplan
    area = width * height

    # generate spsecific I/O ports for the floorplan
    for name in port:
        x0, x1, y0, y1 = 0, 0, 0, 0

        if port[name].position == "top-full":
            x0, x1 = 0, width
            y0, y1 = height, height + 10        # 10 is temporary height for the port
        elif port[name].position == "bottom-full":
            x0, x1 = 0, width
            y0, y1 = -10, 0                     # 10 is temporary height for the port
        elif port[name].position == "left-full":
            x0, x1 = -10, 0                     # 10 is temporary width for the port
            y0, y1 = 0, height
        elif port[name].position == "right-full":
            x0, x1 = width, width + 10          # 10 is temporary width for the port
            y0, y1 = 0, height
        
        if name in net and sum([x0, y0, x1, y1]) > 0:
            net[name].append([x0, y0, x1, y1])

    # iterate through the nets to calculate the HPWL
    for name in net:
        x, y = [], []

        # iterate through the coordinates of the same net
        for coor in net[name]:
            # get the coordinates at the center of pin and append to the list
            x.append((coor[2] - coor[0])/2 + coor[0]) 
            y.append((coor[3] - coor[1])/2 + coor[1])

        # calculate the HPWL
        hpwl.append(max(x) - min(x) + max(y) - min(y))
    
    # return the cost of the floorplan
    return (sum(hpwl) * 0.5) + (area * 0.5)


def sa_perturb(state: BStarTree) -> BStarTree:
    """
    @brief: Perturb the current state
    @param: state -> current state of the floorplan (B*-tree)
    @return: new_state -> new state of the floorplan 
    """
    new_state = copy.deepcopy(state)
    modules   = new_state.get_modules()
    operation = random.randint(1,2)

    # Return if only one module, no operation can be performed
    if len(modules) == 1:
        return new_state

    # Rotate Module
    if operation == 0:
        # print("Rotate")
        pass

    # Swap Between Two Modules
    elif operation == 1:
        # initialize the nodes
        node1 = 0
        node2 = 0

        # randomly select two nodes to swap
        while node1 == node2:
            node1 = random.randint(0,len(modules)-1)
            node2 = random.randint(0,len(modules)-1)

        new_state.swap(modules[node1],modules[node2])

    # Move Module
    elif operation == 2:
        # initialize the nodes and direction
        node1 = 0
        node2 = 0
        child = ["left","right"]

        # randomly select two nodes and a direction to move
        while node1 == node2:
            node1 = random.randint(0,len(modules)-1)
            node2 = random.randint(0,len(modules)-1)
            direction = random.randint(0,1)

        new_state.move(modules[node1],modules[node2],child[direction])

    return new_state