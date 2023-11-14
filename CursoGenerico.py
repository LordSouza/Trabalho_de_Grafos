import pandas as pd
import numpy as np
from icecream import ic
ic.configureOutput(includeContext=True, contextAbsPath=True)


class CursoGenerico:
    def __init__(self, materias_obrigatorias, materias_optativas, materias_concluidas):
        self.materias_obrigatorias = materias_obrigatorias
        self.materias_optativas = materias_optativas
        self.materias_concluidas = materias_concluidas

        # Combinação de disciplinas obrigatórias e optativas em um DataFrame
        self.todas_materias_possiveis = pd.concat(
            [self.materias_obrigatorias, self.materias_optativas], ignore_index=True)

        self.materias_concluidas_sem_equivalentes = self.__substituir_equivalentes()
        self.__materias_nao_concluidas()
        self.__gerar_lista_materias_possiveis()

    def __gerar_lista_materias_possiveis(self):
        self.materias_possiveis = []

        for materia in self.todas_materias_possiveis:
            for materia_cursada in self.materias_concluidas_sem_equivalentes:
                if materia['CODIGO'] != materia_cursada['CÓDIGO']:
                    self.materias_possiveis.append(materia)

    def __substituir_equivalentes(self):
        materias_regulares_concluidas = []
        # Criar dicionários para equivalentes
        dict_equivalentes_regular = {}
        ic(self.todas_materias_possiveis)
        # para cada linha nas optativas
        for materia in self.todas_materias_possiveis.values.tolist():
            # equivalentes recebe as materias equivalentes
            ic(materia[5:])
            equivalentes = materia[5:]

            for equivalente in equivalentes:  # para cada equivalente em equivalentes
                # obtativas_equivalentes[equivalente] vai receber o codigo
                dict_equivalentes_regular[equivalente] = materia[0]
        # ic(dict_equivalentes_regular)

        # para um i ate o tamanho de disciplinas cursadas
        for materia in self.materias_concluidas:
            # codigo vai receber o valor de self.materias_concluidas[i]
            # se tiver o codigo em optativas_equivalentes
            if (materia[1] in list(dict_equivalentes_regular)):
                # troco o valor da self.materias_concluidas[i] pelo codigo da equivalente (optativa)
                materias_regulares_concluidas.append(
                    dict_equivalentes_regular[materia[1]])

        return materias_regulares_concluidas

    # Cria uma lista com as materias não cursadas
    def __materias_nao_concluidas(self):
        self.materias_nao_concluidas = []
        for materia in self.materias_obrigatorias:
            if materia not in self.materias_concluidas_sem_equivalentes and \
                    materia["PRE-REQUISITOS"].split(", ") in self.materias_concluidas_sem_equivalentes:
                self.materias_nao_concluidas.append(materia)

    # TODO terminar essa parte
    def calcularLiberam(self, materias_obrigatorias):
        # Cria um dicionario com o index sendo CODIGO da materia e os seus pre-requisitos como valores
        requisitos = {
            codigo: pre_requisitos
            for codigo, pre_requisitos in zip(
                materias_obrigatorias["CODIGO"],
                materias_obrigatorias["PRE-REQUISITOS"],
            )
        }
        # Gera um vetor com todas as vezes que uma materia esta presente no Pre-requisito
        liberam = []
        for materias in requisitos:
            if requisitos[materias] != "-":
                separar = requisitos[materias].split(", ")
                for mat in separar:
                    liberam.append(mat)
        # testar essa parte
        # Cria a coluna de quantas materias uma disciplina libera quando concluida
        materias_obrigatorias["Liberam"] = 0

        # Faz a soma das materias de acordo com quantas vezes ela aparece no vetor
        for materias in liberam:
            materias_obrigatorias.loc[
                materias_obrigatorias["CODIGO"] == materias, "Liberam"
            ] += 1

        # Ordena de modo que as disciplinas com mais 'Ligações' estejam acima
        # Fomatacao do dataframe [index, CODIGO,	DISCIPLINA,	PER.,	CH,	PRE-REQUISITOS,	Liberam]
        materias_obrigatorias = materias_obrigatorias.sort_values(
            by="Liberam", ascending=False
        )
        return materias_obrigatorias
