###
# Functions
##
def getCurrentIp():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        ip = s.getsockname()[0]
        s.close()
        return ip


def getLastIp():
	last_ip = open("/home/chingiz/rpi/labo2/last_ip", "r")
	last_ip = last_ip.read()
	return last_ip

def saveLastIp():
	last_ip = open("/home/chingiz/rpi/labo2/last_ip", "w")
	last_ip.write(getCurrentIp())
	last_ip.close

def postMessageToSlack():
	from slackclient import SlackClient
	token = "xoxp-153472905298-152766488672-153473234338-976f66418c71f82104c5a028305752ba"
	sc = SlackClient(token)
	resp = sc.api_call(
        	"chat.postMessage",
        	as_user="true",
        	channel="@chinjka",
        	text=getCurrentIp()
	)
	print("IP address has been posted on Slack")


#Import path to check if last_ip file already exists
import os.path

#Check if last_ap file exists
last_ip = os.path.isfile("/home/chingiz/rpi/labo2/last_ip")

if last_ip:
	#if file exists, read the previous IP, get the current IP and compare them
	current_ip = getCurrentIp()
	last_ip = getLastIp()
	if current_ip == last_ip:
		#If they match, no farthe action required
		print("IP unchanged. No action required")
	else:
		#If they differ, send the new IP to Slack
		postMessageToSlack()	

else:
	#If the file doesnt exists, send current IP to Slack
	postMessageToSlack()
	
#Create/Update the file with last IP address for future use
saveLastIp()
