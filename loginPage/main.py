from flask import Flask, flash, render_template,request,session,url_for,redirect
#from functools import wraps
from flask_mysqldb import MySQL
import os
#Cria uma instância/aplicativo da classe Flask 
app = Flask(__name__)

#Configura uma conexão com o MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='adm'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='Login'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#Inicializa o MySQL
mysql = MySQL(app)



#Criando uma rota para raiz
@app.route('/') 	
#Decorator junto com a função para definir  o comportamento lógico da página 
@app.route('/login', methods=['GET', 'POST']) #Para a página de login, o methods lida com solicitação POST ou GET
def login():
	#Variável de erro para retorno de status de Login Correto ou de Login Incorreto
	msg = ''
	#Verifica o método real(GET ou POST) emitido pelo sistema
	if request.method == 'POST':
			#Recebe os valores passados no form de usuário e senha
			username = request.form['username']
			password = request.form['password']
			#Habilita o Flask a realizar operações SQL
			cursor = mysql.connection.cursor()
			#Executa a consulta no nosso banco e verifica os dados passados no form se é igual ao do banco Login
			#Na interpolação de strings(username=%s) deve-se passar as variaveis entre parenteses(tupla)
			cursor.execute('SELECT * FROM Login WHERE username=%s AND password=%s',(username, password))
			'''Armazena em account os dados resultantes pela query execute() 
			que retornar do banco para a variável cursor(que utiliza o 
			método mysql.connection.cursor()) '''
			account = cursor.fetchone() #fetchone Faz uma busca uma por vez e normalmente uma linha 

			#Verifica se há dados 
			if account:
				#Cria uma sessão para o usuário
				session['logged_in'] = True
				session['administrador'] = account['username']
				msg='Login Successfully', 'success'
				return render_template('index.html', msg=msg)
			else:
				msg='Login inválido. Seu usuário ou senha estão incorretos. Tente novamente!'
				
	return render_template('login.html',msg=msg)

#Criando uma rota para logout com a função logout
@app.route('/logout')
def logout(): #Criando uma lógica para a 
	#Libera a variável de sessão passando o usuário da sessão. None para se caso não ache
	session.pop('administrador',None)
	#Redireciona após remover o usuário da sessão para a página de login
	return redirect(url_for('login'))
	
if __name__ == '__main__':
    app.secret_key= os.urandom(12)
    app.run(debug=True)