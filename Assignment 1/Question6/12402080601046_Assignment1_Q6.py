import heapq

def find_cycle(graph, modules):
    visited = set()
    path = []
    position = {}

    def dfs(node):
        visited.add(node)
        position[node] = len(path)
        path.append(node)

        for next_node in graph[node]:
            if next_node not in visited:
                cycle = dfs(next_node)

                if cycle:
                    return cycle

            elif next_node in position:
                start = position[next_node]
                return path[start:] + [next_node]

        path.pop()
        position.pop(node)

        return None

    for module in modules:
        if module not in visited:
            cycle = dfs(module)

            if cycle:
                return cycle

    return None


def main():

    # Input n and e
    n, e = map(int, input("Enter number of modules and imports: ").split())

    modules = []

    print("Enter module names:")

    for _ in range(n):
        module = input().strip()
        modules.append(module)

    # Graph and indegree
    graph = {module: set() for module in modules}
    indegree = {module: 0 for module in modules}

    print("Enter import relationships:")

    for _ in range(e):

        a, b = input().split()

        # a imports b
        # b must be loaded before a
        if a not in graph or b not in graph:
            continue

        if a not in graph[b]:
            graph[b].add(a)
            indegree[a] += 1

    # Min heap for lexicographically smallest module
    heap = []

    for module in modules:
        if indegree[module] == 0:
            heapq.heappush(heap, module)

    order = []

    # Topological sorting
    while heap:

        module = heapq.heappop(heap)
        order.append(module)

        for next_module in graph[module]:

            indegree[next_module] -= 1

            if indegree[next_module] == 0:
                heapq.heappush(heap, next_module)

    # Check for cycle
    if len(order) != n:

        cycle = find_cycle(graph, modules)

        print("CYCLE")

        if cycle:
            print(" ".join(cycle))

    else:
        print("Loading order:")
        print(" ".join(order))


if __name__ == "__main__":
    main()
