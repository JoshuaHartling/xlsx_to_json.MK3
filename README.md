# xlsx_to_json.MK3
This project is meant to assist in uploading mass amounts of metavariable data to FortiManager v7.2
or later.  It takes a specifically formatted Excel file, converts to a JSON file, then uploads it to FortiManager
via an API call.


## Setup
* Download python
    * The best way to download Python is from the official website: https://www.python.org/
    * Python can also be downloaded from terminal: *sudo apt-get install python3.8*
* Clone this repository from Github
    * Option1: clone via GitHub Desktop
    * Option2: clone via git bash using *git clone https://github.com/JoshuaHartling/xlsx_to_json.MK2.git*
* Open this Project in your favorite IDE.  (I recommend Pycharm!)
* Download the following Python modules json either into your project's
virtual environment (recommended) or directly into python.
    * Either download modules using your IDE, or follow these instructions to download modules using
    pip: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
        * json
        * openpyxl
        * requests
        * urllib3
    
## What's Included
* *example.xlsx* is an example Excel file that shows how to format your metavariable data.
    * The first two columns should be your hostname and vdom assignment respectively.  Leave vdom entry
    blank to use global vdom.
        * You can put columns to the left of hostname/vdom columns for notes, but they will not be picked up
        by the script.
    * The first two rows should be metavariable name and its global value respectively.  Leave global entry
    blank to not use a global value.
* *user_settings.py* contains user configuration parameters.
* *main.py* is the main script that should be run to upload your Excel file to FortiManager.

## User Input
There are several parameters that you can set within the *user_settings.py* script,
though the only parameter you always must set is the file_path.

***Excel Parse Settings***
* **file_path:** This variable is the directory path to your Excel file.  It is recommended
to set this as the absolute path.
* **active_sheet:** This is the sheet in your Excel File that holds your metadata.  Set this
if your metavariable data is not on the active (first) sheet of your Excel File.
* **device_list:** is a filter that can be set to only include specific devices.
The filter can be either a string or a list.  Leave it as 'None' to not use it.
* **negate:** is a boolean that when 'True' reverses the filter, turning it into a Blacklist
instead of a whitelist.  All devices not included in the filter will be added to the JSON file.
* **update_defaults:** when 'True' (default) the global values (AKA default values) of each variable
 will be upload to FortiManager.  Set to 'False' to ignore the default values.
 
***FortiManager Upload Settings***
* **adom:** This is the ADOM on FortiManager that you wish to upload metadata to.  If ADOM's have
not been enabled on FortiManager, leave it as "root" as that is the default ADOM.
* **host:** is the IP address or hostname of your FortiManager instance.  Also include your management
port information here if difference from default 443.
* **username:** this is the username of your API administrator account.
* **password:** this is the password of your API administrator account.
* **lock_adom:** set this boolean to True if your FortiManager uses workspace mode.
* **verify_cert:** set this boolean to False if your FortiManager is using an untrusted cert.  
Typically this value will need to be set to False.

***Script Settings***
* **streamline:** set this value to False to pause before uploading metadata for review.
