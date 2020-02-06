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
                "action": str,
                "password": str,
                "userInfos": "username/date"
            }
        """

        if "action" in manag:
            action = manag['action']

            if action == "addUser":
                if "login" in manag and "password" in manag:
                    response = logics.adduser(login=manag['login'], password=manag['password'])

                    status_code = 200 if response['flag'] == 'added' else 400

                else:
                    response["flag"] = "missingInfos"
                    response['message'] = "login password"
                    status_code = 400

            elif action == "getAllUsers":
                response = logics.getAllUsers()
                status_code = 200

            else:
                response["flag"] = "invalidAction"
                response['message'] = "action missed"
                status_code = 400

        else:
            response["flag"] = "missingInfos"
            response['message'] = "action missed"
            status_code = 400

    else:
        response = {"flag": "missedInfos", "message": f"manag | {manag} | {type(manag)}"}

        status_code = 400
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
