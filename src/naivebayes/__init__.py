
class NaiveBayes:

    cat1 = None
    cat2 = None
    cat1_prob = {}
    cat2_prob = {}

    # cat1Prob => {atributo-valorAtributo:probabilidad, atributo-valorAtributo:probabilidad}
    def __init__(self, cat1, cat2, cat1_prob, cat2_prob):
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat1_prob = cat1_prob
        self.cat2_prob = cat2_prob

    # Implementación del algoritmo NaiveBayes
    def __init__(self, rows): # Children => {valorAtributo:vertice, valorAtributo:True/False}
        # Obtenemos las categorías
        cats = []
        for row in rows:
            if row[-1] not in cats:
                cats.append(row[-1])
            if len(cats) == 2:
                break
        self.cat1 = cats[0]
        self.cat2 = cats[1]

        #Obtenemos las probabilidades
        for x in range(len(rows[0])-1):
            for row in rows:
                asdf=1


    def clasify_nb(self, example):  # {atributo:valorAtributo, atributo:valorAtributo}

        cat1_final_prob = 1
        cat2_final_prob = 1

        for x in example:
            string = x + "-" + example[x]
            cat1_final_prob = cat1_final_prob * self.cat1_prob[string]
            cat2_final_prob = cat2_final_prob * self.cat2_prob[string]

        return [self.cat1 if cat1_final_prob > cat2_final_prob else self.cat2, "P("+self.cat1+"): "+str(cat1_final_prob), "P("+ self.cat2+"): "+str(cat2_final_prob)]
