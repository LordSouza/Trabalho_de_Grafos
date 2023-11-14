from Recomendacao import Recomendacao
from User import User


class Menu:
    def __init__(self, pdf_historico):
        self.aluno = User(pdf_historico)
        self.recomendacao = Recomendacao(self.aluno)

    def opcao_gerar_recomendacao(self):
        pass
        # return self.recomendacao.gerar()

    def adicionar_materias_conflitantes(self, materias_com_conflito):
        pass
        # self.recomendacao.adicionar_conflito(materias_com_conflito)
        return "Conflito adicionado"
