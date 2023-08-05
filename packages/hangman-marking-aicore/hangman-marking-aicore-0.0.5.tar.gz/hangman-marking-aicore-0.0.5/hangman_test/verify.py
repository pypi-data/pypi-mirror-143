import os
import requests
import json

user_id = os.environ['USER_ID']
token = os.environ['API_TOKEN']
url_api = 'https://reczg13drk.execute-api.eu-west-1.amazonaws.com/prod/user/project/task/verify'
headers = {'x-api-key': f"{token}"}

def get_errors_fails(report_path: str):
    with open(report_path, 'r') as f:
        report = f.read()

    list_fails = report.split('======================================================================')

    if len(list_fails) > 1:
        list_fails = list_fails[1:]

    fail_error = [fail.split('----------------------------------------------------------------------')[0]
                for fail in list_fails]

    errors = [e.split('ERROR: ')[1].split(' (')[0] for e in fail_error if e.startswith('\nERROR')]
    fails = [f.split('FAIL: ')[1].split(' (')[0] for f in fail_error if f.startswith('\nFAIL')]
    return errors, fails

def mark_complete(task_id: str, message=None):
    data = {
            'task_id': task_id,
            'user_id': user_id,
            }
    if message:
        data['message'] = message

    r = requests.post(url_api, headers=headers, data=json.dumps(data))
    assert r.status_code == 200

def mark_incomplete(task_id: str, message=None):
    data = {
            'task_id': task_id,
            'user_id': user_id,
            'complete': False
            }
    if message:
        data['message'] = message

    r = requests.post(url_api, headers=headers, data=json.dumps(data))

    assert r.status_code == 200