from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel
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
        try:  # Tenta conectar no banco e validar se ja existe cadastro com aquele nome de usuário
            banco = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='',
                database='curso_mysql'
            )
            cursor = banco.cursor()

            query = 'SELECT * FROM vendedores WHERE login = %s'
            values = (login,)
            cursor.execute(query, values)

            result_query = cursor.fetchone()
            if result_query is not None:
                cadVendedor.msg_for_user.setText('Cadastro com esse usuário já existe')
                cadVendedor.msg_for_user.move(156, 320)
                cadVendedor.msg_for_user.resize(172, 21)
            else:  # Se não existe ele faz um novo registro
                query = 'INSERT INTO vendedores (nome, sobrenome, login, senha) VALUES (%s, %s, %s, %s)'
                values = (nome, sobrenome, login, senha)
                cursor.execute(query, values)
                banco.commit()

                cadVendedor.msg_for_user.setText('Cadastro bem sucedido!')
                cadVendedor.msg_for_user.move(182, 320)
                cadVendedor.msg_for_user.resize(121, 21)

        except mysql.connector.Error:
            cadVendedor.msg_for_user.setText('Cadastro mal sucedido!')
            cadVendedor.msg_for_user.move(186, 320)
            cadVendedor.msg_for_user.resize(112, 21)

        finally:
            if banco.is_connected():
                banco.close()

    else:  # Falha na confirmação da senha
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

    atualizar_lista()


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
    cursor.execute(
        f'INSERT INTO produtos (código, descrição, preço, categoria) VALUES ("{cod}", "{desc}", {preco}, "{categoria}")')
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


def excluir_registro():
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    selectNaInterface = consultProdsCadastrados.tableWidget.currentRow()

    cursor.execute('SELECT id_prod FROM produtos')
    idsLidos = cursor.fetchall()
    selectId = str(idsLidos[selectNaInterface][0])

    cursor.execute(f'DELETE FROM produtos WHERE id_prod = {selectId}')

    banco.close()

    atualizar_lista()


def atualizar_lista():
    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    query = 'SELECT * FROM produtos'
    cursor.execute(query)
    dados = cursor.fetchall()

    consultProdsCadastrados.tableWidget.setRowCount(len(dados))
    consultProdsCadastrados.tableWidget.setColumnCount(5)

    for c in range(0, len(dados)):
        for i in range(0, 5):
            consultProdsCadastrados.tableWidget.setItem(c, i, QtWidgets.QTableWidgetItem(str(dados[c][i])))

    banco.close()


def edicao():
    selectNaInterface = consultProdsCadastrados.tableWidget.currentRow()

    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    cursor.execute('SELECT id_prod FROM produtos')
    idsLidos = cursor.fetchall()
    selectId = str(idsLidos[selectNaInterface][0])

    cursor.execute(f'SELECT * FROM produtos WHERE id_prod = {selectId}')
    dados = cursor.fetchall()

    banco.close()

    editProdsCadastrados.lineId.setText(str(dados[0][0]))
    editProdsCadastrados.lineCod.setText(str(dados[0][1]))
    editProdsCadastrados.lineNome.setText(str(dados[0][2]))
    editProdsCadastrados.linePreco.setText(str(dados[0][3]))
    editProdsCadastrados.lineCategoria.setText(str(dados[0][4]))

    editProdsCadastrados.show()


def pesquisar():
    busca = consultProdsCadastrados.barraPesq.text()

    if consultProdsCadastrados.radioId.isChecked():
        criterio = 'id_prod'
    elif consultProdsCadastrados.radioCod.isChecked():
        criterio = 'código'
    elif consultProdsCadastrados.radioDesc.isChecked():
        criterio = 'descrição'
    elif consultProdsCadastrados.radioCat.isChecked():
        criterio = 'categoria'

    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    query = f'SELECT * FROM produtos WHERE {criterio} = {busca}'
    cursor.execute(query)
    result = cursor.fetchone()
    banco.close()

    consultProdsCadastrados.tableWidget.clearContents()
    consultProdsCadastrados.tableWidget.setRowCount(0)
    consultProdsCadastrados.tableWidget.setColumnCount(0)

    consultProdsCadastrados.tableWidget.setRowCount(len(result))
    consultProdsCadastrados.tableWidget.setColumnCount(5)
    for l in range(0, len(result)):
        for c in range(0, 5):
            consultProdsCadastrados.tableWidget.setItem(l, c, QtWidgets.QTableWidgetItem(str(result[c])))


# __________________________________________________________________________
# Janela para editar produto
def salvar_edicao():
    id_prod = editProdsCadastrados.lineId.text()
    codigo = editProdsCadastrados.lineCod.text()
    descricao = editProdsCadastrados.lineNome.text()
    preco = editProdsCadastrados.linePreco.text()
    categoria = editProdsCadastrados.lineCategoria.text()

    banco = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='curso_mysql'
    )
    cursor = banco.cursor()

    cursor.execute(
        f'UPDATE produtos SET código = "{codigo}", descrição = "{descricao}", preço = "{preco}", categoria = "{categoria}" WHERE id_prod = {id_prod}')
    banco.commit()

    banco.close()

    atualizar_lista()

    editProdsCadastrados.close()


# __________________________________________________________________________
# Preparação
app = QtWidgets.QApplication([])

loginVendedor = uic.loadUi('janelaLoginVend.ui')
cadVendedor = uic.loadUi('formCadVendedor.ui')
opcoes = uic.loadUi('janelaOpcoes.ui')
cadProduto = uic.loadUi('formCadProd.ui')
consultProdsCadastrados = uic.loadUi('janelaVerifProd.ui')
editProdsCadastrados = uic.loadUi('editProduto.ui')

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
consultProdsCadastrados.excluirRegistro.clicked.connect(excluir_registro)
consultProdsCadastrados.editarRegistro.clicked.connect(edicao)
consultProdsCadastrados.pesquisar.clicked.connect(pesquisar)
# Janela de editar os produtos salvos
editProdsCadastrados.salvarEdicao.clicked.connect(salvar_edicao)


# Execução
loginVendedor.show()
app.exec()
