import requests
import pprint
import atexit
import inspect

# pretty print object
pp = pprint.PrettyPrinter()


def api_check(results, call_name, suppress):
    # check if call is OK
    if results.reason == 'OK':
        # if call is OK return successful
        if not suppress:
            print(f"{call_name}: API successful\033[0m")
        return results.json()
    else:
        # if call is not OK return failure, reason code, and results
        if suppress is False:
            print(f'{call_name}: API failed - code: {results.status_code}\033[0m')
            print(results.text)
        return None


class FmgAPICall:
    def __init__(self, host, username, password, adom=None, adom_lock=False, verify=True):
        # set self paramters
        self.host = host            # define hostname or IP address
        self.username = username    # define FMG admin username
        self.password = password    # define FMG admin password
        self.cookie = ''            # define placeholder for session cookie
        self.url = f"https://{host}/jsonrpc"    # define standard API url off of host
        if adom is None:            # define the ADOM
            self.adom = 'root'
        else:
            self.adom = adom
        self.adom_lock = adom_lock  # define boolean for enabling/disabling locking the ADOM
        self.verify = verify

        atexit.register(self.cleanup)   # define cleanup function - this function is run when FmgAPICall is destroyed

        # login to FMG
        self.login(suppress=True)   # logs into FortiManager
        # lock FMG if necessary
        if self.adom_lock:
            self.lock(suppress=True)    # locks the ADOM if locking is enabled

    def cleanup(self):
        # unlock adom
        if self.adom_lock:
            self.unlock(suppress=True)  # unlocks the ADOM if locking is enabled
        # logout of fmg
        self.logout(suppress=True)      # logs out of FMG, assuming the session was actually started


    def example(self):
        pass
        # Define Action
        # Define JSON body
        # Make API call, check, and return

    def getAdomFmgVariable(self, variable=None, adom=None, suppress=False):
        # Define adom
        if adom is None:
            adom = self.adom

        # Define Action
        if variable is None:
            action = f"pm/config/adom/{adom}/obj/fmg/variable"
        else:
            action = f"pm/config/adom/{adom}/obj/fmg/variable/{variable}"

        # Define JSON body
        body = {
            "method": "get",
            "params": [{
                "url": action
            }],
            "session": self.cookie,
            "id": 1
        }

        # Make API call, check, and return
        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    def setAdomFmgVariable(self, data, variable=None, adom=None, suppress=False):
        # Define Adom
        if adom is None:
            adom = self.adom

        # Define Action
        if variable is None:
            action = f"pm/config/adom/{adom}/obj/fmg/variable"
        else:
            action = f"pm/config/adom/{adom}/obj/fmg/variable/{variable}"

        # Define JSON body
        body = {
            "method": "set",
            "params": [{
                "data": data,
                "url": action
            }],
            "session": self.cookie,
            "id": 1
        }

        # Make API call, check, and return
        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    def updateAdomFmgVariable(self, data, variable=None, adom=None, suppress=False):
        # Define Adom
        if adom is None:
            adom = self.adom

        # Define Action
        if variable is None:
            action = f"pm/config/adom/{adom}/obj/fmg/variable"
        else:
            action = f"pm/config/adom/{adom}/obj/fmg/variable/{variable}"

        # Define JSON body
        body = {
            "method": "update",
            "params": [{
                "data": data,
                "url": action
            }],
            "session": self.cookie,
            "id": 1
        }

        # Make API call, check, and return
        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    def systemLogingUser(self, suppress=False):
        # Define Action
        action = "sys/login/user"

        # Define JSON body
        body = {
            "method": "exec",
            "params": [{
                "data": {
                    "passwd": self.password,
                    "user": self.username
                },
                "url": action
            }],
            "session": None,
            "id": 1
        }

        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    def systemLogout(self, suppress=False):
        # Define Action
        action = "sys/logout"

        # Define JSON body
        body = {
            "method": "exec",
            "params": [{"url": action}],
            "session": self.cookie,
            "id": 1
        }

        # Make API call, check, and return
        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    def workspaceLockAdom(self, suppress=False):
        # Define Action
        action = f"dvmdb/adom/{self.adom}/workspace/lock"

        # Define JSON body
        body = {
            "method": "exec",
            "params": [{"url": action}],
            "session": self.cookie,
            "id": 1
        }

        # Make API call, check, and return
        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    def workspaceUnlockAdom(self, suppress=False):
        # Define Action
        action = f"dvmdb/adom/{self.adom}/workspace/unlock"

        # Define JSON body
        body = {
            "method": "exec",
            "params": [{"url": action}],
            "session": self.cookie,
            "id": 1
        }

        # Make API call, check, and return
        results = requests.post(self.url, json=body, verify=self.verify)
        return api_check(results, inspect.stack()[0][3], suppress)

    # FMG login action
    def login(self, suppress):
        try:
            result = self.systemLogingUser(suppress)        # makes the login API call
            if result["result"][0]["status"]["code"] == 0:
                self.cookie = result["session"]             # if the call was successful, set the session cookie
            else:
                print("\n\nError: could not login to FMG.\n\n") # if the call was unsuccessful, print the error
                pp.pprint(result)
                self.adom_lock = False  # and set locking to False so that clean up doesn't try and unlock it
                exit(2)
        except TimeoutError:
            print("Error: could not connect to FMG.")
            exit(1)

    def logout(self, suppress):
        if self.cookie != '':
            results = self.systemLogout(suppress)       # logout if the session was active

    def lock(self, suppress):
        result = self.workspaceLockAdom(suppress)
        if result["result"][0]["status"]["code"] != 0:
            self.adom_lock = False
            print("\n\nError: could not lock ADOM.\n\n")
            pp.pprint(result)
            exit(3)

    def unlock(self, suppress):
        result = self.workspaceUnlockAdom(suppress)
        if result["result"][0]["status"]["code"] != 0:
            print("\n\nError: failed to unlock ADOM.\n\n")
