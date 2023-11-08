import sys
import re
from pypdf import PdfReader
from icecream import ic
ic.configureOutput(includeContext=True, contextAbsPath=False)


class User:
    def __init__(self, historico):
        reader = PdfReader(historico)
        number_of_pages = len(reader.pages)
        self.historico_texto = []
        for i in range(0, number_of_pages):
            page = reader.pages[i]
            text = page.extract_text()
            self.historico_texto.append(text.split("\n"))

        self.integralizacao()
        self.materias_aluno()
        self.get_semestre()
        self.check_curso()
        self.mc()
        self.iech()
        self.iepl()
        self.iea()
        # ic(self.materias_aluno)
        ic(self.horas_integralizadas)
        ic(self.semestre)
        ic(self.mc)
        ic(self.iech)
        ic(self.iepl)
        ic(self.iea)

    def integralizacao(self):
        pattern = r"Integralizado"
        self.horas_integralizadas = []
        # le linha por linha e insere na lista "texto"
        for page in range(len(self.historico_texto)):
            for line in range(len(self.historico_texto[page])):
                if re.search(pattern, self.historico_texto[page][line]):
                    self.horas_integralizadas.append(
                        self.historico_texto[page][line+4].split(" "))
        self.horas_integralizadas = int(self.horas_integralizadas[0][0])

    def materias_aluno(self):
        # pattern declara o REGEX a ser procurado no texto
        pattern = r"APR|APRN|CANC|DISP|MATR|REC|REP|REPF|REPMF|REPN|REPNF|TRANC|TRANS|INCORP|CUMP"
        texto = []
        # le linha por linha e insere na lista "texto"
        for page in self.historico_texto:
            for line in page:
                if re.search(pattern, line):
                    texto.append(line.split(" "))

        legenda = ["*", "e", "&", "@", "#", "§", "%"]

        self.materias_aluno = []
        # nao pega as ultimas treze linhas do texto pq é a parte que explica o que é cada situação de matéria, possivelmente vai ter q ajustar para fazer a limpeza dos outros
        for i in range(len(texto) - 15):
            if texto[i][0] in legenda:
                self.materias_aluno.append(
                    [texto[i][2], texto[i][3], texto[i][4], texto[i][6]])
            else:
                self.materias_aluno.append(
                    [texto[i][1], texto[i][2], texto[i][3], texto[i][5]])

    def get_semestre(self):
        self.semestre = int(self.historico_texto[0][23])

    def check_curso(self):
        # historico_texto
        pattern_sin = r"SISTEMAS DE INFORMAÇÃO/IMC"
        pattern_cco = r"CIÊNCIA DA COMPUTAÇÃO/IMC"
        texto = []
        cco = False
        sin = False
        # le linha por linha e insere na lista "texto"
        for page in self.historico_texto:
            for line in page:
                if re.search(pattern_sin, line):
                    sin = True
                    break
                if re.search(pattern_cco, line):
                    cco = True
                    break

    def mc(self):
        soma_nota_carga = 0
        soma_carga = 0
        for materia in self.materias_aluno:
            if materia[3] != "--" and materia[0] == "APR":
                soma_nota_carga += float(materia[2]) * float(materia[3])
                soma_carga += float(materia[2])
        self.mc = round(soma_nota_carga / soma_carga, 4)

    def iech(self):
        soma_carga = 0
        carga_total = 0
        materias_aprovadas = ["APR", "APRN"]
        materia_reprovadas = ["APR", "APRN", "REP",
                              "REPF", "REPMF", "REPN", "REPNF", "TRANC"]
        for materia in self.materias_aluno:
            if materia[0] in materias_aprovadas:
                soma_carga += int(materia[2])
            if materia[0] in materia_reprovadas:
                carga_total += int(materia[2])

        self.iech = round(soma_carga / carga_total, 4)

    def iepl(self):
        total = 2576
        prazo_medio = 9
        deveria_cumprido = total / self.semestre
        ic(deveria_cumprido)
        self.horas_integralizadas = 816
        self.iepl = round(self.horas_integralizadas /
                          ((total*self.semestre)/prazo_medio), 4)
        ic((total/self.semestre))

        ic(self.iepl)
        if self.iepl > 1.1:
            self.iepl = 1.1

    def iea(self):
        self.iea = round(self.mc * self.iech * self.iepl, 4)


if __name__ == "__main__":

    aluno = User(sys.argv[1])
