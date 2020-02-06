import logging

import azure.functions as func

import json

from . import logics


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
        
    """
        no required data
    """

    response = {
        "version": str(),
        "updateDate": str(),
        "functionalities": list()
    }

    status_code = 400

    try:

        lastUpdate = logics.UpdateApp.getLastVersion()

        if lastUpdate:
            response['version'] = lastUpdate.version
            response['updateDate'] = lastUpdate.dateup
            response['functionalities'] = list(lastUpdate.functionality.split(";"))
    except:
        status_code = 400
    
    else:
        status_code = 200
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)
