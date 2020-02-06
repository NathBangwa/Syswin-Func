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
        self.login = login
        self.password = password
        self.active = active

def authAdmin(login, password):
    """
        Verifier la validite d'un compte

        :return: bool
    """

    db = DataBaseConnection()

    if db:
        query = f"SELECT * FROM {Admin.tablename} WHERE {Admin.loginCol} = ?"

        try:
            db.cursor.execute(query, login)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error} | {query}"}
        else:
            row = db.cursor.fetchone()

            if row:
                adminlog = Admin(*row)

                if password == adminlog.password:
                    if adminlog.active:

                        return {"flag": "activated"}
                    
                    else:
                        return {"flag": "noActivated"}
                
                else: # invalide password
                    return {"flag": f"invalidPassword", "message": " {query} | {row}"}
            
            else:
                return {"flag": f"invalidLogin", "message": f"{query}"}



