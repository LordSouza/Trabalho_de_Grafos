import pandas as pd
import numpy as np
from icecream import ic
ic.configureOutput(includeContext=True)


class CursoGenerico:
    def __init__(self, materias_obrigatorias_aluno, todas_materias, materias_concluidas):
        self.materias_obrigatorias_aluno = materias_obrigatorias_aluno.values.tolist()
        self.todas_materias = todas_materias
        self.materias_concluidas = materias_concluidas

        self.__substituir_equivalentes()
        self.__semestralidade()
        self.__materias_nao_concluidas()
        self.__gerar_lista_materias_possiveis()

    def __substituir_equivalentes(self):
        # Criar dicionários para equivalentes
        dict_equivalentes_regular = {}
        # para cada linha nas optativas
        for materia in self.materias_obrigatorias_aluno:
            # equivalentes recebe as materias equivalentes
            equivalentes = materia[5]
            # para cada equivalente em equivalentes
            for equivalente in equivalentes.split(", "):
                # obtativas_equivalentes[equivalente] vai receber o codigo
                dict_equivalentes_regular[equivalente] = materia[0]
        for materia in self.materias_concluidas:
            for key, value in dict_equivalentes_regular.items():
                if materia[1] == key:
                    materia[1] = value

    def __semestralidade(self):
        for materia in self.todas_materias:
            materia.append(False)

        # se for semestral, coloca como true
        for materia in self.todas_materias:
            for materias_check in self.todas_materias:
                if materia[0] == materias_check[0] and \
                        materia[2] % 2 == 1 and \
                        materias_check[2] % 2 == 0:
                    materias_check[-1] = True
                    materia[-1] = True
                    break
        for materia in self.todas_materias:
            for materia_curso in self.materias_obrigatorias_aluno:
                if materia_curso[0] == materia[0] and \
                        len(materia_curso) < len(materia):
                    materia_curso.append(materia[-1])

    # Cria uma lista com as materias não cursadas

    def __materias_nao_concluidas(self):
        self.materias_nao_concluidas = []
        # pega somente os codigos das materias cursadas
        lista_codigo_concluidas = []
        for materia_aluno in self.materias_concluidas:
            lista_codigo_concluidas.append(materia_aluno[1])
        # da append apenas para as materias qm não foram cursadas
        for materia_curso in self.materias_obrigatorias_aluno:
            if materia_curso[0] not in lista_codigo_concluidas and materia_curso not in self.materias_nao_concluidas:
                self.materias_nao_concluidas.append(materia_curso)

    # materias em que foi cumprido o pre requesito
    def __gerar_lista_materias_possiveis(self):
        self.materias_possiveis = self.materias_nao_concluidas.copy()
        # self.materias_nao_concluidas
        lista_codigo_concluidas = []
        for materia_aluno in self.materias_concluidas:
            lista_codigo_concluidas.append(materia_aluno[1])

        for materia in self.materias_nao_concluidas:
            # se a materia n estiver na lista, quer dizer que o pre requisito ainda nao foi cuprido
            for mat in materia[4].split(", "):
                if mat not in lista_codigo_concluidas:
                    self.materias_possiveis.remove(materia)
                    break
