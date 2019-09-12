# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    statesNode = util.Stack()
    statesNode.push(problem.getStartState())

    visited = [] # list of nodes that have already been searched
    finalPath = [] #path to goal state that will be returned

    if statesNode.isEmpty():
        return []

    statesPath = util.Stack()
    currentPosition = statesNode.pop()

    goalReached = False



    while goalReached == False:
        if currentPosition not in visited:
            # if current node has not been visited, add to visited array and check
            # its children, repeat until a dead end or goal state is reached
            visited.append(currentPosition)

            possibleActions = problem.getSuccessors(currentPosition)

            for node, action, length in possibleActions:
                statesNode.push(node)
                statesPath.push(finalPath + [action])
            currentPosition = statesNode.pop() # move to the next child node of the current state
            finalPath = statesPath.pop()
        else:
            currentPosition = statesNode.pop()
            finalPath = statesPath.pop()
            # if node has already been visited, pop from stack
        # print goalReached
        if problem.isGoalState(currentPosition):
            goalReached = True
            # print "True, Goal node has been reached"

    return finalPath
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #same as depth first search, but with a queue
    statesNode = util.Queue()
    statesNode.push(problem.getStartState())

    visited = []  # list of nodes that have already been searched
    finalPath = []  # path to goal state that will be returned

    if statesNode.isEmpty():
        return []
        # print statesNode.isEmpty()


    statesPath = util.Queue()
    currentPosition = statesNode.pop()

    goalReached = False



    while goalReached == False:
        if currentPosition not in visited:
            # if current node has not been visited, add to visited array and check
            # its children, repeat until a dead end or goal state is reached
            visited.append(currentPosition)

            possibleActions = problem.getSuccessors(currentPosition)

            for node, action, length in possibleActions:
                statesNode.push(node)
                statesPath.push(finalPath + [action])
            currentPosition = statesNode.pop()  # move to the next child node of the current state
            finalPath = statesPath.pop()
        else:
            currentPosition = statesNode.pop()
            finalPath = statesPath.pop()
            # if node has already been visited, pop from stack
        # print goalReached
        if problem.isGoalState(currentPosition):
            goalReached = True
            # print "True, Goal node has been reached"

    return finalPath
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Insert the root into the queue
    # While the queue is not empty
    #   Dequeue the maximum priority element from the queue
    #   (If priorities are same, alphabetically smaller path is chosen)
    #   If the path is ending in the goal state, print the path and exit
    #   Else
    #         Insert all the children of the dequeued element, with the cumulative costs as priority
    "*** YOUR CODE HERE ***"
    #similar to bfs, but with a priority queue -- where priority is measured by path cost
    statesNode = util.PriorityQueue()
    statesNode.push(problem.getStartState(),0)

    visited = []  # list of nodes that have already been searched
    finalPath = []  # path to goal state that will be returned

    if statesNode.isEmpty():
        return []

    statesPath = util.PriorityQueue()
    currentPosition = statesNode.pop()

    goalReached = False

    while goalReached == False:
        if currentPosition not in visited:
            # if current node has not been visited, add to visited array and check
            # its children, repeat until a dead end or goal state is reached
            visited.append(currentPosition)

            possibleActions = problem.getSuccessors(currentPosition)

            for node, action, length in possibleActions:
                # statesNode.push(node)
                # statesPath.push(finalPath + [action])

                temp = finalPath + [action]
                cost = problem.getCostOfActions(temp) #find the cost to take the curent path
                if node not in visited:
                    statesNode.push(node,cost) #add to priority queue with cost of path
                    statesPath.push(temp,cost)
            currentPosition = statesNode.pop()  # move to the next child node of the current state
            finalPath = statesPath.pop()
        else:
            currentPosition = statesNode.pop()
            finalPath = statesPath.pop()
            # if node has already been visited, pop from stack
        # print goalReached
        if problem.isGoalState(currentPosition):
            goalReached = True
            # print "True, Goal node has been reached"

    return finalPath
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # heuristic - estimated distance from the current node to the end node.
    # cost - distance between the current node and the start node.
    # total Cost of node = heuristic + cost

    statesNode = util.PriorityQueue()
    statesNode.push(problem.getStartState(), 0)

    visited = []  # list of nodes that have already been searched
    finalPath = []  # path to goal state that will be returned

    if statesNode.isEmpty():
        return []

    statesPath = util.PriorityQueue()
    currentPosition = statesNode.pop()

    goalReached = False

    while goalReached == False:
        if currentPosition not in visited:
            # if current node has not been visited, add to visited array and check
            # its children, repeat until a dead end or goal state is reached
            visited.append(currentPosition)

            possibleActions = problem.getSuccessors(currentPosition)

            for node, action, length in possibleActions:
                # statesNode.push(node)
                # statesPath.push(finalPath + [action])

                temp = finalPath + [action]
                cost = problem.getCostOfActions(temp)
                heuristicCost = cost + heuristic(node, problem)
                # find the cost to take the current path + heuristic
                if node not in visited:
                    statesNode.push(node, heuristicCost)  # add to priority queue with heuristic cost of path
                    statesPath.push(temp, heuristicCost)
            currentPosition = statesNode.pop()  # move to the next child node of the current state
            finalPath = statesPath.pop()
        else:
            currentPosition = statesNode.pop()
            finalPath = statesPath.pop()
            # if node has already been visited, pop from stack
        # print goalReached
        if problem.isGoalState(currentPosition):
            goalReached = True
            # print "True, Goal node has been reached"

    # print finalPath
    return finalPath
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
