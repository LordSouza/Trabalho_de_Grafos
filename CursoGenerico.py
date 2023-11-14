import pandas as pd
import numpy as np
from icecream import ic
ic.configureOutput(includeContext=True)


class CursoGenerico:
    def __init__(self, materias_obrigatorias, materias_optativas, materias_concluidas):
        self.materias_obrigatorias = materias_obrigatorias
        self.materias_optativas = materias_optativas
        self.materias_concluidas = materias_concluidas

        # Combinação de disciplinas obrigatórias e optativas em um DataFrame
        self.todas_materias_possiveis = pd.concat(
            [self.materias_obrigatorias, self.materias_optativas], ignore_index=True)

        self.__substituir_equivalentes()
        self.__materias_nao_concluidas()
        self.__gerar_lista_materias_possiveis()

    # TODO algo esta dando errado
    # materias em que foi cumprido o pre requesito
    def __gerar_lista_materias_possiveis(self):
        self.materias_possiveis = self.materias_nao_concluidas
        # self.materias_nao_concluidas
        # ic(self.materias_nao_concluidas)
        lista_codigo_concluidas = []
        for materia_aluno in self.materias_concluidas:
            lista_codigo_concluidas.append(materia_aluno[1])

        for materia in self.materias_nao_concluidas:
            # se a materia n estiver na lista, quer dizer que o pre requisito ainda nao foi cuprido
            # ic(materia)
            for mat in materia[4].split(", "):
                ic(mat)
                if mat not in lista_codigo_concluidas:
                    # ic(self.materias_possiveis)
                    self.materias_possiveis.remove(materia)
                    # ic(self.materias_possiveis)

                    break
            #     if (materia_cursada[1] in mat):
            #         ic(mat)
            # if materia[0] == materia_cursada[1]:
            #     ic(materia, materia_cursada)
            #     self.materias_possiveis.remove(materia)
        ic(self.materias_possiveis)
        # ic(self.materias_obrigatorias.values.tolist())

    def __substituir_equivalentes(self):
        # Criar dicionários para equivalentes
        dict_equivalentes_regular = {}
        # para cada linha nas optativas
        for materia in self.todas_materias_possiveis.values.tolist():
            # equivalentes recebe as materias equivalentes
            equivalentes = materia[5:]
            for equivalente in equivalentes:  # para cada equivalente em equivalentes
                # obtativas_equivalentes[equivalente] vai receber o codigo
                dict_equivalentes_regular[materia[0]] = equivalente
        for materia in self.materias_concluidas:
            for key, value in dict_equivalentes_regular.items():
                if materia[1] in value.split(", "):
                    materia[1] = key

    # Cria uma lista com as materias não cursadas
    def __materias_nao_concluidas(self):
        self.materias_nao_concluidas = []
        # pega somente os codigos das materias cursadas
        lista_codigo_concluidas = []
        for materia_aluno in self.materias_concluidas:
            lista_codigo_concluidas.append(materia_aluno[1])
        # da append apenas para as materias qm não foram cursadas
        for materia_curso in self.materias_obrigatorias.values.tolist():
            if materia_curso[0] not in lista_codigo_concluidas and materia_curso not in self.materias_nao_concluidas:
                self.materias_nao_concluidas.append(materia_curso)

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
