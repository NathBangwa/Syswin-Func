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
        "datas":
        {
            "login": "str",
            "password": "str"
        }
    """
    response = {
        "activatedAccount": False,
        "existAccount": False,
        "activationDate": "",
        "expirationDate": ""
    }

    status_code = 400

    if datas != None and type(datas) is dict:
        

        login = datas['login']

        if logics.Account.existAccount(login):
            response['existAccount'] = True

            logics.Account.updateAccountStatus(login, status=1)

            thisAccount = logics.Account.getAccountInfos(login)

            response['activatedAccount'] = bool(thisAccount.status)

            response['activationDate'] = thisAccount.activationDate

            response['expirationDate'] = thisAccount.expirationDate

            status_code = 200 if thisAccount.status else 400
        
        else:
            pass


    else:
        pass
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
