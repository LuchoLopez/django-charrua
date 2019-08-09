import zeep

BCU_WSDL = 'http://www.bcu.gub.uy/_vti_bin/search.asmx?WSDL'


def bcu_search(querystr):
    client = zeep.Client(BCU_WSDL)
    resp = None
    req = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <Query xmlns="urn:Microsoft.Search">
          <queryXml>%s</queryXml>
        </Query>
      </soap:Body>
    </soap:Envelope>""" % querystr
    try:
        resp = client.service.Query(req)
    except Exception as e:
        print(e)
    return resp


def bcu_status():
    client = zeep.Client(BCU_WSDL)
    status = 'UNKNOWN'
    try:
        status = client.service.Status()
    except Exception as e:
        print(e)
    return status
