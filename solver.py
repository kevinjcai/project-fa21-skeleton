from parse import read_input_file, write_output_file
import os
import copy
import Task

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    
    duration = 0
    task : Task = None
    sol = []
    availTasks = copy.copy(tasks)
    while duration < 1440 and availTasks != []:
        if duration != 0:
            sol.append(task.get_task_id())
            availTasks.remove(task)
        for t in range(len(availTasks)):
            if t == 0:
                task = availTasks[t]
            else:
                task = max([task, availTasks[t]], key = lambda x : x.get_Profit(duration))
        duration += task.get_duration()
    return sol
    
    pass


# Here's an example of how to run your solver.
if __name__ == '__main__':
    counter = 0
    for size in os.listdir('inputs/'):
        # if size not in ['small']:

        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if counter == 5:
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