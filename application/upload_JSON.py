import pprint
import urllib3
import json
from application.FMG_API import FmgAPICall
from application.constants import *
from user_settings import *

# enable/disable debug
debug = False   # if True, script will upload data one variable at a time for better debugging

# Disable certificate verification warnings
if verify_cert is False:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# pretty print object
pp = pprint.PrettyPrinter()

# Import JSON
with open(f"{OUTPUT}", 'r') as json_file:
    data = json.load(json_file)


# Create FMG Object
FMG = FmgAPICall(host=host, username=username, password=password, adom=adom, adom_lock=lock_adom, verify=verify_cert)


# Upload Metavariables
if debug:   # uploads data one variable at a time for better visibility
    for variable in data:
        print(f"Metavariable is being updated.  Variable: {variable_color}{variable[DEVICE]}{default_color}")
        result = FMG.setAdomFmgVariable(data=[variable], suppress=True)
        if result["result"][0]["status"]["message"] == "OK":
            print("FortiManager MetaVariable updated successfully")
        else:
            print(f"Error: {error_color}{result}{default_color}")
        print()
else:       # bulk upload
    print(FMG.setAdomFmgVariable(data=data))
