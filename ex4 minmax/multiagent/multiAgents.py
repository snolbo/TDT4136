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
        return successorGameState.getScore()

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
        "*** YOUR CODE HERE ***"

        # DEPTHS ARE ONLY COUNTED FOR EVERY MOVE MAX MAKES!!
        # Generate legal actions for max
        legal_actions = gameState.getLegalActions(0)
        best_score = -float("Inf")
        best_action = None
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            new_score = max(best_score, self.min_value(successor_state, self.depth, 1))
            if new_score > best_score:
                best_score = new_score
                best_action = action
        return best_action


    def min_value(self, game_state, remainding_depth, agent_index):
        if agent_index >= game_state.getNumAgents():  # All min's have made action, let max take action
            return self.max_value(game_state, remainding_depth - 1)

        best_score = float("Inf")

        # Get legal moves and check if there are any
        legal_actions = game_state.getLegalActions(agent_index)
        if len(legal_actions) == 0:
            best_score = self.evaluationFunction(game_state)
        else:
            for action in legal_actions:
                new_state = game_state.generateSuccessor(agent_index, action)  # Generate state when min with agent_index takes this action
                best_score = min(best_score, self.min_value(new_state, remainding_depth, agent_index + 1)) # Let min with agent_index + 1 proccess choice
        return best_score



    def max_value(self, game_state, remainding_depth):
        # Reached max depth or no legal actions -> return state score
        if remainding_depth == 0:
            score = self.evaluationFunction(game_state)
            return score

        # Get legal moves and check if there are any
        best_score = -float("Inf")
        legal_actions = game_state.getLegalActions(0)
        if len(legal_actions) == 0:
            best_score = self.evaluationFunction(game_state)
        else:
            # Find best values searching in all branches that are created from the successor state
            for action in legal_actions:
                new_state = game_state.generateSuccessor(0, action)                               # Generate state when max takes this action
                best_score = max(best_score, self.min_value(new_state, remainding_depth, 1))  # Get best score letting ghost 1 process this action
        return best_score





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # DEPTHS ARE ONLY COUNTED FOR EVERY MOVE MAX MAKES!!
        alpha = -float("Inf")
        beta = float("Inf")

        legal_actions = gameState.getLegalActions(0)
        best_score = -float("Inf")
        best_action = None
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            new_score = max(best_score, self.min_value_beta(successor_state, self.depth, 1, alpha, beta))
            if new_score > best_score:
                best_score = new_score
                alpha = new_score
                best_action = action
        return best_action

    def min_value_beta(self, game_state, remainding_depth, agent_index, alpha, beta):
        # All min's have made action, let max take action
        # print "From min values_beta : " + str(alpha) + " " + str(beta)
        if agent_index >= game_state.getNumAgents():
            return self.max_value_alpha(game_state, remainding_depth - 1, alpha, beta)

        best_score = float("Inf")
        legal_actions = game_state.getLegalActions(agent_index)
        if len(legal_actions) == 0:
            best_score = self.evaluationFunction(game_state)
        else:
            for action in legal_actions:
                new_state = game_state.generateSuccessor(agent_index, action)  # Generate state when min with agent_index takes this action
                best_score = min(best_score, self.min_value_beta(new_state, remainding_depth, agent_index + 1, alpha, beta))  # Let min with agent_index + 1 proccess choice
                if best_score < alpha:
                    return best_score
                beta = min(beta, best_score)
        return best_score


    def max_value_alpha(self, game_state, remainding_depth, alpha, beta):
        # Reached max depth or no legal actions -> return state score
        if remainding_depth == 0:
            score = self.evaluationFunction(game_state)
            return score

        best_score = -float("Inf")
        legal_actions = game_state.getLegalActions(0)
        if len(legal_actions) == 0:
            best_score = self.evaluationFunction(game_state)
        else:
            # Find best values searching in all branches that are created from the successor state
            for action in legal_actions:
                new_state = game_state.generateSuccessor(0, action)  # Generate state when max takes this action
                best_score = max(best_score, self.min_value_beta(new_state, remainding_depth, 1, alpha, beta))  # Get best score letting ghost 1 process this action
                if best_score > beta:
                    return best_score
                alpha = max(alpha, best_score)
        return best_score



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
        util.raiseNotDefined()

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

