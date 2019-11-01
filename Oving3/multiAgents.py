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
        pacman=0
        def maximizer(state,depth):
            """
            :param state: current game state, used to evaluate current and future states
            :param depth: current depth, used as a exit-statement, starts as 0 initially
            :return: best_action when self.depth is reached, else it returns current best_score
            """
            if state.isWin() or state.isLose():
                return state.getScore()
            possible_actions=state.getLegalActions(pacman)
            best_score=float('-inf')
            best_action = Directions.STOP  # Default move is standing still, until a move is found
            for action in possible_actions:
                # For each action, the action-tree is explored and the highest possible score is returned, such that the
                # action leading to the highest expected score is chosen
                score = explorer(state.generateSuccessor(pacman,action),depth,1) # Begin with next move of ghost1
                if score > best_score:
                    best_score = score
                    best_action = action
            if depth == 0:
                # Return the best action after all actions have been explored
                return best_action
            else:
                # Return the best score for further comparison
                return best_score

        def explorer(state,depth,agent_number):
            """
            :param state: Current state used to explore actions
            :param depth: Current depth, used to compare with self.depth
            :param agent_number: Current agent to explore actions for
            :return: The minimal score used in minimax
            """
            if state.isLose() or state.isWin():
                return state.getScore()
            next_agent = agent_number + 1
            if agent_number == state.getNumAgents()-1:
                # If final ghost, next agent is pacman
                next_agent = pacman
            possible_actions = state.getLegalActions(agent_number)
            best_score=float("inf")
            for action in possible_actions:
                if next_agent == pacman:
                    if depth == self.depth - 1:
                        # If we are at final depth, get score for state
                        score = self.evaluationFunction(state.generateSuccessor(agent_number,action))
                    else:
                        # Else, maximize pacman's score
                        score = maximizer(state.generateSuccessor(agent_number,action),depth+1)
                else:
                    # Get expected score from ghosts
                    score = explorer(state.generateSuccessor(agent_number,action),depth,next_agent)
                # Returns the minimal score from the above evaluation, used as expected minimal score in minimax
                best_score=min(score,best_score)
            return best_score
        return maximizer(gameState,0)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        pacman = 0
        def maximizer(state, depth, alpha, beta):
            """
            :param state: Current state, used to evaluate and explore future states and actions
            :param depth: Current depth when exploring actions, starts at 0, compared to self.depth
            :param alpha: The highest guaranteed score for an agent, changes as the action-tree is explored
            :param beta: The lowest guaranteed score for an agent, changes as the action-tree is explored
            :return: Best action if self.depth is reached, else it returns current best score for further comparison
            """
            if state.isWin() or state.isLose():
                return state.getScore()
            possible_actions = state.getLegalActions(pacman)
            best_score = float("-inf")
            best_action = Directions.STOP
            for action in possible_actions:
                score = minimizer(state.generateSuccessor(pacman, action), depth, 1, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_action = action
                # Updates alpha to current highest guaranteed score
                alpha = max(alpha, best_score)
                if best_score > beta:
                    # Cuts off the branch and returns the best score, since there is no need to explore the branch any
                    # further, best_score will never be chosen above beta at the minimizer-level.
                    return best_score
            if depth == 0:
                # Return the best action when depth is reached
                return best_action
            else:
                # Else return current best_score
                return best_score

        def minimizer(state, depth, agent_number, alpha, beta):
            """
            :param state: Current state, used to evaluate and explore future states and actions
            :param depth: Current depth when exploring actions
            :param agent_number: Current agent for exploration.
            :param alpha: The highest guaranteed score for an agent, changes as the action-tree is explored
            :param beta: The lowest guaranteed score for an agent, changes as the action-tree is explored
            :return: Best score when minimizing in the action-tree.
            """
            if state.isLose() or state.isWin():
                return state.getScore()
            next_agent = agent_number + 1
            if agent_number == state.getNumAgents() - 1:
                next_agent = pacman
            possible_actions = state.getLegalActions(agent_number)
            best_score = float("inf")
            for action in possible_actions:
                if next_agent == pacman:
                    if depth == self.depth - 1:
                        # Get score at leaf node
                        score = self.evaluationFunction(state.generateSuccessor(agent_number, action))
                    else:
                        # Recursively maximize successor
                        score = maximizer(state.generateSuccessor(agent_number, action), depth + 1, alpha, beta)
                else:
                    # Recursively minimize next_agent
                    score = minimizer(state.generateSuccessor(agent_number, action), depth, next_agent, alpha, beta)
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)  # Update beta
                if best_score < alpha:
                    # Cut off if score is below alpha, best_score will never be chosen over alpha
                    return best_score
            return best_score

        return maximizer(gameState, 0, float("-inf"), float("inf"))


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

