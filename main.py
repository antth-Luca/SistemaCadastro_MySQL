from PyQt5 import uic, QtWidgets
import mysql.connector

banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='cadastro_produtos'
    )


def cadastrar():
    # Adicionando a variáveis os valores digitados pelo usuário
    cod = janCadastro.cod.text()
    desc = janCadastro.desc.text()
    preco = janCadastro.preco.text()

    # Adicionando a variável "categoria" pelos RadioButtons
    if janCadastro.radioInformatica.isChecked():
        categoria = 'Informática'
    elif janCadastro.radioInformatica.isChecked():
        categoria = 'Eletrônica'
    elif janCadastro.radioInformatica.isChecked():
        categoria = 'Mecânica'
    elif janCadastro.radioInformatica.isChecked():
        categoria = 'Ferramentas'

    # Inserindo no banco de dados
    cursor = banco.cursor()
    cursor.execute(f'INSERT INTO produtos VALUES (codigo = "{cod}", descricao = "{desc}", preco = {preco}, categoria = "{categoria}")')
    banco.commit()
    banco.close()

    janCadastro.msg.setText('Cadastro realizado com sucesso!')


# Preparando para executar
app = QtWidgets.QApplication([])
janCadastro = uic.loadUi('formCad.ui')

# Configurando botões tela de cadastro
janCadastro.enviarCad.clicked.connect(cadastrar)

# Executando
janCadastro.show()
app.exec()
