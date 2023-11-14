import pandas as pd
import numpy as np
from CursoGenerico import CursoGenerico


class Recomendacao:
    def __init__(self, aluno):
        self.aluno = aluno
        self.materias_recomendadas = []
        # pega todas as disciplinas Obrigatorias e optativas
        self.disciplinas_obrigatorias_sin = pd.read_csv(
            "datasets\materias_obrigatorias_sin.csv", encoding="UTF-8", sep=";"
        )
        self.disciplinas_optativas_sin = pd.read_csv(
            "datasets\materias_optativas_sin.csv", encoding="UTF-8", sep=";"
        )
        self.disciplinas_obrigatorias_cco = pd.read_csv(
            "datasets\materias_obrigatorias_cco.csv", encoding="UTF-8", sep=";"
        )
        self.disciplinas_optativas_cco = pd.read_csv(
            "datasets\materias_optativas_cco.csv", encoding="UTF-8", sep=";"
        )
        # coloca todas as disciplinas em um unico dataset
        self.todas_disciplinas = pd.concat(
            [self.disciplinas_obrigatorias_sin,
             self.disciplinas_optativas_sin,
             self.disciplinas_obrigatorias_cco,
             self.disciplinas_optativas_cco],
            ignore_index=True
        )
        # leitura de arquivo de acordo com o curso
        if aluno.curso == "SISTEMAS DE INFORMAÇÃO":
            self.curso = CursoGenerico(
                self.disciplinas_obrigatorias_sin,
                self.disciplinas_optativas_sin,
                aluno.materias_aprovadas)
        else:
            self.curso = CursoGenerico(
                self.disciplinas_obrigatorias_cco,
                self.disciplinas_optativas_cco,
                aluno.materias_aprovadas)

    def gerar(self):
        # recomendacao de obrigatorias
        for materia in self.curso.materias_nao_concluidas:
            if materia["CODIGO"] not in self.aluno.materias_aprovadas and len(self.materias_recomendadas) < 5:
                self.materias_recomendadas.append(
                    materia["CODIGO"], materia["DISCIPLINA"])
        pass

    def adicionar_conflito(self, materias_com_conflito):
        self.materias_com_conflito = materias_com_conflito
        pass
