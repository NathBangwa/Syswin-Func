import logging

import azure.functions as func

from . import logics

import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    auth = req.params.get('auth')
    if not auth:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            auth = req_body.get('auth')
        
    response = {"flag": "noFlag", "message": "no message"}
    status_code = 400

    if auth != None and type(auth) is dict:
        """
            auth:{
                "login": str,
                "password": str,
                "userInfos": "username/date"
            }
        """

        login = "login"
        password = "password"
        userInfos = "userInfos"

        if login in auth and password in auth and userInfos in auth:
            response = logics.activateAccount(login=auth[login], password=auth[password], userInfos=auth[userInfos])

            status_code = 200
        
        elif "update" in auth:
                response = logics.modifyInfos(login="nathanbangwa@hotmail.com", value="testosterone")

                status_code = 400

        else:
            response = {"flag": "missedInfos", "message": "login password userInfos"}

            status_code = 400

    else:
        response = {"flag": "missedInfos", "message": f"auth | {auth} | {type(auth)}"}

        status_code = 400
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
