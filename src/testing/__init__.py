from id3 import create_tree
import matplotlib.pyplot as plt
import numpy as np


def test(dataset, train_percent, shuffle, trees, vary, quorum_min, quorum_max, quorum_quorum_type, quorum_interval, quorum_k,
         k_min, k_max, k_quorum, k_quorum_type):
    if vary == "quorum":
        hit_percent = {}
        leaf_count = {}
        leaf_count2 = {"id3": {}, "trunc": {}, "none": {}}
        leaf_hit_percent = {}
        leaf_hit_percent2 = {"id3": {}, "trunc": {}, "none": {}}
        for quorum_vary in range(int(quorum_min), int(quorum_max)+1, int(quorum_interval)):
            print("Quorum", quorum_vary)

            # Se sacan datos de varios arboles
            hit_percent_acc = 0
            id3_count_acc = 0
            id3_hit_percent_acc = 0
            id3_empty_count = 0
            trunc_count_acc = 0
            trunc_hit_percent_acc = 0
            trunc_empty_count = 0
            none_count_acc = 0
            none_hit_percent_acc = 0
            none_empty_count = 0
            for i in range(int(trees)):
                info = get_results(dataset, train_percent, quorum_vary, quorum_quorum_type, quorum_k, shuffle)
                hit_percent_acc += info["hit_percent"]
                id3_count_acc += info["id3_count"]
                id3_hit_percent_acc += info["id3_hit_percent"]
                trunc_count_acc += info["trunc_count"]
                trunc_hit_percent_acc += info["trunc_hit_percent"]
                none_count_acc += info["none_count"]
                none_hit_percent_acc += info["none_hit_percent"]
                if int(info["id3_count"]) == 0:
                    id3_empty_count += 1
                if int(info["trunc_count"]) == 0:
                    trunc_empty_count += 1
                if int(info["none_count"]) == 0:
                    none_empty_count += 1

            # Se almacena la media del resultado
            hit_percent[quorum_vary] = hit_percent_acc / int(trees)
            leaf_count[quorum_vary] = {
                "id3": id3_count_acc/int(trees),
                "trunc": trunc_count_acc/int(trees),
                "none": none_count_acc/int(trees)}
            leaf_count2["id3"][quorum_vary] = id3_count_acc/int(trees)
            leaf_count2["trunc"][quorum_vary] = trunc_count_acc/int(trees)
            leaf_count2["none"][quorum_vary] = none_count_acc/int(trees)
            leaf_hit_percent[quorum_vary] = {
                "id3": 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(int(trees)-id3_empty_count),
                "trunc": 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(int(trees)-trunc_empty_count),
                "none": 0 if int(trees) == none_empty_count else none_hit_percent_acc/(int(trees)-none_empty_count)}
            leaf_hit_percent2["id3"][quorum_vary] = 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(
                    int(trees)-id3_empty_count)
            leaf_hit_percent2["trunc"][quorum_vary] = 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(
                    int(trees)-trunc_empty_count)
            leaf_hit_percent2["none"][quorum_vary] = 0 if int(trees) == none_empty_count else none_hit_percent_acc/(
                    int(trees)-none_empty_count)

        # =========== Gráficas ===========
        # Ratio de acierto
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "hit rate (ratio)", "Ratio de acierto en funcion al Quórum", "quorum_hit_rate",
                   list(hit_percent.values()))
        # Cuenta de hojas
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "no. hojas (int)", "Número de hojas en funcion al quorum", "quorum_leaf_count",
                   list(leaf_count2["id3"].values()), list(leaf_count2["trunc"].values()),
                   list(leaf_count2["none"].values()))
        # Ratio de acierto por tipo de hoja
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "ID3 hit rate (ratio)", "Ratio de acierto de id3 en funcion al Quórum",
                   "quorum_id3_hit_rate", list(leaf_hit_percent2["id3"].values()))
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "truncated leafs hit rate (ratio)", "Ratio de acierto de hojas truncadas en funcion al Quórum",
                   "quorum_trunc_hit_rate", list(leaf_hit_percent2["trunc"].values()))
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "failed leafs hit rate (ratio)", "Ratio de acierto de hojas fallidas en funcion al Quórum",
                   "quorum_none_hit_rate", list(leaf_hit_percent2["none"].values()))
    else:
        hit_percent = {}
        leaf_count = {}
        leaf_count2 = {"id3": {}, "trunc": {}, "none": {}}
        leaf_hit_percent = {}
        leaf_hit_percent2 = {"id3": {}, "trunc": {}, "none": {}}
        for k_vary in range(int(k_min), int(k_max) + 1):
            print("K", k_vary)

            # Se sacan datos de varios arboles
            hit_percent_acc = 0
            id3_count_acc = 0
            id3_hit_percent_acc = 0
            id3_empty_count = 0
            trunc_count_acc = 0
            trunc_hit_percent_acc = 0
            trunc_empty_count = 0
            none_count_acc = 0
            none_hit_percent_acc = 0
            none_empty_count = 0
            for i in range(int(trees)):
                info = get_results(dataset, train_percent, k_quorum, k_quorum_type, k_vary, shuffle)
                hit_percent_acc += info["hit_percent"]
                id3_count_acc += info["id3_count"]
                id3_hit_percent_acc += info["id3_hit_percent"]
                trunc_count_acc += info["trunc_count"]
                trunc_hit_percent_acc += info["trunc_hit_percent"]
                none_count_acc += info["none_count"]
                none_hit_percent_acc += info["none_hit_percent"]
                if int(info["id3_count"]) == 0:
                    id3_empty_count += 1
                if int(info["trunc_count"]) == 0:
                    trunc_empty_count += 1
                if int(info["none_count"]) == 0:
                    none_empty_count += 1

            # Se almacena la media del resultado
            hit_percent[k_vary] = hit_percent_acc / int(trees)
            leaf_count[k_vary] = {
                "id3": id3_count_acc / int(trees),
                "trunc": trunc_count_acc / int(trees),
                "none": none_count_acc / int(trees)}
            leaf_count2["id3"][k_vary] = id3_count_acc/int(trees)
            leaf_count2["trunc"][k_vary] = trunc_count_acc/int(trees)
            leaf_count2["none"][k_vary] = none_count_acc/int(trees)
            leaf_hit_percent[k_vary] = {
                "id3": 0 if int(trees) == id3_empty_count else id3_hit_percent_acc / (int(trees) - id3_empty_count),
                "trunc": 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc / (
                            int(trees) - trunc_empty_count),
                "none": 0 if int(trees) == none_empty_count else none_hit_percent_acc / (int(trees) - none_empty_count)}
            leaf_hit_percent2["id3"][k_vary] = 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(
                    int(trees)-id3_empty_count)
            leaf_hit_percent2["trunc"][k_vary] = 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(
                    int(trees)-trunc_empty_count)
            leaf_hit_percent2["none"][k_vary] = 0 if int(trees) == none_empty_count else none_hit_percent_acc/(
                    int(trees)-none_empty_count)

        # =========== Gráficas ===========
        # Ratio de acierto
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "hit rate (ratio)", "Ratio de acierto en funcion a K", "k_hit_rate",
                   list(hit_percent.values()))
        # Cuenta de hojas
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "no. hojas (int)", "Número de hojas en funcion a K", "k_leaf_count",
                   list(leaf_count2["id3"].values()), list(leaf_count2["trunc"].values()),
                   list(leaf_count2["none"].values()))
        # Ratio de acierto por tipo de hoja
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "ID3 hit rate (ratio)", "Ratio de acierto de id3 en funcion a K",
                   "k_id3_hit_rate", list(leaf_hit_percent2["id3"].values()))
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "truncated leafs hit rate (ratio)", "Ratio de acierto de hojas truncadas en funcion a K",
                   "k_trunc_hit_rate", list(leaf_hit_percent2["trunc"].values()))
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "failed leafs hit rate (ratio)", "Ratio de acierto de hojas fallidas en funcion a K",
                   "k_none_hit_rate", list(leaf_hit_percent2["none"].values()))

    return str(hit_percent) + "\n\n" + str(leaf_count) + "\n\n" + str(leaf_hit_percent)


def get_results(dataset, train_percent, quorum, quorum_type, k, shuffle):
    # Dado que a veces no se puede clasificar, se reintenta hasta conseguirse
    try:
        result, info = create_tree(dataset, train_percent, quorum, quorum_type, k, shuffle)
    except:
        return get_results(dataset, train_percent, quorum, quorum_type, k, shuffle)
    return info


def save_graph(x1, x2, x3, xlabel, ylabel, title, filename, y1, y2=None, y3=None):
    # Data for plotting
    t = np.arange(x1, x2+1, x3)

    fig, ax = plt.subplots()
    ax.plot(t, y1)

    if y2 is not None:
        ax.plot(t, y2)
    if y3 is not None:
        ax.plot(t, y3)

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid()

    fig.savefig("static/graphs/" + filename + ".png")
