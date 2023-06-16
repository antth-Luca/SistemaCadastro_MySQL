from PyQt5 import uic, QtWidgets
import mysql.connector


def conectar():
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='cadastro_produtos'
    )
    cursor = banco.cursor()


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

    conectar()

    # Inserindo no banco de dados
    cursor.execute(f'INSERT INTO produtos VALUES ("{cod}", "{desc}", {preco}, "{categoria}")')
    banco.commit()
    banco.close()

    janCadastro.msg.setText('Cadastro realizado com sucesso!')


try:
    conectar()
except:
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
    )
    cursor = banco.cursor()

    cursor.execute('CREATE DATABASE curso_mysql'
                   'DEFAULT CHARACTER SET utf8'
                   'DEFAULT COLLATE utf8_general_ci;')

    cursor.execute('CREATE TABLE produtos ('
                   'id_prod INT NOT NULL AUTO_INCREMENT,'
                   'código INT NOT NULL AUTO_INCREMENT,'
                   'descrição VARCHAR(50) NOT NULL,'
                   'preço DOUBLE NOT NULL,'
                   'categoria VARCHAR(10) DEFAULT "Diversos",'
                   'PRIMARY KEY (id_prod)'
                   ') DEFAULT CHARSET = utf8;')
else:
    try:
        cursor.execute('SELECT * FROM produtos')
    except:
        cursor.execute('CREATE TABLE produtos ('
                       'id_prod INT NOT NULL AUTO_INCREMENT,'
                       'codigo INT NOT NULL AUTO_INCREMENT,'
                       'descricao VARCHAR(50) NOT NULL,'
                       'preco DOUBLE NOT NULL,'
                       'categoria VARCHAR(10) DEFAULT "Diversos",'
                       'PRIMARY KEY (id_prod)'
                       ') DEFAULT CHARSET = utf8;')
finally:
    banco.close()


# Preparando para executar
app = QtWidgets.QApplication([])
janCadastro = uic.loadUi('formularioCad.ui')

# Configurando botões tela de cadastro
janCadastro.enviarCad.clicked.connect(cadastrar)

# Executando
janCadastro.show()
app.exec()
