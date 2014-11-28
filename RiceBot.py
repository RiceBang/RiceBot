import socket
import random

server = "irc.rizon.net"
channel = raw_input("Channel? \r\n")
botnick = raw_input("Botnick? \r\n")
chanpass = raw_input("Channel password? \r\n")

readers = []
queue = []

def ping():
	ircsock.send("PONG :pingis\r\n")

def joinchan(chan):
	ircsock.send("JOIN "+ chan + " " + chanpass +"\r\n")

def rand(a,b):
	return random.randint(a,b)

def commands(nick,channel,message):
	if ".help" in message.lower() and not "bot" in message.lower():
		ircsock.send("PRIVMSG %s :Commands: .help, .xkcd, .cad \r\n" % channel)
	elif "love" in message.lower() and not "hate" in message.lower() and botnick.lower() in message.lower():
		nick=ircmsg.split('!')[0][1:]
		ircsock.send("PRIVMSG %s :I love you too %s! \r\n" % (channel,nick))
	elif ".xkcd" in message.lower() and not botnick in message.lower():
		comnum = rand(1,1334)
		ircsock.send("PRIVMSG %s :http://xkcd.com/%s/ \r\n" % (channel,comnum))
	elif ".cad" in message.lower() and not botnick in message.lower():
		comnum = rand(1,3474)
		ircsock.send("PRIVMSG %s :http://explosm.net/comics/%s/ \r\n" % (channel,comnum))

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send("NICK %s \r\n" % (botnick))
ircsock.send("USER %s %s %s :RiceBang\r\n" % (botnick,botnick,botnick))

joinchan(channel)

while True:
	ircmsg = ircsock.recv(2048)
	ircmsg = ircmsg.strip('\n\r')

	if ircmsg.find("PING :") != -1:
		ping()

	if "JOIN" in ircmsg and not botnick in ircmsg:
		nick=ircmsg.split('!')[0][1:]
		ircsock.send("PRIVMSG %s :Welcome to %s, %s! Type '.add' to add your name to the queue and '.queue' to view the queue. \r\n" % (channel,channel,nick))

	if ircmsg.find(' PRIVMSG ')!=-1:
		nick=ircmsg.split('!')[0][1:]
		channel=ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
		commands(nick,channel,ircmsg)
