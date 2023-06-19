from PyQt5 import uic, QtWidgets
import mysql.connector
import mod


def cadastrar():
    # Zerando aviso ao usuário para caso de um cadastro seguido de outro
    janCadastro.msg.setText('')

    # Conectando ao banco
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    # Adicionando os valores digitados pelo usuário a variáveis para tratamento e uso
    cod = str(janCadastro.cod.text())
    desc = janCadastro.desc.text()
    preco = str(janCadastro.preco.text())
    if ',' in preco:
        preco = preco.replace(',', '.')
    # RadioButtons
    if janCadastro.radioInformatica.isChecked():
        categoria = 'Informática'
    elif janCadastro.radioEletronica.isChecked():
        categoria = 'Eletrônica'
    elif janCadastro.radioMecanica.isChecked():
        categoria = 'Mecânica'
    elif janCadastro.radioFerramentas.isChecked():
        categoria = 'Ferramentas'

    # Inserindo no banco de dados
    cursor.execute(
        f'INSERT INTO produtos (código, descrição, preço, categoria) VALUES ("{cod}", "{desc}", {preco}, "{categoria}")')
    banco.commit()
    # Fechando banco
    banco.close()

    # Aviso para o usuário
    janCadastro.msg.setText('Cadastro realizado com sucesso!')

    # Limpando campos
    janCadastro.cod.setText('')
    janCadastro.desc.setText('')
    janCadastro.preco.setText('')


# Preparando para a execução
app = QtWidgets.QApplication([])
telaCadastro = uic.loadUi('formCadVendedor.ui')
primTela = uic.loadUi('janelaLoginVend.ui')
segTela = uic.loadUi('janelaOpcoes.ui')
janCadastro = uic.loadUi('formCadProd.ui')

# Configuração dos elementos da primeira tela
primTela.senha.setEchoMode(QtWidgets.QLineEdit.Password)
primTela.botao_entrar.clicked.connect(logar)
primTela.botao_cadastre.clicked.connect(abrir_tela_cadastro)
# Configuração dos elementos da segunda tela
segTela.botao_sair.clicked.connect(deslogar)
# Configuração dos elementos da tela de cadastro
telaCadastro.senha.setEchoMode(QtWidgets.QLineEdit.Password)
telaCadastro.confirma_senha.setEchoMode(QtWidgets.QLineEdit.Password)
telaCadastro.botao_voltar.clicked.connect(voltar_home)
telaCadastro.enviar_dados.clicked.connect(cadastrar)

# Execução
primTela.show()
app.exec()
