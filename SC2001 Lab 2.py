import random
import time

infinityValue = float("inf")

# ---------------------------------------------------------------------------
# part (a): adjacency matrix + array based priority queue
# ---------------------------------------------------------------------------

def dijkstraWithMatrixAndArray(adjacencyMatrix, startingVertex):

    numberOfVertices = len(adjacencyMatrix)
    shortestDistanceFromStart = [infinityValue] * numberOfVertices #we set the distance to all vertices to infinity
    shortestDistanceFromStart[startingVertex] = 0
    hasBeenVisited = [False] * numberOfVertices #keeping track of which vertices have been finalised in terms of distance

    # we need to visit every vertex exactly once
    for numberOfVerticesProcessedSoFar in range(numberOfVertices):

        # step 1: find the unvisited vertex with the smallest known
        # distance. this is the "array priority queue" part - instead of
        # a heap, we just loop through every vertex by hand
        currentVertex = -1
        smallestDistanceSoFar = infinityValue

        for candidateVertex in range(numberOfVertices): #finding the lowest distance vertex that has not been visited yet
            if not hasBeenVisited[candidateVertex]:
                if shortestDistanceFromStart[candidateVertex] < smallestDistanceSoFar:
                    smallestDistanceSoFar = shortestDistanceFromStart[candidateVertex]
                    currentVertex = candidateVertex
        if currentVertex == -1: #which means no vertex is left, or that it is not all connected
            break

        hasBeenVisited[currentVertex] = True

        # step 2: try to improve the distance of every neighbour of the
        # current vertex by going "through" the current vertex
        for neighbourVertex in range(numberOfVertices):
            edgeWeight = adjacencyMatrix[currentVertex][neighbourVertex]
            if edgeWeight == infinityValue: #skip if already finalised distance or has no edge
                continue
            if hasBeenVisited[neighbourVertex]:
                continue

            distanceThroughCurrentVertex = smallestDistanceSoFar + edgeWeight

            if distanceThroughCurrentVertex < shortestDistanceFromStart[neighbourVertex]:
                shortestDistanceFromStart[neighbourVertex] = distanceThroughCurrentVertex

    return shortestDistanceFromStart

class MinimisingHeap: #building the minimising heap, with bubble up, bubble down, push and pop. parent of index i is at i-2//2, left child is 2i+1, right child is 2i+2.
    def __init__(self):
        self.heapItems = []

    def isEmpty(self):
        return len(self.heapItems) == 0

    def swapTwoItems(self, firstIndex, secondIndex):
        self.heapItems[firstIndex], self.heapItems[secondIndex] = (
            self.heapItems[secondIndex],
            self.heapItems[firstIndex],
        )

    def bubbleUp(self, indexOfItemToMove):
        currentIndex = indexOfItemToMove

        while currentIndex > 0:
            parentIndex = (currentIndex - 1) // 2

            currentDistance = self.heapItems[currentIndex][0]
            parentDistance = self.heapItems[parentIndex][0]

            if currentDistance < parentDistance:
                self.swapTwoItems(currentIndex, parentIndex)
                currentIndex = parentIndex
            else:
                break

    def bubbleDown(self, indexOfItemToMove):
        currentIndex = indexOfItemToMove
        numberOfItemsInHeap = len(self.heapItems)

        while True:
            leftChildIndex = (2 * currentIndex) + 1
            rightChildIndex = (2 * currentIndex) + 2
            smallestIndexSoFar = currentIndex
            if leftChildIndex < numberOfItemsInHeap:
                if self.heapItems[leftChildIndex][0] < self.heapItems[smallestIndexSoFar][0]:
                    smallestIndexSoFar = leftChildIndex
            if rightChildIndex < numberOfItemsInHeap:
                if self.heapItems[rightChildIndex][0] < self.heapItems[smallestIndexSoFar][0]:
                    smallestIndexSoFar = rightChildIndex
            if smallestIndexSoFar == currentIndex:
                break
            self.swapTwoItems(currentIndex, smallestIndexSoFar)
            currentIndex = smallestIndexSoFar

    def push(self, distance, vertex):
        self.heapItems.append((distance, vertex))
        lastIndex = len(self.heapItems) - 1
        self.bubbleUp(lastIndex)

    def popSmallestItem(self):
        smallestItem = self.heapItems[0]
        lastItemInHeap = self.heapItems.pop() 

        if not self.isEmpty():
            self.heapItems[0] = lastItemInHeap
            self.bubbleDown(0)

        return smallestItem

def dijkstraWithAdjacencyListAndHeap(adjacencyList, startingVertex):
    numberOfVertices = len(adjacencyList)

    shortestDistanceFromStart = [infinityValue] * numberOfVertices
    shortestDistanceFromStart[startingVertex] = 0
    priorityQueue = MinimisingHeap()
    priorityQueue.push(0, startingVertex)
    hasBeenVisited = [False] * numberOfVertices

    while not priorityQueue.isEmpty():
        currentDistance, currentVertex = priorityQueue.popSmallestItem()
        if hasBeenVisited[currentVertex]:
            continue
        hasBeenVisited[currentVertex] = True
        for neighbourVertex, edgeWeight in adjacencyList[currentVertex]:
            if hasBeenVisited[neighbourVertex]:
                continue

            distanceThroughCurrentVertex = currentDistance + edgeWeight

            if distanceThroughCurrentVertex < shortestDistanceFromStart[neighbourVertex]:
                shortestDistanceFromStart[neighbourVertex] = distanceThroughCurrentVertex
                priorityQueue.push(distanceThroughCurrentVertex, neighbourVertex)

    return shortestDistanceFromStart

def generateRandomConnectedGraph(numberOfVertices, numberOfExtraEdges, maximumWeight=20): #builds the random connected graph for our tests
    adjacencyMatrix = [[infinityValue] * numberOfVertices for _ in range(numberOfVertices)] #starting it empty
    for vertex in range(numberOfVertices):
        adjacencyMatrix[vertex][vertex] = 0
    adjacencyList = [[] for _ in range(numberOfVertices)]

    def addUndirectedEdge(firstVertex, secondVertex, weight):
        adjacencyMatrix[firstVertex][secondVertex] = weight
        adjacencyMatrix[secondVertex][firstVertex] = weight
        adjacencyList[firstVertex].append((secondVertex, weight))
        adjacencyList[secondVertex].append((firstVertex, weight))

    for vertex in range(numberOfVertices - 1): #guarantees connection from n to n+1, so the graph is connected
        randomWeight = random.randint(1, maximumWeight)
        addUndirectedEdge(vertex, vertex + 1, randomWeight)

    for _ in range(numberOfExtraEdges): #adding more random edges
        firstVertex = random.randint(0, numberOfVertices - 1)
        secondVertex = random.randint(0, numberOfVertices - 1)

        if firstVertex == secondVertex: #skip self loops or existing ones
            continue
        if adjacencyMatrix[firstVertex][secondVertex] != infinityValue:
            continue

        randomWeight = random.randint(1, maximumWeight)
        addUndirectedEdge(firstVertex, secondVertex, randomWeight)

    return adjacencyMatrix, adjacencyList

def measureAverageRunningTime(functionToTest, graphArgument, startingVertex, numberOfRepeats=10): #tracking the time

    totalTimeTaken = 0.0

    for _ in range(numberOfRepeats):
        startTime = time.perf_counter()
        functionToTest(graphArgument, startingVertex)
        endTime = time.perf_counter()
        totalTimeTaken += (endTime - startTime)

    return totalTimeTaken / numberOfRepeats


def runTimingExperimentsVaryingNumberOfVertices():

    print("timing experiment: growing the number of vertices |V|")
    print("-" * 60)
    print(f"{'vertices':>10} {'edges (approx)':>16} {'matrix+array (s)':>18} {'list+heap (s)':>16}")

    verticesToTry = [50, 100, 200, 400, 800]

    for numberOfVertices in verticesToTry:
        numberOfExtraEdges = numberOfVertices * 2

        adjacencyMatrix, adjacencyList = generateRandomConnectedGraph(
            numberOfVertices, numberOfExtraEdges
        )

        matrixTime = measureAverageRunningTime(dijkstraWithMatrixAndArray, adjacencyMatrix, 0)
        heapTime = measureAverageRunningTime(dijkstraWithAdjacencyListAndHeap, adjacencyList, 0)

        approximateNumberOfEdges = (numberOfVertices - 1) + numberOfExtraEdges

        print(f"{numberOfVertices:>10} {approximateNumberOfEdges:>16} {matrixTime:>18.6f} {heapTime:>16.6f}")

    print()


def runTimingExperimentsVaryingNumberOfEdges():
    """
    keeps the number of vertices fixed and grows the number of extra
    edges, to see how each implementation scales with |E|.
    """

    print("timing experiment: fixed |V|, growing the number of edges |E|")
    print("-" * 60)
    print(f"{'vertices':>10} {'extra edges':>12} {'matrix+array (s)':>18} {'list+heap (s)':>16}")

    fixedNumberOfVertices = 300
    maximumPossibleEdges = fixedNumberOfVertices * (fixedNumberOfVertices - 1) // 2
    extraEdgesToTry = [200, 1000, 5000, 15000, min(30000, maximumPossibleEdges - fixedNumberOfVertices)]

    for numberOfExtraEdges in extraEdgesToTry:
        adjacencyMatrix, adjacencyList = generateRandomConnectedGraph(
            fixedNumberOfVertices, numberOfExtraEdges
        )

        matrixTime = measureAverageRunningTime(dijkstraWithMatrixAndArray, adjacencyMatrix, 0)
        heapTime = measureAverageRunningTime(dijkstraWithAdjacencyListAndHeap, adjacencyList, 0)

        print(f"{fixedNumberOfVertices:>10} {numberOfExtraEdges:>12} {matrixTime:>18.6f} {heapTime:>16.6f}")

    print()

if __name__ == "__main__":
    runTimingExperimentsVaryingNumberOfVertices()
    runTimingExperimentsVaryingNumberOfEdges()
