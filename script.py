import json
import requests
from requests.structures import CaseInsensitiveDict


def yes_or_no_question(question, default_no=True):
    choices = ' [y/N]: ' if default_no else ' [Y/n]: '
    default_answer = 'n' if default_no else 'y'
    reply = str(input(question + choices)).lower().strip() or default_answer
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False if default_no else True



api = "http://cm.jsu.ac.ir/api/v1";

with open('config.json') as configs_raw:
    configs_json = json.load(configs_raw);


configs_json = configs_json['credentials']


#sends verification code to your phone
login_by_phone_json = requests.post(
    f"{api}/login_by_phone",
    params={"phone_number":configs_json["phone_number"]}
).json()


#obtain session id and save for later usage
session_id = login_by_phone_json['session_id']


#self explanatory!
verification_code = input("Enter verification code sent to you: ")


#send verification code and server returns token
verification_code_res = requests.post(
    f"{api}/login_send_verification_code",
    params={"session_id": session_id, "verification_code": verification_code}
).json()


#write debugging information to file with ut8 encoding
with open('debug.json', 'w', encoding='utf8') as debug_output:
    json.dump(verification_code_res, debug_output, indent=4, ensure_ascii=False);



token = verification_code_res['token']


#prepare headers specially token
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = f"Bearer {token}"
headers["Content-Type"] = "application/json"


#send token and password and server returns scores
scores = requests.post(
    f"{api}/get_scores_by_password",
    headers=headers,
    params={"password": configs_json['golestan_password']}
).json()



#write json to file with ut8 encoding
with open('scores.json', 'w', encoding='utf8') as scores_output:
    json.dump(scores, scores_output, indent=4, ensure_ascii=False);



#-----------------------------------------------------------------------------------------------------

if yes_or_no_question("Would you like to logout?"):
    logout_res = requests.post(
        f"{api}/logout",
        headers=headers,
    )
    if logout_res.status_code == 200:
        print("Logout Successful")
    
