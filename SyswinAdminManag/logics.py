import pyodbc

from datetime import datetime


class DataBaseConnection:
    def __init__(self):
        server = 'tcp:syswintracker.database.windows.net'
        database = 'syswin-tracker-db'
        username = 'nathanbangwa'
        password = 'Ski@Nb#07'
        driver= '{ODBC Driver 17 for SQL Server}'
        connectionStr = f"Driver={driver};Server={server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
        
        self.conn = pyodbc.connect(connectionStr)
        self.cursor = self.conn.cursor()
    
        
class AutorizedLogin:
    tablename = "AUTORIZEDLOGIN"

    loginIDCol = "LoginID"
    loginCol = "Login"
    passwordCol = "Password"
    firstUserCol = "FirstUser"
    secondUserCol = "SecondUser"

    def __init__(self, loginID, login, password, firstUser='', secondUser=''):
        self.loginID = loginID
        self.login = login
        self.password = password
        self.firstUser = firstUser
        self.secondUser = secondUser
    
    def modifyInfos(self, column, value):
        query = f"UPDATE {self.tablename} SET {column} = ? WHERE {self.loginCol} = ?"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, value, self.login)
        except Exception as error:
            return False, query
        else:
            db.conn.commit()

            return True, query
    
    @staticmethod
    def addUser(login, password):
        query = f"INSERT INTO {AutorizedLogin.tablename} VALUES(?, ?, ?, ?)"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, login, password, '', '')
        except Exception as error:
            return False, query
        else:
            db.conn.commit()

            return True, query

class Admin:
    tablename = "Admin"

    adminIDCol = "adminId"
    fullnameCol = "fullname"
    loginCol = "Login"
    passwordCol = "Password"
    activeCol = "active"

    def __init__(self, adminId, fullname, login, password, active):
        self.adminId = adminId
        self.fullname = fullname
        self.login = login
        self.password = password
        self.active = active

    @staticmethod
    def addAdmin(fullname, login, password, active=1):
        query = f"INSERT INTO {Admin.tablename} VALUES(?, ?, ?, ?)"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, fullname, login, password, active)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error} | {query}"}
        else:
            db.conn.commit()

            return {"flag": "added", "message": f"| {query}"}

    @staticmethod
    def modifyAdmin(fullname, login, password, active=1):
        query = f"INSERT INTO {Admin.tablename} VALUES(?, ?, ?, ?)"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, fullname, login, password, active)
        except Exception as error:
                return {"flag": "queryError", "message": f"{error} | {query}"}
        else:
            db.conn.commit()

            return {"flag": "added", "message": f"| {query}"}

class Infos:
    tablename = "INFOS"

    infosIdCol = "infosID"
    adminLoginCol = "adminLogin"
    userLoginCol = "userLogin"
    datatimeCol = "datetime"

    @staticmethod
    def addInfos(adminLogin, userLogin):
        serverDateTime = datetime.now()

        serverDateTime = str(serverDateTime)

        query = f"INSERT INTO {Infos.tablename} VALUES(?, ?, ?)"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, adminLogin, userLogin, serverDateTime)
        except Exception as error:
            return False, {"flag": "queryError", "message": f"{error} | {query}"}
        else:
            db.conn.commit()
            return True, {"flag": "added", "message": f"| {query}"}





    
def addUserAccount(adminLogin, userLogin, userPassword):
    """
        Verifier la validite d'un compte

        :return: bool
    """

    db = DataBaseConnection()

    if db:
        query = f"SELECT * FROM {AutorizedLogin.tablename} WHERE {AutorizedLogin.loginCol} = ?"

        try:
            db.cursor.execute(query, userLogin)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error} | {query}"}
        else:
            row = db.cursor.fetchone()

            if not row:
                status, message = AutorizedLogin.addUser(userLogin, userPassword)

                if status:
                    infoAdded, message = Infos.addInfos(adminLogin=adminLogin, userLogin=userLogin)
                
                    if infoAdded:
                        return {"flag": "added", "message": f"add success| {status} | {message} | {row}"}
                    
                    else:
                        return {"flag": "addError", "message": "error to add infos"}
                
                else:
                    return {"flag": "addError", "message": "error to add user"}
            
            else:
                return {"flag": f"loginExist", "message": f"{query}"}



