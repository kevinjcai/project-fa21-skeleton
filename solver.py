from parse import read_input_file, write_output_file
import os
import copy
import Task
import numpy as np
import numpy.random as rn

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    
    duration = 0
    task : Task = None
    idOrder = []
    iglooOrder = []
    profit = 0
    availTasks = copy.copy(tasks)

    while duration < 1440 and availTasks != []:
        if duration != 0:
            idOrder.append(task.get_task_id())
            iglooOrder.append(task)
            profit += task.get_Profit(duration)
            availTasks.remove(task)
        for t in range(len(availTasks)):
            if t == 0:
                task = availTasks[t]
            else:
                task = max([task, availTasks[t]], key = lambda x : x.get_Profit(duration))
        duration += task.get_duration()
    random_start = [idOrder, iglooOrder, profit]
    sol = annealing(random_start, tasks)
    costs = sol[3]
    bestIndex = 0
    bestSeq = sol[3][0]
    for i in range(1, len(sol[3])):
        if sol[3][i] > bestSeq:
            bestIndex = i
            bestSeq =  sol[3][i]
    # print(sol[2][bestIndex][0])
    return sol[2][bestIndex][0]
    pass

#Source https://perso.crans.org/besson/publis/notebooks/Simulated_annealing_in_Python.html
def annealing(random_start, tasks, maxsteps=100, debug=True):
    """ Optimize the black-box function 'cost_function' with the simulated annealing algorithm."""
    state = random_start
    cost = cost_function(state)
    states, costs = [state], [cost]
    for step in range(maxsteps):
        fraction = step / float(maxsteps)
        T = temperature(fraction)
        new_state = random_neighbour(state, tasks, fraction)
        new_cost = cost_function(new_state)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)
            # print("  ==> Accept it!")
        # else:
        #    print("  ==> Reject it...")
    return state, cost_function(state), states, costs

def cost_function(seq):
    return seq[2]

def random_neighbour(seq, tasks, fraction=1):
    """Move a little bit x, from the left or the right."""
    oldIglooOrder = seq[1]
    oldIdOrder = seq[0]

    l = rn.randint(1, len(oldIglooOrder) - 1)
    
    iglooOrder = oldIglooOrder[ : l]
    idOrder = oldIdOrder[ : l]
    duration = 0
    availTasks = copy.copy(tasks)
    profit = 0
    for task in iglooOrder:
        profit += task.get_Profit(duration)
        availTasks.remove(task)
        duration += task.get_duration()
    
#Source https://www.geeksforgeeks.org/python-program-to-find-second-largest-number-in-a-list/
    mx = max([availTasks[0], availTasks[1]], key = lambda x : x.get_Profit(duration))
    secondmax = min([availTasks[0], availTasks[1]], key = lambda x : x.get_Profit(duration))
    n = len(availTasks)
    for i in range(2, n):
        if availTasks[i].get_Profit(duration) > mx.get_Profit(duration):
            secondmax = mx
            mx = availTasks[i]
        elif availTasks[i].get_Profit(duration) > secondmax.get_Profit(duration) and mx != availTasks[i]:
            secondmax = availTasks[i]

    iglooOrder.append(secondmax)
    idOrder.append(secondmax.get_task_id())
    profit += secondmax.get_Profit(duration)
    availTasks.remove(secondmax)
    duration += secondmax.get_duration()
    # while task != None:
    #     i = rn.randint(len(availTasks))
    #     if availTasks[i].get_Profit(duration) > 0:
    #         task = availTasks[i]
    #         iglooOrder.append(task)
    #         idOrder.append(task.get_task_id())
    #         profit += task.get_Profit(duration)
    #         availTasks.remove(task)
    #         duration += task.get_duration()
    counter = 0
    while duration < 1440 and availTasks != []:
        if counter != 0:
            idOrder.append(task.get_task_id())
            iglooOrder.append(task)
            profit += task.get_Profit(duration)
            availTasks.remove(task)
        for t in range(len(availTasks)):
            if t == 0:
                task = availTasks[t]
            else:
                task = max([task, availTasks[t]], key = lambda x : x.get_Profit(duration))
        duration += task.get_duration()
        counter = 1
    
    return [idOrder, iglooOrder, profit]

def acceptance_probability(cost, new_cost, temperature):
    if new_cost > cost:
        # print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
        return 1
    else:
        p = np.exp((new_cost - cost) / temperature)
        # print("    - Acceptance probabilty = {:.3g}...".format(p))
        return p

def temperature(fraction):
    """ Example of temperature dicreasing as the process goes on."""
    return max(0.01, min(1, 1 - fraction))



# Here's an example of how to run your solver.
if __name__ == '__main__':
    counter = 0
    for size in os.listdir('inputs/'):
        # if size not in ['small']:

        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if counter == 1:
                break
            if size not in input_file:
                continue
            input_path = 'inputs/{}/{}'.format(size, input_file)
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            print(input_path, output_path)
            tasks = read_input_file(input_path)
            output = solve(tasks)
            write_output_file(output_path, output)
            # counter += 1