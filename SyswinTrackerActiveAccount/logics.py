import pyodbc

from datetime import datetime

import datetime as datetimePack


class DataBaseConnection:
    def __init__(self):
        server = 'tcp:trackertoolsdb.database.windows.net'
        database = 'TrackerTools-sqldb'
        username = 'nathanbangwa'
        password = 'Ski@Nb#07'
        driver= '{ODBC Driver 17 for SQL Server}'
        connectionStr = f"Driver={driver};Server={server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
        
        self.conn = pyodbc.connect(connectionStr)
        self.cursor = self.conn.cursor()


class Account:
    tablename = "ACCOUNT"

    idCol = "id"
    usernameCol = "username"
    loginCol = "login"
    passwordCol = "password"
    firstPCIDCol = "firstPCID"
    secondPCIDCol = "secondPCID"
    activationDateCol = "activationDate"
    expirationDateCol = "expirationDate"
    statusCol = "status"

    def __init__(self, id, username, login, password, firstPCID, secondPCID, activationDate, expirationDate, status):
        self.id = id
        self.username = username
        self.login = login
        self.password = password
        self.firstPCID = firstPCID
        self.secondPCID = secondPCID
        self.activationDate = activationDate
        self.expirationDate = expirationDate
        self.status = status
    
    @staticmethod
    def existAccount(login:str) -> bool:
        """
            permet de verifier l'existance d'un compte
        """

        query = f"SELECT * FROM {Account.tablename} WHERE {Account.loginCol} = ?"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, login)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error}"} 
        else:
            row = db.cursor.fetchone()

            if row:
                return True
            else:
                return False
    
    @staticmethod
    def getAccountInfos(login:str):

        query = f"SELECT * FROM {Account.tablename} WHERE {Account.loginCol} = ?"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, login)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error}"} 
        else:
            row = db.cursor.fetchone()

            if not row:
                return []
            else:
                account = Account(*row)
                account.expirationDate = str(account.expirationDate)
                account.activationDate = str(account.activationDate)
                
                return account
    
    @staticmethod
    def getAllAccounts():
        query = f"SELECT * FROM {Account.tablename}"

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
        

    
    @staticmethod
    def updateAccountStatus(login:str, status:int=0)->bool:
        """
            activate and deactivate an account
        """

        query = f"UPDATE {Account.tablename} SET {Account.statusCol} = ? WHERE {Account.loginCol} = ?"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, status, login)

            if status == 1: # activation
                newActivationDate = datetime.now().date()
                newExpirationDate = (newActivationDate + datetimePack.timedelta(days=155)).date() # warning : + 5 mois

                newActivationDate = str(newActivationDate)
                newExpirationDate = str(newExpirationDate)

                query = f"UPDATE {Account.tablename} SET {Account.activationDateCol} = ?, {Account.expirationDateCol} = ? WHERE {Account.loginCol} = ?"

                db.cursor.execute(query, newActivationDate, newExpirationDate, login)

        except Exception as error:
            return {"flag": "queryError", "message": f"{error}"}
        else:
            db.conn.commit()
            return True
        
    @staticmethod
    def addNewUser(username, login, password, firstPCID='', secondPCID='', activationDate='', expirationDate='', status=0):

        activationDate = expirationDate = str(datetime.now().date())

        query = f"INSERT INTO {Account.tablename} VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, username, login, password, firstPCID, secondPCID, activationDate, expirationDate, status)
        except Exception as error:
            return False
        else:
            db.conn.commit()
            return True
            
    def modifyColumn(self, column, newValue):
        query = f"UPDATE {self.tablename} SET {column} = ? WHERE {self.loginCol} = ? "

        try:
            db = DataBaseConnection()
            db.cursor.execute(query, newValue, self.login)
        except Exception as error:
            return False, query
        else:
            db.conn.commit()

            return True, query

class UpdateApp:
    tablename = "UPDATEAPP"

    idCol = "id"
    versionCol = "version"
    dateupCol = "dateup"
    functionalityCol = "functionality"
    

    def __init__(self, id, version, dateup, functionality):
        self.id = id
        self.version = version
        self.dateup = dateup
        self.functionality = functionality

    @staticmethod
    def getLastVersion():
        query = f"SELECT * FROM {UpdateApp.tablename}"

        try:
            db = DataBaseConnection()
            db.cursor.execute(query)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error}"}
        else:
            lastUpdate = None

            row = db.cursor.fetchone()

            while row:
                lastUpdate = UpdateApp(*row)

                row = db.cursor.fetchone()
            
            lastUpdate.dateup = str(lastUpdate.dateup)
            
            return lastUpdate
        
        return {"flag": "None", "message": ""}
    
    @staticmethod
    def addUpdate(version, functionality=[]):
        pass

def getAllUsers():
    query = f"SELECT * FROM {Account.tablename}"

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


def authentUser(login, password, pcID):
    """
        Verifier la validite d'un compte

        :return: bool
    """

    serverDatetime = datetime.now()

    serverDatetime = str(serverDatetime)

    db = DataBaseConnection()

    if db:
        query = f"SELECT * FROM {Account.tablename} WHERE {Account.loginCol} = ?"

        try:
            db.cursor.execute(query, login)
        except Exception as error:
            return {"flag": "queryError", "message": f"{error} | {query}"}
        else:
            row = db.cursor.fetchone()

            if row:
                accountObj = Account(*row)

                if password == accountObj.password:
                    if not accountObj.firstPCID:
                        status, message = accountObj.modifyColumn(column=accountObj.firstPCIDCol, newValue=pcID)

                        return {"flag": "activated", "message": f"activated first succefuul | {status} | {message} | {row}"} if status else {"flag": "updateError", "message": "error to update first user infos"}

                    elif not accountObj.secondPCID:
                        status, message = accountObj.modifyColumn(column=accountObj.secondPCIDCol, newValue=pcID)

                        return {"flag": "activated", "message": f"activated second succefuul | {status} | {message} | {row}"} if status else {"flag": "updateError", "message": "error to update second user infos"}


                    else: # all keys are used
                        return {"flag": "allKeysUsed", "Userinfos": [accountObj.firstPCID, accountObj.secondPCID]}
                
                else: # invalide password
                    return {"flag": f"invalidPassword", "message": " {query} | {row}"}
            
            else:
                return {"flag": f"invalidLogin", "message": f"{query}"}
