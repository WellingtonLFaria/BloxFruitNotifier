import mysql.connector
import re

class DB:
    def __init__(self, host, user, password, database):
        self.con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.con.cursor()
    
    def setUp(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) UNIQUE, password VARCHAR(255), email VARCHAR(255) UNIQUE, PRIMARY KEY(username))")
    
    def users(self):
        self.con.commit()
        self.cursor.execute("SELECT * from users")
        users = self.cursor.fetchall()
        return users
    
    def addUser(self, username, password, email):
        try:
            self.cursor.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')")
            self.con.commit()
            return "Usuário cadastrado com sucesso"
        except mysql.connector.errors.IntegrityError as error:
            regex = r"Duplicate entry '(.*?)' for key '(.*?)'"
            correspondencias = re.search(regex, str(error))
            if correspondencias:
                valor_duplicado = correspondencias.group(1)
                nome_da_chave = correspondencias.group(2)
                if nome_da_chave == 'users.PRIMARY': return "Nome de usuário já cadastrado"
                elif nome_da_chave == 'users.email': return "Email já cadastrado"
                else: return str(error)
    def updateUser(self, username, password, email):
        self.cursor.execute(f"UPDATE users SET password = '{password}', email = '{email}' WHERE username = '{username}'")
        self.con.commit()