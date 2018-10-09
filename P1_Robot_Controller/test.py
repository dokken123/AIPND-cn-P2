import helper

env_data = helper.fetch_maze()

#TODO 1模拟环境的行数
rows = len(env_data) 

#TODO 2模拟环境的列数
columns = len(env_data[0])

#TODO 3取出模拟环境第三行第六列的元素
row_3_col_6 = env_data[2][5] 

print("迷宫共有", rows, "行", columns, "列，第三行第六列的元素是", row_3_col_6)

#TODO 4计算模拟环境中，第一行的的障碍物个数。
number_of_barriers_row1 = len([x for x in env_data[0] if x == 2])

#TODO 5计算模拟环境中，第三列的的障碍物个数。
number_of_barriers_col3 = len([x[2] for x in env_data if x[2] == 2])

print("迷宫中，第一行共有", number_of_barriers_row1, "个障碍物，第三列共有", number_of_barriers_col3, "个障碍物。")

loc_map = {} #TODO 6按照上述要求创建字典

for i in range(len(env_data)):
    for j in range(len(env_data[i])):
        if env_data[i][j] == 1:
            loc_map["start"] = (i,j)
        if env_data[i][j] == 3:
            loc_map["destination"] = (i,j)
robot_current_loc = loc_map["start"] #TODO 7保存机器人当前的位置
robot_destination_loc = loc_map["destination"] # Save robot destination location

def is_move_valid(env_data, loc, act):
    """
    Judge wether the robot can take action act
    at location loc.
    
    Keyword arguments:
    env -- list, the environment data
    loc -- tuple, robots current location
    act -- string, robots meant action
    """
    rowIndex = loc[0]
    colIndex = loc[1]
    if act == 'u' and rowIndex > 0:
        nextBlock = env_data[rowIndex - 1][colIndex]
        return nextBlock != 2
    if act == 'l' and colIndex > 0:
        nextBlock = env_data[rowIndex][colIndex - 1]
        return nextBlock != 2
    if act == 'd' and rowIndex < rows - 1:
        nextBlock = env_data[rowIndex + 1][colIndex]
        return nextBlock != 2
    if act == 'r' and colIndex < columns - 1:
        nextBlock = env_data[rowIndex][colIndex + 1]
        return nextBlock != 2
    return False

## TODO 10 从头定义、实现你的函数
def valid_actions(env_data, loc):
    """
    return a list contains all valid action could be proceeded on current location
    
    Keyword arguments:
    env_data -- the matrix of environment
    loc      -- current location of robot
    """
    actions = ['u','d','l','r']
    possible = [a for a in actions if is_move_valid(env_data, loc, a)]
    return possible
    
def move_robot(loc, act):
    """
    return new location after the action
    
    Keyword arguments:
    loc -- current location
    act -- action to take
    """
    rowIndex = loc[0]
    colIndex = loc[1]
    if act == 'u':
        return (rowIndex - 1,colIndex)
    if act == 'l':
        return (rowIndex,colIndex - 1)
    if act == 'd':
        return (rowIndex + 1,colIndex)
    if act == 'r':
        return (rowIndex,colIndex + 1)

def random_choose_actions(env_data, loc):
    """
    try 300 times to find the treasure by random moves
    
    Keyword arguments:
    env_data -- environment matrix data
    loc      -- current location
    """
    from random import choice
    steps = 0
    found = False
    while steps <= 300 and not found:
        actions = valid_actions(env_data, loc)
        act = choice(actions)
        loc = move_robot(loc, act)
        found = loc == robot_destination_loc
        steps += 1
    
    if found:
        print("Treasure found in %s steps!" % steps)
    else:
        print("Treasure not found!")

def calc_h_val(loc):
    return calc_g_val(loc, robot_destination_loc)

def calc_g_val(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[0] - loc2[0])

def build_node(loc, parent):
    h_val = calc_h_val(loc)
    if parent:
        g_val = calc_g_val(loc, parent["loc"])
    else:
        g_val = 0
    return {"loc": loc, "parent": parent, "G":g_val, "H":h_val, "F":h_val + g_val}

def get_node_with_min_F(open_list):
    min_F = open_list[0]
    for i in range(1, len(open_list)):
        if open_list[i]["F"] < min_F["F"]:
            min_F = open_list[i]
    return min_F

def find_node_in_list(loc, search_list):
    search = [x for x in search_list if x["loc"] == loc]
    if len(search) > 0:
        return search[0]
    else:
        return None

def action_with_AStar(env_data, robot_current_loc):
    open_list = []
    close_list = []
    start_node = build_node(robot_current_loc, None)
    open_list.append(start_node)
    cruise_node = None
    found = False
    while not found and len(open_list) > 0:
        node = get_node_with_min_F(open_list)
        open_list.remove(node)
        close_list.append(node)
        actions = valid_actions(env_data, node["loc"])
        for act in actions:
            next_block = move_robot(node["loc"], act)
            if next_block == robot_destination_loc:
                cruise_node = build_node(next_block, node)
                found = True
                break
            if not find_node_in_list(next_block, close_list):
                exist_open_node = find_node_in_list(next_block, open_list)
                if exist_open_node:
                    g_val = calc_g_val(node["loc"], nextBlock)
                    if g_val < exist_open_node["G"]:
                        open_list.remove(exist_open_node)
                        exist_open_node["G"] = g_val
                        exist_open_node["parent"] = node
                        open_list.append(exist_open_node)
                else:
                    next_node = build_node(next_block, node)
                    open_list.append(next_node)
    if found:
        paths = []
        while cruise_node != None:
            paths.append(cruise_node["loc"])
            cruise_node = cruise_node["parent"]
        paths.reverse()
        print("Cruise to treasure found! %s paths in total." % (len(paths) - 1))
        print("Path data:")
        for p in paths:
            print(p)
    else:
        print("No cruise!")

action_with_AStar(env_data, robot_current_loc)

#random_choose_actions(env_data, robot_current_loc)