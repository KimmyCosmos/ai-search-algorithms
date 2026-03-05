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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    fringe = Stack()
    initial_state = problem.getStartState()
    fringe.push((initial_state, []))  # (state, path)
    foundNode = set()

    while not fringe.isEmpty():
        postn, road = fringe.pop()

        if postn in foundNode:
            continue
        foundNode.add(postn)

        if problem.isGoalState(postn):
            return road

        for successor, action, _ in problem.getSuccessors(postn):
            if successor not in foundNode:
                fringe.push((successor, road + [action]))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    fringe = Queue()
    initial_state = problem.getStartState()
    fringe.push((initial_state, []))
    foundNode = set([initial_state])

    while not fringe.isEmpty():
        postn, road = fringe.pop()

        if problem.isGoalState(postn):
            return road

        for successor, action, _ in problem.getSuccessors(postn):
            if successor not in foundNode:
                foundNode.add(successor)
                fringe.push((successor, road + [action]))
    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    fringe = PriorityQueue()
    start_state = problem.getStartState()
    fringe.push((start_state, [], 0), 0)
    visited_costs = {}

    # Detect if problem has dynamic environment features
    use_dynamic = hasattr(problem, "ghosts") or hasattr(problem, "food")

    while not fringe.isEmpty():
        state, path, cost = fringe.pop()

        # Skip already visited nodes with lower cost
        if state in visited_costs and visited_costs[state] <= cost:
            continue
        visited_costs[state] = cost

        # Goal test
        if problem.isGoalState(state):
            return path

        # Explore successors
        for successor, action, step_cost in problem.getSuccessors(state):

            # ---- DYNAMIC COST FUNCTION ----
            if use_dynamic:
                dynamic_penalty = 0

                # If ghosts exist → add penalty for proximity
                if hasattr(problem, "ghosts") and isinstance(problem.ghosts, (list, tuple)):
                    for ghost_pos in problem.ghosts:
                        if isinstance(ghost_pos, tuple) and len(ghost_pos) == 2:
                            dist = abs(successor[0] - ghost_pos[0]) + abs(successor[1] - ghost_pos[1])
                            if dist <= 1:
                                dynamic_penalty += 10 / max(dist, 1)

                # If food grid exists → add reward for nearby food
                if hasattr(problem, "food"):
                    try:
                        if problem.food[successor[0]][successor[1]]:
                            dynamic_penalty -= 5
                    except Exception:
                        pass  # Skip if not indexable or not a grid

                new_cost = cost + step_cost + dynamic_penalty
            else:
                new_cost = cost + step_cost
            # ---- END DYNAMIC COST FUNCTION ----

            new_path = path + [action]
            fringe.push((successor, new_path, new_cost), new_cost)

    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    fringe = PriorityQueue()
    initial_state = problem.getStartState()
    fringe.push((initial_state, []), heuristic(initial_state, problem))
    foundNode = {}

    while not fringe.isEmpty():
        postn, road = fringe.pop()
        g = problem.getCostOfActions(road)

        if postn in foundNode and foundNode[postn] <= g:
            continue
        foundNode[postn] = g

        if problem.isGoalState(postn):
            return road

        for successor, action, _ in problem.getSuccessors(postn):
            new_road = road + [action]
            g_new = problem.getCostOfActions(new_road)
            f = g_new + heuristic(successor, problem)
            fringe.push((successor, new_road), f)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch