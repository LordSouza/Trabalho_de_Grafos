import pandas as pd
import numpy as np
from CursoGenerico import CursoGenerico
from icecream import ic
ic.configureOutput(includeContext=True)


class Recomendacao:
    def __init__(self, aluno):
        self.aluno = aluno
        self.materias_recomendadas = []
        # pega todas as disciplinas Obrigatorias
        self.disciplinas_obrigatorias_sin = pd.read_csv(
            "datasets\materias_obrigatorias_sin.csv", encoding="UTF-8", sep=";"
        )
        self.disciplinas_obrigatorias_cco = pd.read_csv(
            "datasets\materias_obrigatorias_cco.csv", encoding="UTF-8", sep=";"
        )

        # coloca todas as disciplinas em um unico dataset
        self.todas_disciplinas = self.disciplinas_obrigatorias_sin.values.tolist() + \
            self.disciplinas_obrigatorias_cco.values.tolist()

        # leitura de arquivo de acordo com o curso
        if aluno.curso == "SISTEMAS DE INFORMAÇÃO":
            self.curso = CursoGenerico(
                self.disciplinas_obrigatorias_sin,
                self.todas_disciplinas,
                aluno.materias_aprovadas)
        else:
            self.curso = CursoGenerico(
                self.disciplinas_obrigatorias_cco,
                self.todas_disciplinas,
                aluno.materias_aprovadas)

        self.gerar()

    # recomendacao
    def gerar(self):
        self.materias_recomendadas
        listaIndice = []
        listaIndiceIRA = []
        self.CargaH = 0
        self.CargaH_Total = 0
        obrigatorias_disponiveis = self.curso.materias_possiveis.copy()

        for materia in obrigatorias_disponiveis:
            self.CargaH = int(materia[3])
            materia.append(
                self.aluno.calcular_iea(materia[0], self.CargaH))
            materia.append(
                self.aluno.calcular_ira(materia[0], self.CargaH))
            if materia[6] == True:
                materia[6] = "SEMESTRAL"
            elif materia[6] == False:
                materia[6] = "ANUAL"

        def sort_internal(e):
            return e[-1]
        obrigatorias_disponiveis.sort(key=sort_internal, reverse=False)
        ic(obrigatorias_disponiveis)

    def adicionar_conflito(self, materias_com_conflito):
        self.materias_com_conflito = materias_com_conflito
        pass
