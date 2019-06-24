from id3 import create_tree


def test(dataset, train_percent, shuffle, trees, vary, quorum_min, quorum_max, quorum_quorum_type, quorum_interval, quorum_k,
         k_min, k_max, k_quorum, k_quorum_type):
    if vary == "quorum":
        result = get_results(dataset, train_percent, VARY, quorum_quorum_type, quorum_k, shuffle)
    elif vary == "naive":
        result = get_results(dataset, train_percent, k_quorum, k_quorum_type, VARY, shuffle)

    return "Hola"

def get_results(dataset, train_percent, quorum, quorum_type, k, shuffle):
    # Dado que a veces no se puede clasificar, se reintenta hasta conseguirse
    try:
        result, info = create_tree(dataset, train_percent, quorum, quorum_type, k, shuffle)
    except:
        return get_results()
    return info
