'''
Usage:
    1. Install ZStack Enterprise.
    2. Execute CLI to go to zstackcli mode: 
        source /var/lib/zstack/virtualenv/zstackcli/bin/activate
    3. Run the demo script to create a zone in zstack.
        python ./zs_api_sdk.py
The python sdk interfaces are wrapped inside zs_api_sdk.py, 
user can refer to the script to customize their own expected scripts.
'''

import apibinding.api_actions as api_actions
from apibinding import api
import xml.etree.cElementTree as etree
import apibinding.inventory as inventory
import time
import os
import sys
import traceback
import hashlib

zstack_server_ip = os.environ['ZS_SERVER_IP']
user_name = 'admin'
user_password = 'password'

#For user's program: must keep
def sync_call(apicmd, session_uuid):
    api_instance = api.Api(host = zstack_server_ip, port = '8080')
    if session_uuid:
        api_instance.set_session_to_api_message(apicmd, session_uuid)
    (name, reply) = api_instance.sync_call(apicmd)
    if not reply.success: raise api.ApiError("Sync call at %s: [%s] meets error: %s." % (zstack_server_ip, apicmd.__class__.__name__, api.error_code_to_string(reply.error)))
    #print("[Sync call at %s]: [%s] Success" % (zstack_server_ip, apicmd.__class__.__name__))
    return reply

#For user's program: must keep
def async_call(apicmd, session_uuid):
    api_instance = api.Api(host = zstack_server_ip, port = '8080')
    api_instance.set_session_to_api_message(apicmd, session_uuid)
    (name, event) = api_instance.async_call_wait_for_complete(apicmd)
    time.sleep(1)
    if not event.success: raise api.ApiError("Async call at %s: [%s] meets error: %s." % (zstack_server_ip, apicmd.__class__.__name__, api.error_code_to_string(reply.error)))
    #print("[Async call at %s]: [%s] Success" % (zstack_server_ip, apicmd.__class__.__name__))
    return event

#For user's program: must keep
def login_as_admin():
    accountName = inventory.INITIAL_SYSTEM_ADMIN_NAME
    password = inventory.INITIAL_SYSTEM_ADMIN_PASSWORD
    accountName = user_name
    password = user_password
    return login_by_account(accountName, password)

#For user's program: must keep
def login_by_account(name, password, timeout = 60000):
    login = api_actions.LogInByAccountAction()
    login.accountName = name
    login.password = hashlib.sha512(password).hexdigest()
    login.timeout = timeout
    session_uuid = async_call(login, None).inventory.uuid
    return session_uuid

#For user's program: must keep
def logout(session_uuid):
    logout = api_actions.LogOutAction()
    logout.timeout = 60000
    logout.sessionUuid = session_uuid
    async_call(logout, session_uuid)

#For user's program: must keep
def execute_action_with_session(action, session_uuid, async=True):
    if session_uuid:
        action.sessionUuid = session_uuid
        if async:
            evt = async_call(action, session_uuid)
        else:
            evt = sync_call(action, session_uuid)
    else:
        session_uuid = login_as_admin()
        try:
            action.sessionUuid = session_uuid
            if async:
                evt = async_call(action, session_uuid)
            else:
                evt = sync_call(action, session_uuid)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e
        finally:
            # New login must be logout. If the active login session
            # exceed the limit, no account login is allowed. 
            # The default active logined session limit is  500.
            logout(session_uuid)

    return evt


def gen_query_conditions(name, op, value, conditions=[]):
    new_conditions = [{'name': name, 'op': op, 'value': value}]
    new_conditions.extend(conditions)
    return new_conditions

def query_vm_by_host(host_uuid, conditions = [], session_uuid = None):
    action = api_actions.QueryVmInstanceAction()
    action.conditions = gen_query_conditions('hostUuid', '=', host_uuid, conditions)
    evt = execute_action_with_session(action, session_uuid)
    return evt.inventories

