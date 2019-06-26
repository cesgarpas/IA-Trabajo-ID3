import pydot
from id3 import get_results
from vertex import Vertex
from naivebayes import NaiveBayes

count = 0


def get_graph(dataset, quorum, quorum_type):
    try:
        global count
        count = 0
        tree, result, info = get_results(dataset, 99.99, quorum, quorum_type, 0, True, 0)

        graph = pydot.Dot(graph_type="digraph", rankdir="LR")

        recursion(tree, graph, None, "")

        with open("static/graphs/tree.png", "wb") as png:
            png.write(graph.create_png())
        return True
    except:
        return False


def recursion(vertex, graph, parent, edge_label):
    global count
    if type(vertex) is Vertex:
        node = pydot.Node(vertex.attribute + str(count), style="filled", fillcolor="white")
        count += 1
        graph.add_node(node)

        if parent is not None:
            edge = pydot.Edge(parent, node, label=edge_label)
            graph.add_edge(edge)

        for child in vertex.children:
            recursion(vertex.children[child], graph, node, child)

    elif type(vertex) is NaiveBayes:
        node = pydot.Node("N-B" + str(count), style="filled", fillcolor="red")
        count += 1
        graph.add_node(node)

        if parent is not None:
            edge = pydot.Edge(parent, node, label=edge_label)
            graph.add_edge(edge)

    else:
        node = pydot.Node(str(vertex) + str(count), style="filled", fillcolor="green")
        count += 1
        graph.add_node(node)

        if parent is not None:
            edge = pydot.Edge(parent, node, label=edge_label)
            graph.add_edge(edge)
