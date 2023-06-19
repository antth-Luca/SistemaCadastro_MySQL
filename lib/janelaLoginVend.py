def logar():
    # Atribuindo Login e Senha digitados pelo usuário a variáveis
    login = primTela.login.text()
    senha = primTela.senha.text()
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
        primTela.msg_erro.setText('Sem conexão com o banco de dados')
    else:
        try:
            # Solicitando logins do banco
            cursor.execute('SELECT login FROM vendedores')
        except:
            primTela.msg_erro.setText('Conexão interrompida. Não consegui verificar seu login')
        else:
            # Atribuindo login do banco a uma variável
            logins_bd = cursor.fetchall()

            # Validando login
            for c in range(0, len(logins_bd)):
                if login == logins_bd[c][0]:
                    primTela.msg_erro.setText('')
                    try:
                        # Solicitando senha do login digitado pelo usuário
                        cursor.execute(f'SELECT senha FROM vendedores WHERE login = "{login}"')
                    except:
                        primTela.msg_erro.setText('Conexão interrompida. Não consegui verificar a senha')
                    else:
                        # Atribuindo senha do banco a uma variável
                        senha_bd = cursor.fetchall()

                        # Validando senha. Se True executar segunda tela
                        if senha == senha_bd[0][0]:
                            janelaOpcoes.msg_logado.setText(f'{login} está logado')
                            primTela.close()
                            janelaOpcoes.show()
                        else:
                            primTela.msg_erro.setText('Senha incorreta')
                    break
            else:
                primTela.msg_erro.setText('Login incorreto')
        finally:
            # Fechando banco de dados
            banco.close()


def abrir_tela_cadastro():
    primTela.msg_erro.setText('')
    primTela.close()
    telaCadastro.show()