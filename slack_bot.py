import os
import time
import re
from slackclient import SlackClient
import psycopg2
import subprocess
import unicodedata
import thread
import os, os.path
import glob
import shutil
host = "131.155.11.15"
user = "postgres"
password ="tweeid70"
dbname = "uni"
port = "5432"

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
key_list = ['u8Tl6IP',
'FFP2DXZ',
'qldooP3',
'KKmsc9m',
'5DjpLvw',
'uN9u4jH',
'9iAQPQS',
'cjkFPmh',
'b7OM0rj',
'PfPomKo',
'jRXXkh6',
'5HLR6vc',
'RWOqjwd',
'G5UipI4',
'KgfeEJH',
'CgMPTWi',
'lSgWGiz',
'gQinFyR',
'w5LSJgh',
'9oaVnzO',
'xYz0JqU',
'yL096A7',
'2NiLxhd',
'cmL4MhR',
'M4muDfX',
'OZvZgO5',
'Xo2q3IR',
'ycs2dXl',
'EGDw8xn',
'G5UipI4',
'xYOthws',
'gcazYli',
'pQjlKIP',
'uC2a7HX']

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            print("entering if condition")
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def submission(question):
    question = question.split(' ')


def MyThreadResponse(id,submited,channel,default_response):
    while(submited and check_execution(id)==False):
        time.sleep(5)
    response = "error"
    res = 0
    q1=q2=""
    try:
        #change the credentials for database
        conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port+"")
        cur = conn.cursor()
        #main_function
        #time_count function
        cur.execute("UPDATE submissions SET status=4 WHERE param1='"+id+"'")
        conn.commit()

        cur.execute("SELECT results_q1, score FROM submissions WHERE param1='"+id+"' ORDER BY score ASC LIMIT 10")
        res = cur.fetchone()
        cur.execute("SELECT stime, score FROM submissions WHERE status=4 ORDER BY score ASC LIMIT 10")
        #leader_board sort by time and pick top10(sql)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        q1=rows
    except Exception, e:
        print(e)
    response = "Your result is " + str(res[0].split("\n")[0]) +"\n TOP10: \n"
    i = 1
    for elem in q1:
        response = response + str(i) + " "+elem[0].strftime("%Y-%m-%d %H:%M:%S")+ " " + str(elem[1]) + "\n"
        i = i + 1
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
    pass


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    #print("Received " + message_text)
    submission(message_text)
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def check(text):
    hack_array = ['drop', 'delete', 'update', 'select', 'insert']
    for i in hack_array:
        if text.find(i) > -1:
            return False
    return True


def java_call(student_id):
    subprocess.call('timeout 1h java #arguments# 2ID70_' + student_id, shell=True)


def execute_command(url, student_id):
    print('bash 2ID70_' + student_id + '/load.sh')
    shutil.rmtree('2ID70_' + student_id, ignore_errors=True)
    subprocess.call('git clone ' + url[1:len(url)-1], shell=True)
    subprocess.call('timeout 1h bash 2ID70_' + student_id + '/load.sh &>results_q1', shell=True)

def check_execution(id):
    try:
        #change the credentials for database
        conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port+"")
        cur = conn.cursor()
        #main_function
        #time_count function
        cur.execute("SELECT executed FROM submissions WHERE param1='"+id+"'")
        #leader_board sort by time and pick top10(sql)
        rows = cur.fetchone()
        cur.close()
        conn.close()
        return rows[0]
    except Exception, e:
        return False


def postgres(id, url, time='1'):
    try:
        #change the credentials for database
        conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port+"")
        cur = conn.cursor()
        #main_function
        #time_count function
        cur.execute("UPDATE submissions SET param2 ='"+url+"', command='1', executed=FALSE, status=1, results_load='', results_q1='', score=1000, stime='now()' WHERE param1='"+id+"'; INSERT INTO submissions (param1,param2,command,executed,status,stime) SELECT '"+id+"','"+url+"','1',FALSE,1,'now()' WHERE NOT EXISTS(SELECT 1 FROM submissions WHERE param1='"+id+"');")
        conn.commit()
        cur.execute("SELECT * FROM submissions WHERE param1='"+id+"'")
        #leader_board sort by time and pick top10(sql)
        rows = cur.fetchone()
        #print(rows)
        cur.close()
        conn.close()
        return True
    except Exception, e:
        print("I am unable to connect to the database"+str(e))
        return False

def pick_student():
    try:
        #change the credentials for database
        conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port+"")
        cur = conn.cursor()
        #main_function
        #time_count function
        cur.execute("SELECT * FROM SUBMISSIONS WHERE STATUS=1 ORDER BY STIME LIMIT 1")
        #leader_board sort by time and pick top10(sql)
        rows = cur.fetchone()
        if rows != None:
            cur.execute('UPDATE SUBMISSIONS SET STATUS = 2 WHERE PARAM1' + rows[0])
            cur.commit()
        cur.close()
        conn.close()
        return rows[0], rows[1]
    except Exception, e:
        print("I am unable to connect to the database"+str(e))
        return False


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = ""
    # This is where you start to implement more commands!
    argument = command.split(' ')
    submited = False
    if len(argument) != 2:
        response = "Check ID, url and spaces between them"
    else:
        #response = ""
        student_id = argument[0]
        student_id = unicodedata.normalize('NFKD', student_id).encode('ascii', 'ignore')
        if len(argument[0]) > 8 and check(argument[0]) == False and argument[0] in key_list:
            response = "Check the correctness of ID"
        url = argument[1]
        url = unicodedata.normalize('NFKD', url).encode('ascii', 'ignore')
        url = url.replace("<","").replace(">","")
        if len(url) == 0 and check(url) == False:
             response += "Check url"
        # else:
        #     "Everything is fine"
        if response == "":
           response = "good job, "+argument[0]
           if postgres(argument[0], url):
               submited=True
               #pick_student()
               #execute_command(url, student_id)
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
    if(submited):
        thread.start_new_thread(MyThreadResponse, (argument[0],submited,channel,default_response,))

if __name__ == "__main__":
    if slack_client.    rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        print("my id is "+starterbot_id)
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

print("Starter Bot connected and running!")