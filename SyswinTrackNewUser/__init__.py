import logging

import azure.functions as func

import json

from . import logics


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    datas = req.params.get('datas')

    

    if not datas:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            datas = req_body.get('datas')
        
    """
        datas = {
            "username": "str",
            "login": "str",
            "password": "str"
    }
    """
    response = {
        "addedAccount": False,
        "AlreadyExistAccount": False,
        "activatedAccount": False,
        "activationDate": str(),
        "expirationDate": str(),
    }

    status_code = 400

    if datas != None and type(datas) is dict:

        login = datas['login']
        password = datas['password']
        username = datas['username']

        if logics.Account.existAccount(login):
            response['AlreadyExistAccount'] = True
        
        else:
            logics.Account.addNewUser(username, login, password)
            
            if logics.Account.existAccount(login):
                thisAccount = logics.Account.getAccountInfos(login)

                response['addedAccount'] = True
                response['activatedAccount'] = bool(thisAccount.status)
                response['activationDate'] = thisAccount.activationDate
                response['expirationDate'] = thisAccount.expirationDate

                status_code = 200

            else:
                status_code = 400

    else:
        pass
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
