# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # evaluate the strength of currently available player moves
        if successorGameState.isWin():
            return 100**2

        # get the positions of all active ghosts
        ghostDistances = []
        for ghost in newGhostStates:
            # measure the manhattan distance from the successor state position to the new ghost state position
            ghostDistances.append(manhattanDistance(newPos, ghost.getPosition()))
            nearestGhostDistance = min(ghostDistances)
        if nearestGhostDistance:
            ghost_heur = 10/(nearestGhostDistance)
        else:
            ghost_heur = 10000

        # get the position of all food that is left in the game
        foodLocations = newFood.asList()
        foodDistances = []
        if not len(foodLocations) == 0:
            for food in foodLocations:
                currentDistance = manhattanDistance(newPos, food)
                foodDistances.append(currentDistance)
            nearestFood = min(foodDistances)
        else:
            nearestFood = 0

        # go towards power pellet
        if newPos in currentGameState.getCapsules():
            capsule_heur = 150
        else:
            capsule_heur = 0
        # scare time --> move toward ghosts if they are scared
        scaredTime = newScaredTimes
        totalScared = sum(scaredTime)

        # add positive incentive to clear food from the board
        foodRemaining = len(foodLocations)

        # tweak heuristics
        food_left_heur = 100*foodRemaining
        food_heur = 2*nearestFood

        # calculate final heuristic
        final_heur = -food_heur -ghost_heur -food_left_heur + capsule_heur

        return final_heur


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        # make sure to reference self.depth and self.evaluation for the auto-grader system
        # number of agents minus one ( pacman ) will equate the number of ghosts present
        "*** YOUR CODE HERE ***"
        # first index as pac-man agent at root position and depth
        score, move = self.miniMax(gameState, 0, 0)
        return move

    # miniMax algorithm implementation
    def miniMax(self, gameState, agentIndex, depth):
        win = gameState.isWin()
        lose = gameState.isLose()
        depthEnd = depth == self.depth
        # end the mini-max algorithm if the game is over
        if win or lose or depthEnd:
            return self.evaluationFunction(gameState), 0

        possibleMoves = gameState.getLegalActions(agentIndex)
        ghostCount = gameState.getNumAgents() - 1
        minimizerMove = ''
        maximizerMove = ''

        # maximizer (pac-man agent)
        if agentIndex == 0:
            # worst possible value for maximizer
            worstVal = -float("inf")
            for moves in possibleMoves:
                successorState = gameState.generateSuccessor(agentIndex, moves)
                currentVal, moveChoice = self.miniMax(successorState, 1, depth)
                if currentVal > worstVal:
                    worstVal, maximizerMove = currentVal, moves
            return worstVal, maximizerMove
        # minimizer (ghost agent)
        else:
            # worst possible value for minimizer
            worstVal = float("inf")
            for moves in possibleMoves:
                if agentIndex < ghostCount:
                    successorState = gameState.generateSuccessor(agentIndex, moves)
                    currentVal, moveChoice = self.miniMax(successorState, agentIndex + 1, depth)
                else:
                    successorState = gameState.generateSuccessor(agentIndex, moves)
                    currentVal, moveChoice = self.miniMax(successorState, 0,  depth + 1)
                if currentVal < worstVal:
                    worstVal = currentVal
                    minimizerMove = moves
            return worstVal, minimizerMove



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction

          #game state.getLegalActions(agentIndex):
          returns a list of the legal actions for an agent (0 is pacman) ghost are 1 forwards

          #gameState.generateSuccessor(agentIndex, action):
          returns the successor game state after an agent takes an action

          #gameState.getnumAgents():
          returns the number of agents in a game (no. of ghosts will be equal to this value - 1 , due to him being
          indexed as the 0 agent)
        """

        "*** YOUR CODE HERE ***"
        # implement pruning on miniMax algorithm
        def alphaBeta(gameState):
            # worst possible initial values set
            value = -float("inf")
            alpha = -float("inf")
            beta = float("inf")
            possibleMoves = gameState.getLegalActions(0)
            for currentAction in possibleMoves:
                successorState = gameState.generateSuccessor(0, currentAction)
                minimizerValue = minimizer(successorState, 1, 1, alpha, beta)
                if minimizerValue > value:
                    value = minimizerValue
                if alpha == -float("inf"):
                    alpha = value
                    moveDecision = currentAction
                else:
                    if value > alpha:
                        moveDecision = currentAction
                        alpha = value
            return moveDecision

        def minimizer(gameState, agentIndex, depth, alpha, beta):
            totalAgents = gameState.getNumAgents()
            if agentIndex == totalAgents:
                return maximizer(gameState, 0, depth + 1, alpha, beta)
            # initialize value to positive infinity
            value = float("inf")
            possibleMoves = gameState.getLegalActions(agentIndex)
            # for each successor state
            for currentAction in possibleMoves:
                successorState = gameState.generateSuccessor(agentIndex, currentAction)
                # v = minimizer(v,successorState, alpha, beta)
                moveChoice = minimizer(successorState, agentIndex + 1, depth, alpha, beta)
                if moveChoice < value:
                    value = moveChoice
                # if v < alpha return v
                if value < alpha:
                    return value
                if value < beta:
                    beta = value
            # return value
            if not value == float("inf"):
                return value
            # a possible move value has not been determined -- game is over / error
            else:
                return self.evaluationFunction(gameState)

        def maximizer(gameState, agentIndex, depth, alpha, beta):
            # if at the end of the tree
            if depth > self.depth:
                return self.evaluationFunction(gameState)
            # initialize v to -infinity
            value = -float("inf")
            # for each successor state
            possibleMoves = gameState.getLegalActions(agentIndex)
            for currentAction in possibleMoves:
                successorState = gameState.generateSuccessor(agentIndex, currentAction)
                moveChoice = minimizer(successorState, agentIndex + 1, depth, alpha, beta)
                # set v to successor if successor is greater than v
                if moveChoice > value:
                    value = moveChoice
                # if v is greater than beta return v
                if value > beta:
                    return value
                # if v is greater than alpha alpha = v
                if value > alpha:
                    alpha = value
            # return value
            if not value == -float("inf"):
                return value
            # a possible move value has not been determined -- game is over / error
            else:
                return self.evaluationFunction(gameState)
        return alphaBeta(gameState)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # expectimax used to play against imperfect adversary agents
        # goal is to maximize average score
        # max nodes like in minimax search
        # chance nodes --  work like minimizer nodes in minimax search
        def expectimax():
            return 0


        return expectimax()
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

