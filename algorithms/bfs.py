from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State, is_solvable
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        if not is_solvable(initial.tiles):
            return result

        frontier = deque([initial])
        seen = {initial.tiles}

        while frontier:
            current = frontier.popleft()
            if current.is_goal:
                result.solution = current
                result.depth = len(current.path()) - 1
                return result

            result.nodes_expanded += 1
            for child in current.neighbors():
                if child.tiles in seen:
                    continue
                seen.add(child.tiles)
                frontier.append(child)
                result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result

