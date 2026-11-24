from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        if depth_limit < 0:
            raise ValueError("O limite de profundidade deve ser não negativo.")
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        if not is_solvable(initial.tiles):
            return result

        frontier = [(initial, 0)]
        best_depth = {initial.tiles: 0}

        while frontier:
            current, depth = frontier.pop()
            if depth != best_depth[current.tiles]:
                continue

            if current.is_goal:
                result.solution = current
                result.depth = depth
                return result

            if depth >= self.depth_limit:
                continue

            result.nodes_expanded += 1
            for child in reversed(current.neighbors()):
                next_depth = depth + 1
                previous_depth = best_depth.get(child.tiles)
                if previous_depth is not None and previous_depth <= next_depth:
                    continue
                best_depth[child.tiles] = next_depth
                frontier.append((child, next_depth))
                result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result

