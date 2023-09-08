# Device Import Settings
# # specify filepath to metavariable Excel file
# file_path = "example.xlsx"
file_path = "path/to/your/file"

# # specify which sheet to use
# active_sheet = "metavariables"  # name of the sheet containing metavariables
active_sheet = None  # specify None to use the active (first) sheet of the Excel file

# # select devices - select the devices to include
# device_list = "Nashville_Spoke_01"  # include just this device
# device_list = ["Nashville_Spoke_01", "LasVegas_Spoke_02"]  # include any device with the hostname in list
device_list = None  # include all devices

# # select negation
negate = False  # set to true if you wish to include every device except the one(s) listed in the device_list

# # update default values
update_defaults = True  # if set to false, the global values row will be ignored

# FortiManager Parameters
adom = 'root'                       # name of adom; if ADOM's are not in use, specify 'root'
host = "Your_FortiManager_IP:port"  # the IP address or hostname of FortiManager
username = "Your_Username"          # the username used to log into FMG
password = "Your_Password"          # the password used to log into FMG
lock_adom = False   # set to true if workflow mode is in use and ADOM must be locked before editing
verify_cert = True  # set to False, if your FMG instance is using an untrusted certificate

# Enable/Disable Streamline
streamline = True   # if set to False, script will pause between generating JSON file and uploading it
