import os
import subprocess
import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# Config
NGINX_HOST = "192.168.56.10"
NGINX_PORT = 8080
SYSLOG_SERVER = "172.21.0.20"
SYSLOG_PORT = 514
CONTAINER_NAME = "logger"
LOG_FILE = "healthcheck.log"
EMAIL_TO = "usman2003.fb@gmail.com"  # ← Replace with your email
EMAIL_FROM = "monitor@lab.local"
SMTP_HOST = "192.168.56.1"
SMTP_PORT = 2525
TEST_MESSAGE = f"Health test {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def log_status(line):
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line)

def ping_host(ip):
    result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL)
    return result.returncode == 0

def http_check(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def send_syslog():
    try:
        subprocess.run(["logger", "--server", SYSLOG_SERVER, "--port", str(SYSLOG_PORT), TEST_MESSAGE], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_syslog_in_container():
    try:
        logs = subprocess.check_output(["docker", "logs", CONTAINER_NAME], stderr=subprocess.DEVNULL)
        return TEST_MESSAGE in logs.decode()
    except subprocess.CalledProcessError:
        return False

def send_email(subject, body):
    msg = MIMEText(body)
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        print("Email sent.")
    except Exception as e:
        print("Email failed:", e)

def run_healthcheck():
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # PING
    ping_status = "OK" if ping_host(NGINX_HOST) else "FAIL"

    # HTTP
    http_status = "200 OK" if http_check(f"http://{NGINX_HOST}:{NGINX_PORT}") else "FAIL"

    # SYSLOG
    syslog_sent = send_syslog()
    time.sleep(2)
    syslog_status = "RECEIVED" if syslog_sent and check_syslog_in_container() else "FAIL"

    # Log result
    line = f"{timestamp} PING {NGINX_HOST} {ping_status} | HTTP {http_status} | SYSLOG {syslog_status}"
    log_status(line)

    # Email result
    is_all_ok = (ping_status == "OK") and (http_status == "200 OK") and (syslog_status == "RECEIVED")
    email_subject = "✅ Healthcheck PASSED" if is_all_ok else "❌ Healthcheck FAILED"
    send_email(email_subject, line)

if __name__ == "__main__":
    run_healthcheck()
