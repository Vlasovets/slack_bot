import os
import time
import re
import psycopg2
import subprocess
import unicodedata
import thread
import os, os.path
import glob
import shutil
from git import Repo



host = "131.155.11.15"
user = "postgres"
password ="tweeid70"
dbname = "uni"
port = "5432"


def get_duration_from_file(filename):
    f_read = open(filename, "r")
    last_line = f_read.readlines()[0]
    print(last_line)
    last_line_1 = last_line.split(" sec")[0]
    print(last_line_1)
    last_line_1 = last_line_1.split("Total =")
    print(last_line_1)
    f_read.close()
    try:
        return int(filter(str.isdigit, last_line_1[-1]))
    except:
        return 1000
#CLASSPATH=".:/usr/share/java/postgresql-jdbc4.jar"

def execute_command(url):
            if not os.path.exists("code"):
                 os.makedirs("code")
            else:
                 shutil.rmtree("code", ignore_errors=True)
            subprocess.call("psql -d uni -c \"SELECT drop_tables('vmuser');\"", shell=True)
            Repo.clone_from(url, "code")
            os.chdir("code")
            return_code = subprocess.call('timeout 1h bash load.sh > ./results_q1 2>&1', shell=True)
            if return_code>0:
                return 1000
            return_code = subprocess.call('timeout 5m psql -d uni -f q2Create.sql', shell=True)
            if return_code>0:
                return 1000
            os.chdir("..")
            return_code = subprocess.call('timeout  java AutomaticTestingQ2', shell=True)
            if return_code>0:
                return 1000
            return 0


def check_submissions():
    try:
        #change the credentials for database
        conn = psycopg2.connect(
            "dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "' port=" + port)
        cur = conn.cursor()
        #main_function
        #time_count function
        cur.execute("SELECT * FROM submissions WHERE status=1 ORDER BY stime ASC")
        #leader_board sort by time and pick top10(sql)
        rows = cur.fetchone()
        if(rows):
            result = (rows[0],rows[1])
            cur.execute("UPDATE submissions SET status = 2 WHERE param1='" + rows[0]+"';")
            conn.commit()
        else:
            result = None
        cur.close()
        conn.close()
        return result
    except Exception, e:
        print(e)
        return False


def get_file_content(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content


def save_results(id, res1, res2, score):
    try:
        #change the credentials for database
        conn = psycopg2.connect(
            "dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "' port=" + port + "")
        cur = conn.cursor()
        #main_function
        #time_count function
        cur.execute("UPDATE submissions SET status=3, executed=true, results_load='"+str(res1)+"',results_q1='"+str(res2)+"', score="+str(score)+" WHERE param1='"+str(id)+"'")
        #leader_board sort by time and pick top10(sql)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception, e:
        print(e)
        return False


def main():
    while(True):
        check_result = check_submissions()
        if(check_result != None and check_result!=False):
            current_id = check_result[0]
            score = execute_command(check_result[1])
            file_load = "error, Total = 1000 sec"
            file_q2 = "error, Total = 1000 sec"
            if score == 0:
                file_load = get_file_content("code/results_q1")
                file_q2 = get_file_content("code/resultsGroup.txt")
                score = get_duration_from_file("code/resultsGroup.txt")
            else:
                score = 1000
            save_results(current_id,file_load,file_q2,score)
        time.sleep(5)


if __name__ == '__main__':
    main()