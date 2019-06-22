
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
    def __init__(self, rows, k):       # Children => {valorAtributo:vertice, valorAtributo:True/False}
        # Obtenemos las categorías
        cats = {}
        for row in rows[1:]:
            if row[-1] not in cats:
                cats[row[-1]] = 1
            else:
                cats[row[-1]] = cats[row[-1]] + 1

        keys = list(cats.keys())
        self.cat1, self.cat2 = keys[0], keys[1]

        # Obtenemos los positivos, negativos y total
        values = list(cats.values())
        a, b, c = values[0], values[1], values[0] + values[1]

        # Obtenemos atributos
        attr = rows[0][:-1]

        # Obtenemos las probabilidades e introducimos las probabilidades positivas y negativas
        cat1_prob = {self.cat1: (a + k) / (c + 2*k)}
        cat2_prob = {self.cat2: (b + k) / (c + 2*k)}

        # Obtenemos el numero de valores para cada atributo
        for x in range(len(rows[0])-1):
            att_values = []
            for row in rows[1:]:
                att_values.append(row[x])
            att_values = list(set(att_values))

            for att_value in att_values:
                # Obtenemos un subconjunto con las filas de ese valor del atributo
                sub_rows = []
                for row in rows[1:]:
                    if row[x] == att_value:
                        sub_rows.append(row)

                # Contamos positivos y negativos
                cat1_count = 0
                cat2_count = 0
                for row in sub_rows:
                    if row[-1] == self.cat1:
                        cat1_count += 1
                    else:
                        cat2_count += 1

                # Almacenamos en las probabilidades
                cat1_prob[attr[x] + "-" + att_value] = (cat1_count + k) / (a + k * len(att_values))
                cat2_prob[attr[x] + "-" + att_value] = (cat2_count + k) / (b + k * len(att_values))

        self.cat1_prob = cat1_prob
        self.cat2_prob = cat2_prob

    def clasify_nb(self, example):  # {atributo:valorAtributo, atributo:valorAtributo}

        cat1_final_prob = self.cat1_prob[self.cat1]
        cat2_final_prob = self.cat2_prob[self.cat2]

        for x in example:
            string = x + "-" + example[x]
            cat1_final_prob = cat1_final_prob * self.cat1_prob[string]
            cat2_final_prob = cat2_final_prob * self.cat2_prob[string]

        return [self.cat1 if cat1_final_prob > cat2_final_prob else self.cat2, "P("+self.cat1+"): "+str(cat1_final_prob), "P("+ self.cat2+"): "+str(cat2_final_prob)]
