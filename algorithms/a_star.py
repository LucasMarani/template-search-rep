import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import GOAL_STATE, State, is_solvable
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        goal_positions = {tile: index for index, tile in enumerate(GOAL_STATE)}
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal = goal_positions[tile]
            total += abs(index // 3 - goal // 3) + abs(index % 3 - goal % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        if not is_solvable(initial.tiles):
            return result

        serial = count()
        frontier = [(initial.cost + self.heuristic(initial), next(serial), initial)]
        best_g = {initial.tiles: initial.cost}

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.cost != best_g[current.tiles]:
                continue

            if current.is_goal:
                result.solution = current
                result.depth = len(current.path()) - 1
                return result

            result.nodes_expanded += 1
            for child in current.neighbors():
                if child.cost >= best_g.get(child.tiles, float("inf")):
                    continue
                best_g[child.tiles] = child.cost
                priority = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (priority, next(serial), child))
                result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
