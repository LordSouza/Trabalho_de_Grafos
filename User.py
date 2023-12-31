import re
from pypdf import PdfReader
from icecream import ic
ic.configureOutput(includeContext=True)


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
        self.mc = self.__mc_calculo(self.materias_aluno_cursadas)
        self.iech = self.__iech_calculo(self.materias_aluno_cursadas)
        self.iepl = self.__iepl_calculo()
        self.iea = self.__iea_calculo(self.mc, self.iech, self.iepl)
        self.ira = self.__ira_calculo(self.materias_aluno_cursadas)
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
                ic(materias_sem_tratamento[i])
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

    def __mc_calculo(self, materias_cursadas):
        soma_nota_carga = 0
        soma_carga = 0
        codigo_aprovacao = ["APR", "APRN", "CUMP", "INCORP"]
        for materia in materias_cursadas:
            if materia[3] != "--" and materia[0] in codigo_aprovacao:
                soma_nota_carga += float(materia[2]) * float(materia[3])
                soma_carga += float(materia[2])
        # retorna mc
        return round(soma_nota_carga / soma_carga, 4)

    def __iech_calculo(self, materias_cursadas):
        soma_carga = 0
        carga_total = 0
        materias_aprovadas = ["APR", "APRN"]
        materia_reprovadas = ["APR", "APRN", "REP", "REPF",
                              "REPMF", "REPN", "REPNF", "TRANC"]
        for materia in materias_cursadas:
            if materia[0] in materias_aprovadas:
                soma_carga += int(materia[2])
            if materia[0] in materia_reprovadas:
                carga_total += int(materia[2])

        return round(soma_carga / carga_total, 4)

    def __iepl_calculo(self, materia_extra: any = None):
        carga_necessaria = int(self.cargas_horarias[0][4][1:])
        carga_cumprida = int(self.cargas_horarias[0][3][1:])

        if (materia_extra != None):
            carga_cumprida += materia_extra

        periodo_minimo = 9
        # se n for sin, é cco, que possui periodo minimo de 8
        if (self.curso != "SISTEMAS DE INFORMAÇÃO"):
            periodo_minimo = 8

        carga_media_obrigatoria = carga_necessaria / periodo_minimo
        iepl = round((carga_cumprida) / ((self.semestre - 1)
                                         * carga_media_obrigatoria), 5)

        if iepl > 1.1:
            iepl = 1.1

        return iepl

    def __iea_calculo(self, mc, iech, iepl):
        return round(mc * iech * iepl, 4)

    def calcular_iea(self, codigo, carga_horaria):
        """Recebe o codigo da materia e carga horaria

        Args:
            codigo (string): exemplo => 'XDES01'
            carga_horaria (int): exemplo => 64

        Returns:
            iea: retorna o iea com a materia adicionada, supondo que o aluno tire 6
        """
        materia = list([codigo, str(carga_horaria)])
        materia.insert(0, "APR")
        materia.append('6.0')
        calcula_materias = self.materias_aluno_cursadas.copy()
        calcula_materias.append(materia)
        return self.__iea_calculo(
            self.__mc_calculo(calcula_materias),
            self.__iech_calculo(calcula_materias),
            self.__iepl_calculo(int(carga_horaria)))

    def __ira_calculo(self, materias_cursadas):
        total_nota = 0
        total_carga_horaria = 0
        for materia in materias_cursadas:
            if materia[3] != '--':
                total_nota += int(materia[2])*float(materia[3])
                total_carga_horaria += int(materia[2])

        return round(total_nota / total_carga_horaria, 4)

    def calcular_ira(self, codigo, carga_horaria):
        materia = list([codigo, str(carga_horaria)])
        materia.insert(0, "APR")
        materia.append('6.0')
        calcula_materias = self.materias_aluno_cursadas.copy()
        calcula_materias.append(materia)
        return self.__ira_calculo(calcula_materias)

    def calcular_varias_materias_iea(self, lista_materias):
        calcula_materias = self.materias_aluno_cursadas.copy()
        for mat in lista_materias:
            mat = list([mat[0], str(mat[1])])
            mat.insert(0, "APR")
            mat.append('6.0')
            calcula_materias.append(mat)
