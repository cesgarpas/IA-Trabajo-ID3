from id3 import get_results
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


def test(dataset, train_percent, shuffle, trees, vary, quorum_min, quorum_max, quorum_quorum_type, quorum_interval, quorum_k,
         k_min, k_max, k_quorum, k_quorum_type):
    if vary == "quorum":
        hit_percent = {}
        leaf_count = {}
        leaf_count2 = {"id3": {}, "trunc": {}}
        leaf_hit_percent = {}
        leaf_hit_percent2 = {"id3": {}, "trunc": {}}
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

            for i in range(int(trees)):
                result, info = get_results(dataset, train_percent, quorum_vary, quorum_quorum_type, quorum_k, shuffle, 0)
                if info is None:
                    return None
                hit_percent_acc += info["hit_percent"]
                id3_count_acc += info["id3_count"]
                id3_hit_percent_acc += info["id3_hit_percent"]
                trunc_count_acc += info["trunc_count"]
                trunc_hit_percent_acc += info["trunc_hit_percent"]
                if int(info["id3_count"]) == 0:
                    id3_empty_count += 1
                if int(info["trunc_count"]) == 0:
                    trunc_empty_count += 1

            # Se almacena la media del resultado
            hit_percent[quorum_vary] = hit_percent_acc / int(trees)
            leaf_count[quorum_vary] = {
                "id3": id3_count_acc/int(trees),
                "trunc": trunc_count_acc/int(trees)}
            leaf_count2["id3"][quorum_vary] = id3_count_acc/int(trees)
            leaf_count2["trunc"][quorum_vary] = trunc_count_acc/int(trees)
            leaf_hit_percent[quorum_vary] = {
                "id3": 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(int(trees)-id3_empty_count),
                "trunc": 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(int(trees)-trunc_empty_count)}
            leaf_hit_percent2["id3"][quorum_vary] = 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(
                    int(trees)-id3_empty_count)
            leaf_hit_percent2["trunc"][quorum_vary] = 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(
                    int(trees)-trunc_empty_count)

        # =========== Gráficas ===========
        # Ratio de acierto
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "hit rate (ratio)", "Ratio de acierto en funcion al Quórum", "quorum_hit_rate",
                   list(hit_percent.values()))
        # Cuenta de hojas
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "no. hojas (int)", "Número de hojas en funcion al quorum", "quorum_leaf_count",
                   list(leaf_count2["id3"].values()), list(leaf_count2["trunc"].values()))
        # Ratio de acierto por tipo de hoja
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "ID3 hit rate (ratio)", "Ratio de acierto de id3 en funcion al Quórum",
                   "quorum_id3_hit_rate", list(leaf_hit_percent2["id3"].values()))
        save_graph(int(quorum_min), int(quorum_max), int(quorum_interval), "quorum (" + quorum_quorum_type + ")",
                   "truncated leafs hit rate (ratio)", "Ratio de acierto de hojas truncadas en funcion al Quórum",
                   "quorum_trunc_hit_rate", list(leaf_hit_percent2["trunc"].values()))

    else:
        hit_percent = {}
        leaf_count = {}
        leaf_count2 = {"id3": {}, "trunc": {}}
        leaf_hit_percent = {}
        leaf_hit_percent2 = {"id3": {}, "trunc": {}}
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

            for i in range(int(trees)):
                result, info = get_results(dataset, train_percent, k_quorum, k_quorum_type, k_vary, shuffle, 0)
                if info is None:
                    return None
                hit_percent_acc += info["hit_percent"]
                id3_count_acc += info["id3_count"]
                id3_hit_percent_acc += info["id3_hit_percent"]
                trunc_count_acc += info["trunc_count"]
                trunc_hit_percent_acc += info["trunc_hit_percent"]
                if int(info["id3_count"]) == 0:
                    id3_empty_count += 1
                if int(info["trunc_count"]) == 0:
                    trunc_empty_count += 1

            # Se almacena la media del resultado
            hit_percent[k_vary] = hit_percent_acc / int(trees)
            leaf_count[k_vary] = {
                "id3": id3_count_acc / int(trees),
                "trunc": trunc_count_acc / int(trees)}
            leaf_count2["id3"][k_vary] = id3_count_acc/int(trees)
            leaf_count2["trunc"][k_vary] = trunc_count_acc/int(trees)
            leaf_hit_percent[k_vary] = {
                "id3": 0 if int(trees) == id3_empty_count else id3_hit_percent_acc / (
                        int(trees) - id3_empty_count),
                "trunc": 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc / (
                            int(trees) - trunc_empty_count)}
            leaf_hit_percent2["id3"][k_vary] = 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(
                    int(trees)-id3_empty_count)
            leaf_hit_percent2["trunc"][k_vary] = 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(
                    int(trees)-trunc_empty_count)

        # =========== Gráficas ===========
        # Ratio de acierto
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "hit rate (ratio)", "Ratio de acierto en funcion a K", "k_hit_rate",
                   list(hit_percent.values()))

        # Ratio de acierto para hojas truncadas
        save_graph(int(k_min), int(k_max), 1, "K (int)",
                   "truncated leafs hit rate (ratio)", "Ratio de acierto de hojas truncadas en funcion a K",
                   "k_trunc_hit_rate", list(leaf_hit_percent2["trunc"].values()))

    return str(hit_percent) + "\n\n" + str(leaf_count) + "\n\n" + str(leaf_hit_percent)


def save_graph(x1, x2, x3, xlabel, ylabel, title, filename, y1, y2=None):
    # Data for plotting
    t = np.arange(x1, x2+1, x3)

    fig, ax = plt.subplots()
    ax.plot(t, y1)

    if y2 is not None:
        ax.plot(t, y2)
        orange_patch = mpatches.Patch(color='orange', label='Truncada')
        blue_patch = mpatches.Patch(color='blue', label='ID3')
        plt.legend(handles=[orange_patch, blue_patch])

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid()

    fig.savefig("static/graphs/" + filename + ".png")
    plt.close('all')

