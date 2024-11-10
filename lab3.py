import queue
import matplotlib.pyplot as plt  
def getHeuristics():
    heuristics = {}  
    f = open("heuristic.txt")  
    for i in f.readlines():  
        node_heuristic_val = i.split()  
        heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1]) 
    return heuristics

def getCity():
    city = {}  
    citiesCode = {}  
    f = open("cities.txt") 
    j = 1 
    
    for i in f.readlines(): 
        node_city_val = i.split() 
        
        city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]
        
        citiesCode[j] = node_city_val[0] 
        j += 1  
        
    return city, citiesCode

def createGraph():
    graph = {}
    file = open("citiesGraph.txt")
    for i in file.readlines():
        node_val = i.split()
        if node_val[0] in graph and node_val[1] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})
            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})
        elif node_val[0] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})
            graph[node_val[1]] = [[node_val[0], node_val[2]]]
        elif node_val[1] in graph:
            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})
            graph[node_val[0]] = [[node_val[1], node_val[2]]]
        else:
            graph[node_val[0]] = [[node_val[1], node_val[2]]]
            graph[node_val[1]] = [[node_val[0], node_val[2]]]
    return graph
def GBFS(startNode, heuristics, graph, goalNode):

    priorityQueue = queue.PriorityQueue()
    visited = set()  
    priorityQueue.put((heuristics[startNode], startNode))
    parent = {startNode: None} 
    
    while not priorityQueue.empty():
        current = priorityQueue.get()[1]
        
        if current in visited:
            continue
            
        visited.add(current)
        
        if current == goalNode:
            path = []
            while current is not None:
                path.append(current)
                current = parent.get(current)
            return list(reversed(path))
        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                parent[neighbor] = current  
                priorityQueue.put((heuristics[neighbor], neighbor))
    
    return []  
def Astar(startNode, heuristics, graph, goalNode):

    priorityQueue = queue.PriorityQueue()
    visited = set() 
    g_score = {startNode: 0}  
    came_from = {}  

    priorityQueue.put((heuristics[startNode], startNode))
    
    while not priorityQueue.empty():
        current = priorityQueue.get()[1]
        
        if current == goalNode:
            break
            
        if current in visited:
            continue
            
        visited.add(current)
        

        for neighbor, cost in graph[current]:
            if neighbor in visited:
                continue              
            tentative_g = g_score[current] + int(cost)
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
               
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristics[neighbor]
                priorityQueue.put((f_score, neighbor))
    path = []
    current = goalNode
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(startNode)
    path.reverse()
    
    return path

def drawMap(city, gbfs, astar, graph):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            second = city[gbfs[i + 1]]
            plt.plot([first[0], second[0]], [first[1], second[1]], "green")
        except:
            pass

    for i in range(len(astar)):
        try:
            first = city[astar[i]]
            second = city[astar[i + 1]]
            plt.plot([first[0], second[0]], [first[1], second[1]], "blue")
        except:
            continue

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.errorbar(1, 1, label="ASTAR", color="blue")
    plt.legend(loc="lower left")
    plt.show()

if __name__ == "__main__":
    heuristic = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode1 = int(input("Nhập điểm bắt đầu: "))
        inputCode2 = int(input("Nhập điểm kết thúc: "))
        
        if inputCode1 == 0 or inputCode2 == 0:
            break
            
        startCity = citiesCode[inputCode1]
        endCity = citiesCode[inputCode2]
        
        gbfs = GBFS(startCity, heuristic, graph, endCity)
        astar = Astar(startCity, heuristic, graph, endCity)
        print("GBFS: ", gbfs)
        print("A*: ", astar)
        
        drawMap(city, gbfs, astar, graph)