"""
Initial structure for classes and functions as they pertain to VMCS automation functions.

Worked on by: 
    Cody De Arkland (cdearkland@vmware.com), VMware
    Grant Orchard (gorchard@vmware.com), VMware

"""
import requests
import json
import os
import sys
from prettytable import PrettyTable


class Session(object):
    """
    Session class for instantiating a logged in session
    for VMCS.

    Requires refresh token from VMCS portal to instantiate
    """
    def __init__(self, auth_token):
        self.token = 'Bearer '+auth_token
        self.headers = {'Content-Type':'application/json','authorization': self.token}
        self.baseurl = 'https://api.mgmt.cloud.vmware.com'

    @classmethod
    def login(self, refresh_token):
            baseurl = 'https://api.mgmt.cloud.vmware.com'
            uri = '/iaas/login'
            headers = {'Content-Type':'application/json'}
            payload = json.dumps({"refreshToken": refresh_token })
            try:
                r = requests.post(f'{baseurl}{uri}', headers = headers, data = payload)
                print('Login successful.')
                auth_token = r.json()['token']
                return self(auth_token)
            except requests.exceptions.HTTPError as e:
                print(e)
                sys.exit(1)

class Blueprint(object):
    """
    Classes for Blueprint methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = '/blueprint/api/blueprints/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j['links']:
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @staticmethod
    def describe(session, bp):
        table = PrettyTable(['Name', 'CreatedBy', 'LastUpdated'])
        uri = f'/blueprint/api/blueprints/{bp}'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code == 403:
            print(f'You do not have sufficient access to org to list its details.')
        else:
            table.add_row([j['name'], j['createdBy'], j['updatedAt']])
        print(table)
        return j

    @staticmethod
    def detail(session, bp):
        uri= f'/blueprint/api/blueprints/{bp}'
        print(uri)
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        return j
    
    @staticmethod
    def listastable(session,bp):
        table = PrettyTable(['Name', 'Project', 'Created By', 'Creation Date'])
        for i in bp:
            uri = f'/blueprint/api/blueprints/{i}'
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            table.add_row([j['name'], j['projectName'], j['createdBy'], j['createdAt']])
        return print(table)

    @staticmethod
    def listastable(session,bp):
        table = PrettyTable(['Name', 'Project', 'Created By', 'Creation Date'])
        for i in bp:
            uri = f'/blueprint/api/blueprints/{i}'
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            table.add_row([j['name'], j['projectName'], j['createdBy'], j['createdAt']])
        return print(table)