import subprocess
import json
from application.constants import *
from user_settings import streamline


# run script to generate JSON file
print("Generating MetaVariables JSON file...")
try:
    subprocess.run(["python", f"application/{GENERATE}"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running {GENERATE}: {e}")
    quit(10)
print()

# pause if streamline is False
if streamline is False:
    with open(OUTPUT, "r") as jsonfile:
        jsondata = json.load(jsonfile)
        print(json.dumps(jsondata, indent=2))
        print()
    input("Press enter to Upload MetaVariables...")
    print()

# run script to upload JSON file
print("Uploading MetaVariables to FortiManager")
try:
    subprocess.run(["python", f"application/{UPLOAD}"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running {UPLOAD}: {e}")
