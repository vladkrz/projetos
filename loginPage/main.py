from flask import Flask, render_template,request,session,url_for,redirect
#from functools import wraps
from flask_mysqldb import MySQL
import os
from datetime import datetime
#	Cria uma instância/aplicativo da classe Flask com o nome atual do arquivo
#	Adicionamos o diretório da pasta static com static_url_path para scripts JS, CSS e etc	
app = Flask(__name__,static_url_path='/static')

#Configura uma conexão com o MySQL
#Conexão local
app.config['MYSQL_HOST']='localhost'
#Usuário do mysql
app.config['MYSQL_USER']='adm'
#Senha do usuário mysql
app.config['MYSQL_PASSWORD']='1234'
#Banco de dados a ser conectado
app.config['MYSQL_DB']='Login'
#Faz com que os dados sejam apresentados como dicionário chave-valor ao invés de tupla
#Torna mais fácil de trabalhar
app.config['MYSQL_CURSORCLASS']='DictCursor'
#Inicializa/instancia o MySQL
mysql = MySQL(app)

#	Mapeando uma URL para vincular com função a ser renderizado
#	Criando uma rota para raiz
@app.route('/') 	

#	Decorator junto com a função para definir  o comportamento lógico da página 
#	Para a página de login, o methods diz com quais solicitações essa rota irá
#	trabalhar se é POST ou GET ou os dois
#	Esta rota está vinculada a função login()

@app.route('/login', methods=['GET', 'POST']) 
def login():
	#	Variável de erro para retorno de mensagem de Login Correto ou de Login Incorreto
	msg = ''
	#	Verifica o método http da página(GET ou POST) emitido pela requisição
	if request.method == 'POST':
			#	Recebe os valores passados no form de usuário e senha
			username = request.form['username']
			password = request.form['password']
			#	Habilita o Flask a realizar operações SQL
			cursor = mysql.connection.cursor()
			'''
				Executa a consulta/comando no nosso banco e verifica os dados passados 
				no form se é igual ao do banco Login
				Na interpolação de strings(username=%s) deve-se passar as variaveis entre 
				parenteses(tupla)
			'''
			cursor.execute('SELECT * FROM Login WHERE username=%s AND password=%s',(username, password))
			'''
				Armazena em account os dados da consulta executado pelo execute() 
				que retornar do banco para a variável cursor.fetchone(que utiliza o 
				método mysql.connection.cursor())
			'''
			account = cursor.fetchone() #	fetchone busca uma linha por vez na consulta

			#	Verifica se há dados retornados 
			if account:
				#	Logged_in é opcional. Caso queira trabalhar melhor com 
				#	flags de sessão como logado e não logado
				session['logged_in'] = True
				'''
				Armazena dados do usuário no objeto sessão associando um par chave-valor
				onde a chave username recebe a variável username(allan)
				'''
				session['username'] = account['username']
				
				'''
					A variável na função render_template o torna acessível a colocarmos
					no template html, no caso o index.html
					É importante que os templates html estejam na pasta templates e no
					mesmo diretório do arquivo principal da aplicação python 
					já que o render_template busca os templates na pasta templates
					
					Templates ou modelos são arquivos que contem dados estáticos e espaços
					reservados para dados dinamicos. Esses dados dinamicos são manipulados pelo
					Jinja2. O documento final é produzido e renderizado pelo jinja2.
				'''
				'''	
					render_template renderiza/carrega  o arquivo html usando a modelagem Jinja2
					A variável msg está recebendo a variável local da função msg 
					e a variável msg no render_template é uma variável que vai ser usada para preencher
					o campo que tenha o statements {{ msg }} com dados em algum
					canto do código html que tenha os statements {{ msg }}
				'''
				return redirect(url_for('inicio'))
			else:
				msg='Login inválido!\nSeu usuário ou senha estão incorretos.'
				
	return render_template('login.html',msg=msg)


@app.route('/inicio')
def inicio():
	return render_template('index.html',sistemaHorario=datetime.now().strftime('%H:%M, %d/%m/%Y |'))

@app.route('/consulta', methods=['GET','POST'])
def consulta():
	msg_query = ''
	consulta_db = ''
	if request.method == 'POST':
		botao_form = request.form['opcao']
		cursor = mysql.connection.cursor()
		

		if botao_form == 'consulta_codigo':
			cursor.execute('SELECT * FROM Aluno ORDER BY codigo;')
			consulta_db = cursor.fetchall()
			msg_query = 'Consulta realizada com sucesso!'
		
		elif botao_form == 'consulta_nome':
			cursor.execute('SELECT * FROM Aluno ORDER BY nome;')
			consulta_db = cursor.fetchall()
			msg_query = 'Consulta realizada com sucesso!'
		
		else:
			msg_query = 'Aconteceu algum erro na consulta!'
	return render_template('consulta.html',msg_query=msg_query,consulta_db=consulta_db,sistemaHorario=datetime.now().strftime('%H:%M, %d/%m/%Y |'))

@app.route('/aluno', methods=['GET','POST'])
def aluno():
	msg_query = ''
	checa_input_cadastro = ''
	if request.method == 'POST':
		codigo_aluno = request.form['codigo_aluno']
		nome_aluno = request.form['nome_aluno']
		nascimento_aluno = request.form['data_nascimento']
		serie_aluno = request.form['serie_aluno']
		dados_aluno = (codigo_aluno,nome_aluno,nascimento_aluno,serie_aluno)
		sql_query = 'INSERT INTO Aluno(codigo, nome, nascimento, serie) VALUES (%s, %s, %s, %s)'
		cursor = mysql.connection.cursor()

		if codigo_aluno == '3':
			cursor.execute('SELECT codigo,nome,nascimento,serie FROM Aluno WHERE codigo=%s;', (codigo_aluno))
			checa_input_cadastro = cursor.fetchone()
			msg_query = 'Esse código já foi cadastrado!'
		else:
			cursor.execute(sql_query, dados_aluno)
			mysql.connection.commit()
			msg_query = 'Usuário cadastrado com sucesso!'

	return render_template('aluno.html', msg_query=msg_query,checa_input_cadastro=checa_input_cadastro,sistemaHorario=datetime.now().strftime('%H:%M, %d/%m/%Y |'))

@app.route('/materia', methods=['GET', 'POST'])
def materia():
	msg_query = ''
	if request.method == "POST":
		codigo_materia = request.form['codigo_materia']
		nome_materia = request.form['nome_materia']
		
		cursor = mysql.connection.cursor()
		sql_query = 'INSERT INTO Materia(codigo, materia) VALUES (%s, %s)'
		dados_materia = (codigo_materia, nome_materia)

		cursor.execute(sql_query, dados_materia)
		mysql.connection.commit()

		msg_query = 'Matéria cadastrada com sucesso'

	return render_template('materia.html',msg_query=msg_query,sistemaHorario=datetime.now().strftime('%H:%M, %d/%m/%Y |'))

@app.route('/notas', methods=['GET', 'POST'])
def notas():
	msg_query = ''
	if request.method == 'POST':
		bimestre_aluno = request.form['bimestre_aluno']
		codigo_aluno = request.form['codigo_aluno']
		codigo_materia = request.form['codigo_materia']
		nota_aluno = request.form['nota_aluno']

		sql_query = 'INSERT INTO Notas(bimestre,codigo_aluno,codigo_materia,nota) VALUES (%s, %s, %s, %s)'
		dados_notas = (bimestre_aluno, codigo_aluno, codigo_materia, nota_aluno)
		
		cursor = mysql.connection.cursor()
		cursor.execute(sql_query, dados_notas)
		mysql.connection.commit()

		msg_query = 'Nota cadastrada com sucesso!'

	return render_template('notas.html', msg_query=msg_query,sistemaHorario=datetime.now().strftime('%H:%M, %d/%m/%Y |'))
#	Criando uma rota para logout com a função logout
@app.route('/logout')
def logout(): #	Criando uma lógica para a 
	
	#	Mudar a flag de logado para Falso
	session['logged_in'] = False
	#	Remove a chave 'username' criada em session['username'] que armazena o usuário do sistema
	# 	None para caso não ache
	session.pop('username',None)
	'''
	Redireciona após remover o usuário da sessão para a página de login
	O redirecionamento é feito com redirect e url_for, onde ao inves de passarmos a rota,
	a string de rota /login	passamos apenas 'login' que é a função da rota
	para ser redirecionado para essa URL
	
	'''
	return redirect(url_for('login'))

#	Verifica se a aplicação está sendo executado no mesmo arquivo(atual)	
if __name__ == '__main__':
	'''
	Chave secreta para aplicação Flask
	Importante para as sessões de usuário e evitar alterações nos cookies de usuário
	A chave secreta realmente deve ser algo seguro e forte ao invés de um os.urandom
	ou uma string simples
	'''
	app.secret_key= os.urandom(12)
	'''
	Inicia o servidor web de desenvolvimento
	Para uma implantação de produção, use um servidor da Web pronto para produção,
	como gunicorn ou uWSGI .

	O servidor de desenvolvimento e a depuração deve permanecer desativada em 
	ambiente de produção, pois permite código arbitrário python a partir do navegador
	'''
	#host='0.0.0.0'
	app.run(debug=True)

'''
agoraDataHora = datahora.dataHoraAtual()
antigaDataHora = agoraDataHora
while True:
	if antigaDataHora == agoraDataHora.dataHoraAtual():
		continue
	else:'''