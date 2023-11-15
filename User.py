import re
from pypdf import PdfReader


class User:
    def __init__(self, historico):
        reader = PdfReader(historico)
        number_of_pages = len(reader.pages)
        self.historico_texto_inteiro = []
        # extrai as informações do pdf sem tratar os dados
        for i in range(0, number_of_pages):
            page = reader.pages[i]
            text = page.extract_text()
            self.historico_texto_inteiro.append(text.split("\n"))

        # calcula os indices depois de receber o pdf
        self.__materias_aluno()
        self.__get_semestre()
        self.__check_curso()
        self.__mc_calculo()
        self.__iech_calculo()
        self.__iepl_calculo()
        self.__iea_calculo()
        self.__materias_aprovadas_separacao()

    def __materias_aluno(self):
        # pattern declara o REGEX a ser procurado no texto
        pattern = r"APR|APRN|CANC|DISP|MATR|REC|REP|REPF|REPMF|REPN|REPNF|TRANC|TRANS|INCORP|CUMP"
        materias_sem_tratamento = []

        # patten_iepl pega a linha que possui as informações necessárias para o calculo do iepl
        pattern_iepl = r"hComplementares"
        self.cargas_horarias = []

        # le linha por linha e insere na lista "texto"
        for page in self.historico_texto_inteiro:
            for line in page:
                if re.search(pattern, line):
                    materias_sem_tratamento.append(line.split(" "))
                if re.search(pattern_iepl, line):
                    self.cargas_horarias.append(line.split(" "))

        legenda = ["*", "e", "&", "@", "#", "§", "%"]

        self.materias_aluno_cursadas = []
        # nao pega as ultimas treze linhas do texto pq é a parte que explica o que é cada situação de matéria, possivelmente vai ter q ajustar para fazer a limpeza dos outros
        for i in range(len(materias_sem_tratamento) - 15):
            if materias_sem_tratamento[i][0] in legenda:
                self.materias_aluno_cursadas.append(
                    [materias_sem_tratamento[i][2], materias_sem_tratamento[i][3], materias_sem_tratamento[i][4], materias_sem_tratamento[i][6]])
            else:
                self.materias_aluno_cursadas.append(
                    [materias_sem_tratamento[i][1], materias_sem_tratamento[i][2], materias_sem_tratamento[i][3], materias_sem_tratamento[i][5]])

    def __materias_aprovadas_separacao(self):
        self.materias_aprovadas = []
        codigo_aprovacao = ["APR", "APRN", "CUMP", "INCORP"]
        for materia in self.materias_aluno_cursadas:
            if materia[0] in codigo_aprovacao:
                self.materias_aprovadas.append(materia)

    def __get_semestre(self):
        self.semestre = int(self.historico_texto_inteiro[0][23])

    def __check_curso(self):
        # historico_texto
        pattern_sin = r"SISTEMAS DE INFORMAÇÃO/IMC"
        pattern_cco = r"CIÊNCIA DA COMPUTAÇÃO/IMC"
        self.curso = ""

        # le linha por linha e insere na lista "texto"
        for page in self.historico_texto_inteiro:
            for line in page:
                if re.search(pattern_sin, line):
                    self.curso = "SISTEMAS DE INFORMAÇÃO"
                    break
                if re.search(pattern_cco, line):
                    self.curso = "CIÊNCIA DA COMPUTAÇÃO"
                    break

    def __mc_calculo(self):
        soma_nota_carga = 0
        soma_carga = 0
        codigo_aprovacao = ["APR", "APRN", "CUMP", "INCORP"]
        for materia in self.materias_aluno_cursadas:
            if materia[3] != "--" and materia[0] in codigo_aprovacao:
                soma_nota_carga += float(materia[2]) * float(materia[3])
                soma_carga += float(materia[2])
        self.mc = round(soma_nota_carga / soma_carga, 4)

    def __iech_calculo(self):
        soma_carga = 0
        carga_total = 0
        materias_aprovadas = ["APR", "APRN"]
        materia_reprovadas = ["APR", "APRN", "REP",
                              "REPF", "REPMF", "REPN", "REPNF", "TRANC"]
        for materia in self.materias_aluno_cursadas:
            if materia[0] in materias_aprovadas:
                soma_carga += int(materia[2])
            if materia[0] in materia_reprovadas:
                carga_total += int(materia[2])

        self.iech = round(soma_carga / carga_total, 4)

    def __iepl_calculo(self):
        carga_necessaria = int(self.cargas_horarias[0][4][1:])
        carga_cumprida = int(self.cargas_horarias[0][3][1:])

        periodo_minimo = 9
        # se n for sin, é cco, que possui periodo minimo de 8
        if (self.curso != "SISTEMAS DE INFORMAÇÃO"):
            periodo_minimo = 8

        carga_media_obrigatoria = carga_necessaria / periodo_minimo
        self.iepl = round((carga_cumprida) / ((self.semestre - 1)
                                              * carga_media_obrigatoria), 5)

        if self.iepl > 1.1:
            self.iepl = 1.1

    def __iea_calculo(self):
        self.iea = round(self.mc *
                         self.iech * self.iepl, 4)

    def calcular_iea(self, materia):

        pass
