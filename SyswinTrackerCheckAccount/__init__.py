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
            "password": "str",
            "pcID": "str
        }
    """

    response = {
        "acceptNewActivation": False,
        "existAccount": False,
        "activatedAccount": False,
        "invalidLogin": False,
        "invalidPassword": False,
        "allKeysUsed": False,
        "pcIDS": [],
        "username": "",
        "activationDate": "",
        "expirationDate": ""

    }

    status_code = 400

    if datas != None and type(datas) is dict:
        login = datas['login']
        password = datas['password']
        pcID = datas['pcID']

        if logics.Account.existAccount(login):
            response['existAccount'] = True

            thisAccount = logics.Account.getAccountInfos(login)

            if thisAccount.password == password:
                if thisAccount.status == 1:
                    if not thisAccount.firstPCID or not thisAccount.secondPCID:
                        response['acceptNewActivation'] = True
                        status_code = 200

                        if not thisAccount.firstPCID:
                            thisAccount.modifyColumn(thisAccount.firstPCIDCol, pcID)
                        
                        else: # not thisAccount.secondPCIDCol
                            thisAccount.modifyColumn(thisAccount.secondPCIDCol, pcID)
                            response['allKeysUsed'] = True
                    
                    else:
                        response['acceptNewActivation'] = False
                        response['allKeysUsed'] = True
                else:
                    pass
            
            else:
                response['invalidPassword'] = True
                status_code = 400
            
            thisAccount = logics.Account.getAccountInfos(login)

            response['activatedAccount'] = True if thisAccount.status else False

            response['pcIDS'] = [thisAccount.firstPCID, thisAccount.secondPCID]

            response['username'] = thisAccount.username
            
            response['activationDate'] = thisAccount.activationDate

            response['expirationDate'] = thisAccount.expirationDate
        
        else:
            response['existAccount'] = False
            response['invalidLogin'] = True

    else:
        pass

    # condition 

    # valide password and login
    validLoginPassword = not(response["invalidPassword"]) and not(response["invalidLogin"])

    # esist and active account
    existValidAccount = response["existAccount"] and response["activatedAccount"]

    response["acceptNewActivation"] = validLoginPassword and existValidAccount  and not(response["allKeysUsed"])
                                      
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
