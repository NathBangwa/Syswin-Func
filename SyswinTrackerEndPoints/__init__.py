import logging

import azure.functions as func

import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    response = {
        "server": "https://trackertools-func.azurewebsites.net",
        "code": "t4RJy0YkJBZNSCIGQ9YyDdwVcZAvbB1Ef2FIsmVEq3TOj5i8TSUaxg=="
    }

    status_code = 200
    
    response = json.dumps(response)

    return func.HttpResponse(response, status_code=status_code)

    