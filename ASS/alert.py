import requests
import json
def alert():
	header = {

	"Content-Type": "application/json; charset=utf-8",
	"Authorization": "Basic MzlhOGJhY2QtODg4Zi00OTI1LTk2OGMtZDIzNjVhMGQyYmVh"}
	payload = {
	"app_id": "20720743-d58e-4c65-a12e-d5f791a5bea9",
           "included_segments": ["All"],
           "contents": {"en": "Alert! Patient is outside restricted area"}}

	req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
	print(req.reason, req.status_code)
	return (req.reason, req.status_code)
	# sending notification include rest api key
