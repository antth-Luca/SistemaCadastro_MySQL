from PyQt5 import uic, QtWidgets
import mysql.connector
from lib import *












def cadastrar():
    # Pegando dados digitados pelo usuário
    nome = telaCadastro.dado_nome.text()
    sobrenome = telaCadastro.dado_sobrenome.text()
    login = telaCadastro.login.text()
    senha = telaCadastro.senha.text()
    c_senha = telaCadastro.confirma_senha.text()
    # Validando senha
    if senha == c_senha:
        try:
            # Tentando conexão com o banco
            banco = sql.connect('banco_cadastro.db')
            cursor = banco.cursor()
            # Verificando existencia da tabela, se existir faz o registro e se não cria a tabela e faz o registro
            cursor.execute('CREATE TABLE IF NOT EXISTS cadastro (nome text, sobrenome text, login text, senha text)')
            cursor.execute(f'INSERT INTO cadastro VALUES ("{nome}", "{sobrenome}", "{login}", "{senha}")')

            banco.commit()
            banco.close()

            telaCadastro.msg_for_user.setText('Cadastro bem sucedido!')
            telaCadastro.msg_for_user.move(182, 320)
            telaCadastro.msg_for_user.resize(121, 21)

        except sql.Error as erro:
            print(f'Erro ao inserir os dados: {erro}')
            telaCadastro.msg_for_user.setText('Cadastro mal sucedido!')
            telaCadastro.msg_for_user.move(182, 320)
            telaCadastro.msg_for_user.resize(121, 21)
    else:     # Falha na confirmação da senha
        telaCadastro.msg_for_user.setText('As senhas digitadas estão diferentes. Verifique e tente novamente')
        telaCadastro.msg_for_user.move(81, 320)
        telaCadastro.msg_for_user.resize(322, 21)



