import logging

import azure.functions as func

from . import logics

import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    manag = req.params.get('manag')

    if not manag:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            manag = req_body.get('manag')
        
    response = {"flag": "noFlag", "message": "no message"}
    status_code = 400

    if manag != None and type(manag) is dict:
        """
            manag:{
                "action": str
                "adminLogin": str,
                "userLogin": str,
                "userPassword": str,
                "fullname": str
            }
        """

        adminLogin = "adminLogin"
        userLogin = "userLogin"
        userPassword = "userPassword"
        fullname = "fullname"
        adminPassword = "adminPassword"

        if "action" in manag:
            action = manag['action']

            if action == "addUser":
                if userLogin in manag and userPassword in manag and adminLogin in manag:
                    response = logics.addUserAccount(adminLogin=manag[adminLogin], userLogin=manag[userLogin], userPassword=manag[userPassword])

                    status_code = 200
                
                else:
                    response = {"flag": "missedInfos", "message": "userLogin userPassword adminLogin"}
        
            elif action == "addAdmin":
                if fullname in manag and adminLogin in manag and adminPassword in manag:
                    response = logics.Admin.addAdmin(fullname=manag[fullname], login=manag[adminLogin], password=manag[adminPassword])

                    status_code = 200 if response['flag'] == 'added' else 400
                
                else:
                    response = {"flag": "missedInfos", "message": "adminLogin adminPassword"}

        else:
            response = {"flag": "missedInfos", "message": "action"}

            status_code = 400

    else:
        response = {"flag": "missedInfos", "message": f"manag | {manag} | {type(manag)}"}

        status_code = 400
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
