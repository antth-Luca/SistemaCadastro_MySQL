from PyQt5 import uic, QtWidgets
import mysql.connector


def cadastrar():
    # Adicionando a variáveis os valores digitados pelo usuário
    cod = janCadastro.cod.text()
    desc = janCadastro.desc.text()
    preco = janCadastro.preco.text()

    # Adicionando a variável "categoria" pelos RadioButtons
    if janCadastro.radioInformatica.isChecked():
        categoria = 'Informática'
    elif janCadastro.radioEletronica.isChecked():
        categoria = 'Eletrônica'
    elif janCadastro.radioMecanica.isChecked():
        categoria = 'Mecânica'
    elif janCadastro.radioFerramentas.isChecked():
        categoria = 'Ferramentas'

    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='cadastro_produtos'
    )
    cursor = banco.cursor()

    # Inserindo no banco de dados
    cursor.execute(f'INSERT INTO produtos VALUES (codigo = "{cod}", descricao = "{desc}", preco = {preco}, categoria = "{categoria}")')
    banco.commit()
    banco.close()

    janCadastro.msg.setText('Cadastro realizado com sucesso!')


# Preparando para executar
app = QtWidgets.QApplication([])
janCadastro = uic.loadUi('formularioCad.ui')

# Configurando botões tela de cadastro
janCadastro.enviarCad.clicked.connect(cadastrar)

# Executando
janCadastro.show()
app.exec()
