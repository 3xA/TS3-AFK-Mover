#!/usr/bin/env python3
import pexpect
def extract_between(text, sub1, sub2, nth=1):
	if sub2 not in text.split(sub1, nth)[-1]:
		return None
	return text.split(sub1, nth)[-1].split(sub2, nth)[0]

# SERVER CONFIGURATION
# ----
HOST = 'localhost' #IP, domain or localhost
PORT = '10011' #by default 10011
USERNAME = 'serveradmin'
PASSWORD = '123superpassword456'
SERVERID = '1' #1 by default
DISPLAYNAME = 'AFK Bot' #Shown in chat to all users
IDLETIMELIMIT = 360 #Minutes
AFKCHANNEL = 18 #Channel to move client after IDLETIMELIMIT
CHANBLACKLIST = "['18','19','20']" #Channels not to watch
# ----

if ' ' in DISPLAYNAME:
	DISPLAYNAME = DISPLAYNAME.replace(' ','\s')
if HOST == 'localhost':
	HOST = str('127.0.0.1')
child = pexpect.spawn('telnet ' + HOST + ' ' + PORT)
connStatus = child.after
child.sendline('login ' + USERNAME + ' ' + PASSWORD)
child.expect("msg=ok")
child.sendline("use sid=" + SERVERID)
child.expect("msg=ok")
child.sendline('clientupdate client_nickname=' + DISPLAYNAME)
child.expect("msg=ok")
child.sendline("clientlist -away -times")
child.expect("msg=ok")
clientBlob = str(child.before)
if 'error id=0' in clientBlob:
	cAT_Formatted = ('|' + clientBlob[35:-18] + '|')
	splitUsers = cAT_Formatted.split('|')
	n = 0
	client = [['clid', 'cid', 'client_nickname', 'client_type', 'client_away', 'client_idle_time']]
	IDLETIMELIMIT = IDLETIMELIMIT * 60 * 1000
	for user in splitUsers:
		if n == 0:
			n = n + 1
		else:
			if 'client_type=0' in user:
				clid = extract_between(user, 'clid=', ' ')
				cid = extract_between(user, 'cid=', ' ')
				client_nickname = extract_between(user, 'client_nickname=', ' ')
				client_type = extract_between(user, 'client_type=', ' ')
				client_away = extract_between(user, 'client_away=', ' ')
				client_idle_time = extract_between(user, 'client_idle_time=', ' ')
				if clid == None:
					n = n + 1
				else:
					client.append([clid, cid, client_nickname, client_type, client_away, client_idle_time])
					n = n + 1
	for x in client:
		xClid = x[0]
		xChan = x[1]
		xNick = x[2]
		xAway = x[4]
		xITime = x[5]
		if xChan.isdigit():
			xChan = int(xChan)
			if str(xChan) not in CHANBLACKLIST:
				if xITime.isdigit():
					if int(xITime) >= IDLETIMELIMIT:
						if xClid.isdigit():
							child.sendline('clientmove clid=' + str(xClid) + ' cid=' + str(AFKCHANNEL))
	child.sendline('logout')
	child.expect('msg=ok')
	child.sendline('quit')