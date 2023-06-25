from PyQt5 import uic, QtWidgets
import mysql.connector


# __________________________________________________________________________
# Janela de login do vendedor
def entrar():
    # Atribuindo Login e Senha digitados pelo usuário a variáveis
    login = loginVendedor.login.text()
    senha = loginVendedor.senha.text()
    try:
        # Tentando conectar ao banco
        banco = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='curso_mysql'
        )
        cursor = banco.cursor()
    except:
        loginVendedor.msg_erro.setText('Sem conexão com o banco de dados')
    else:
        try:
            # Solicitando logins do banco
            cursor.execute('SELECT login FROM vendedores')
        except:
            loginVendedor.msg_erro.setText('Conexão interrompida. Não consegui verificar seu login')
        else:
            # Atribuindo login do banco a uma variável
            logins_bd = cursor.fetchall()

            # Validando login
            for c in range(0, len(logins_bd)):
                if login == logins_bd[c][0]:
                    loginVendedor.msg_erro.setText('')
                    try:
                        # Solicitando senha do login digitado pelo usuário
                        cursor.execute(f'SELECT senha FROM vendedores WHERE login = "{login}"')
                    except:
                        loginVendedor.msg_erro.setText('Conexão interrompida. Não consegui verificar a senha')
                    else:
                        # Atribuindo senha do banco a uma variável
                        senha_bd = cursor.fetchall()

                        # Validando senha. Se True executar segunda tela
                        if senha == senha_bd[0][0]:
                            opcoes.msg_logado.setText(f'{login} está logado')
                            loginVendedor.close()
                            opcoes.show()
                        else:
                            loginVendedor.msg_erro.setText('Senha incorreta')
                    break
            else:
                loginVendedor.msg_erro.setText('Login incorreto')
        finally:
            # Fechando banco de dados
            banco.close()


def abrir_cadastrar_vend():
    loginVendedor.msg_erro.setText('')
    loginVendedor.close()
    cadVendedor.show()


# __________________________________________________________________________
# Janela de cadastro de novo vendedor
def cadastrar_vend():
    # Pegando dados digitados pelo usuário
    nome = cadVendedor.dado_nome.text()
    sobrenome = cadVendedor.dado_sobrenome.text()
    login = cadVendedor.login.text()
    senha = cadVendedor.senha.text()
    c_senha = cadVendedor.confirma_senha.text()
    # Validando senha
    if senha == c_senha:
        try:
            banco = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='',
                database='curso_mysql'
            )
            cursor = banco.cursor()
        except:
            cadVendedor.msg_for_user.setText('Não foi possível conectar ao banco de dados')
            cadVendedor.msg_for_user.move(131, 320)
            cadVendedor.msg_for_user.resize(222, 21)
        else:
            try:
                cursor.execute(f'INSERT INTO vendedores (nome, sobrenome, login, senha) VALUES ("{nome}", "{sobrenome}", "{login}", "{senha}")')
                banco.commit()
            except:
                cadVendedor.msg_for_user.setText('Cadastro mal sucedido!')
                cadVendedor.msg_for_user.move(186, 320)
                cadVendedor.msg_for_user.resize(112, 21)
            else:
                cadVendedor.msg_for_user.setText('Cadastro bem sucedido!')
                cadVendedor.msg_for_user.move(182, 320)
                cadVendedor.msg_for_user.resize(121, 21)
            finally:
                banco.close()
    else:     # Falha na confirmação da senha
        cadVendedor.msg_for_user.setText('As senhas digitadas estão diferentes. Verifique e tente novamente')
        cadVendedor.msg_for_user.move(81, 320)
        cadVendedor.msg_for_user.resize(322, 21)


def volta_home():
    cadVendedor.close()
    loginVendedor.show()


# __________________________________________________________________________
# Janela opções/navegação
def saindo():
    loginVendedor.msg_erro.setText('')
    opcoes.close()
    loginVendedor.show()


def ver_produtos_cads():
    opcoes.close()
    consultProdsCadastrados.show()

def abrir_cadastrar_prod():
    opcoes.close()
    cadProduto.show()


# __________________________________________________________________________
# Janela de cadastro de novo produto
def cadastrar_prod():
    # Zerando aviso ao usuário para caso de um cadastro seguido de outro
    cadProduto.msg.setText('')

    # Conectando ao banco
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    # Adicionando os valores digitados pelo usuário a variáveis para tratamento e uso
    cod = str(cadProduto.cod.text())
    desc = cadProduto.desc.text()
    preco = str(cadProduto.preco.text())
    if ',' in preco:
        preco = preco.replace(',', '.')
    # RadioButtons
    if cadProduto.radioInformatica.isChecked():
        categoria = 'Informática'
    elif cadProduto.radioEletronica.isChecked():
        categoria = 'Eletrônica'
    elif cadProduto.radioMecanica.isChecked():
        categoria = 'Mecânica'
    elif cadProduto.radioFerramentas.isChecked():
        categoria = 'Ferramentas'

    # Inserindo no banco de dados
    cursor.execute(f'INSERT INTO produtos (código, descrição, preço, categoria) VALUES ("{cod}", "{desc}", {preco}, "{categoria}")')
    banco.commit()
    # Fechando banco
    banco.close()

    # Aviso para o usuário
    cadProduto.msg.setText('Cadastro realizado com sucesso!')

    # Limpando campos
    cadProduto.cod.setText('')
    cadProduto.desc.setText('')
    cadProduto.preco.setText('')


def volta_opcoes1():
    cadProduto.close()
    opcoes.show()


# __________________________________________________________________________
# Janela de ver os produtos cadastrados
def volta_opcoes2():
    consultProdsCadastrados.close()
    opcoes.show()

# Preparação
app = QtWidgets.QApplication([])

# __________________________________________________________________________
# Preparação
loginVendedor = uic.loadUi('janelaLoginVend.ui')
cadVendedor = uic.loadUi('formCadVendedor.ui')
opcoes = uic.loadUi('janelaOpcoes.ui')
cadProduto = uic.loadUi('formCadProd.ui')
consultProdsCadastrados = uic.loadUi('janelaVerifProd.ui')

# __________________________________________________________________________
# Configurando botões
# Janela de login do vendedor
loginVendedor.senha.setEchoMode(QtWidgets.QLineEdit.Password)
loginVendedor.botao_entrar.clicked.connect(entrar)
loginVendedor.botao_cadastre.clicked.connect(abrir_cadastrar_vend)
# Janela de cadastro de novo vendedor
cadVendedor.senha.setEchoMode(QtWidgets.QLineEdit.Password)
cadVendedor.confirma_senha.setEchoMode(QtWidgets.QLineEdit.Password)
cadVendedor.botao_voltar.clicked.connect(volta_home)
cadVendedor.enviar_dados.clicked.connect(cadastrar_vend)
# Janela opções/navegação
opcoes.botao_sair.clicked.connect(saindo)
opcoes.verifCads.clicked.connect(ver_produtos_cads)
opcoes.cadNovoProd.clicked.connect(abrir_cadastrar_prod)
# Janela de cadastro de novo produto
cadProduto.botao_voltar.clicked.connect(volta_opcoes1)
cadProduto.enviarCad.clicked.connect(cadastrar_prod)
# Janela de ver os produtos cadastrados
consultProdsCadastrados.botao_voltar.clicked.connect(volta_opcoes2)

# Execução
loginVendedor.show()
app.exec()
