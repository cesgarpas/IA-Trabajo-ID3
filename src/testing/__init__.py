from id3 import create_tree


def test(dataset, train_percent, shuffle, trees, vary, quorum_min, quorum_max, quorum_quorum_type, quorum_interval, quorum_k,
         k_min, k_max, k_quorum, k_quorum_type):
    if vary == "quorum":
        hit_percent = {}
        leaf_count = {}
        leaf_hit_percent = {}
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
            leaf_hit_percent[quorum_vary] = {
                "id3": 0 if int(trees) == id3_empty_count else id3_hit_percent_acc/(int(trees)-id3_empty_count),
                "trunc": 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc/(int(trees)-trunc_empty_count),
                "none": 0 if int(trees) == none_empty_count else none_hit_percent_acc/(int(trees)-none_empty_count)}
        return str(hit_percent) + "\n\n" + str(leaf_count) + "\n\n" + str(leaf_hit_percent)
    elif vary == "naive":
        hit_percent = {}
        leaf_count = {}
        leaf_hit_percent = {}
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
            leaf_hit_percent[k_vary] = {
                "id3": 0 if int(trees) == id3_empty_count else id3_hit_percent_acc / (int(trees) - id3_empty_count),
                "trunc": 0 if int(trees) == trunc_empty_count else trunc_hit_percent_acc / (
                            int(trees) - trunc_empty_count),
                "none": 0 if int(trees) == none_empty_count else none_hit_percent_acc / (int(trees) - none_empty_count)}
        return str(hit_percent) + "\n\n" + str(leaf_count) + "\n\n" + str(leaf_hit_percent)


def get_results(dataset, train_percent, quorum, quorum_type, k, shuffle):
    # Dado que a veces no se puede clasificar, se reintenta hasta conseguirse
    try:
        result, info = create_tree(dataset, train_percent, quorum, quorum_type, k, shuffle)
    except:
        return get_results(dataset, train_percent, quorum, quorum_type, k, shuffle)
    return info
