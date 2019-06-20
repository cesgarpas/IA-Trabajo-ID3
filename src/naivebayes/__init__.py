
class NaiveBayes:

    cat1 = None
    cat2 = None
    cat1_prob = {}
    cat2_prob = {}

    def __init__(self, cat1, cat2, cat1Prob, cat2Prob): # cat1Prob => {atributo-valorAtributo:probabilidad, atributo-valorAtributo:probabilidad}
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat1_prob = cat1Prob
        self.cat2_prob = cat2Prob

    # def __init__(self, dataset): # Children => {valorAtributo:vertice, valorAtributo:True/False}
    #     self.attribute = attribute
    #     self.children = children

    def clasify_nb(self, example): # {atributo:valorAtributo, atributo:valorAtributo}

        cat1_final_prob = 1
        cat2_final_prob = 1

        for x in example:
            string = x + "-" + example[x]
            cat1_final_prob = cat1_final_prob * self.cat1_prob[string]
            cat2_final_prob = cat2_final_prob * self.cat2_prob[string]

        print("PROBABILIDADES")
        print(cat1_final_prob)
        print(cat2_final_prob)

