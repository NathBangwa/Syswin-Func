import pyodbc


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

def modifyInfos(login, value):
    query = f"UPDATE {AutorizedLogin.tablename} SET {AutorizedLogin.firstUserCol}=? WHERE {AutorizedLogin.loginCol} = ?"

    try:
        db = DataBaseConnection()
        db.cursor.execute(query, value, login)
    except Exception as error:
        return {"flag": "queryError", "message": f"{error}"}
    else:
        db.conn.commit()
        return {"flag": "True", "message": f"modificated"}


class AutorizedLogin:
    tablename = "AUTORIZEDLOGIN"

    loginIDCol = "LoginID"
    loginCol = "Login"
    passwordCol = "Password"
    firstUserCol = "FirstUser"
    secondUserCol = "SecondUser"

    def __init__(self, loginID, login, password, firstUser, secondUser):
        self.loginID = loginID
        self.login = login
        self.password = password
        self.firstUser = firstUser
        self.secondUser = secondUser
    
    def modifyInfos(self, column, value):
        query = f"UPDATE {self.tablename} SET {column}=? WHERE {self.loginCol} = ?"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, value, self.login)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error}"}
        else:
            db.conn.commit()
            return True

def adduser(login, password):
    """
        add an user
    """

    query = f"SELECT * FROM {AutorizedLogin.tablename} WHERE {AutorizedLogin.loginCol} = ?"

    try:
        db = DataBaseConnection()
        db.cursor.execute(query, login)
    except Exception as error:
        return {"flag": "queryError", "message": f"{error}"} 
    else:
        row = db.cursor.fetchone()

        if not row:
            query = f"INSERT INTO {AutorizedLogin.tablename} VALUES(?, ?, ?, ?)"

            try:
                db = DataBaseConnection()
                db.cursor.execute(query, login, password, '', '')
            except Exception as error:
                return {"flag": "queryError", "message": f"{error}"}
            else:
                db.conn.commit()
                return {"flag": "added"}
        
        else:
            return {"flag": "existMail", "message": f"the login {login} already exist"}

def getAllUsers():
    query = f"SELECT * FROM {AutorizedLogin.tablename}"

    try:
        db = DataBaseConnection()
        db.cursor.execute(query)
    except Exception as error:
        return {"flag": "queryError", "message": f"{error}"}
    else:
        listUsers = list()

        row = db.cursor.fetchone()

        while row:
            listUsers.append(list(row))

            row = db.cursor.fetchone()
        
        return {"flag": "done", "datas": listUsers}
    
    return {"flag": "None", "message": ""}