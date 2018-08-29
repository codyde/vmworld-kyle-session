import requests
import os

def authvc(api_url,user,password):
    r = requests.post(f'{api_url}/rest/com/vmware/cis/session', auth=(user,password), verify=False)
    if r.status_code == 200:
        print("Authentication Success")
        return r.json()['value']
    else:
        print("You didn't say the magic word")
        return print("Fail")

def getapidata(path):
    sid = authvc(os.environ['vcurl'],os.environ['vcuser'],os.environ['vcpass'])
    r = requests.get(f'https://vcenter.sddc-34-218-57-180.vmc.vmware.com/rest{path}', headers={'vmware-api-session-id':sid}, verify=False)
    print(r.json())
    if r.status_code == 200:
        return r.json()
    else: 
        return print("Failure with Status Code "+r.status_code)