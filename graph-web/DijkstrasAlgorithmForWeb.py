

def INPUT(graph):
    pass
##### input ref
    def ingraph(value):
    count = 0
    for x in graph:
        if x.value == value:
            return count
        else:
            count += 1
        return None

    while inputting:
        print("Enter # to exit")
        Node = input("Enter Node: ")
        if Node != "#":
            neighbours = input("Enter neighbour/priority: ")
            neighbours = neighbours.split(",")
            for num in range(len(neighbours)):
                neighbours[num] = neighbours[num].split("/")
            
            if ingraph(Node) != None:
                    this_node = graph[ingraph(Node)]
            else:
                this_node = node(Node)
                graph.append(this_node)
                graph2.append(this_node.value)

            for neighbour in neighbours:
                if ingraph(neighbour[0]) != None:
                    this_neighbour = graph[ingraph(neighbour[0])]
                else:
                    this_neighbour = node(neighbour[0])
                    graph.append(this_neighbour)
                    graph2.append(this_neighbour.value)

                this_node.give_neighbour(this_neighbour)
                this_node.give_neighbour_weight(-int(neighbour[1]))

        else:
            inputting = False

Q = queue(len(graph)*10)
Q.enqueue(graph[0], 0)

while Q.is_empty()==False:
    current = Q.dequeue()
    if current[0].checkfinal() == False:
        current[0].placeval = -current[1]
        current[0].final = True
        for neighbour in current[0].neighbours:
            num = current[0].getplaceofweight(neighbour)
            neighbour.placeval = current[0].placeval - int(current[0].weightofneighbours[num])
            neighbour.priority = neighbour.placeval
            Q.enqueue(neighbour, -neighbour.priority)
        
        print(current[0].value,  current[0].placeval)