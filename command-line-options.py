"""
Runtime
Web UI
Master & Worker
Stats
Tag
Log
Others

-f: file name
-u: users
-r: spawn rate
-t: time
--csv: path to csv where the results will be saved
--csv-full-history:
-L: Log level. Valid values are: DEBUG/INFO/WARNING/ERROR/CRITICAL
--logfile: File where logs will be stored
--html: html report file name

locust -f command-line-options.py -u 1 -r 1 -t 10s --headless --print-stats --csv results/sample-results.csv --csv-full-history --host=https://www.google.com
locust -f command-line-options.py -u 1 -r 1 -t 10s --headless --print-stats --csv results/sample-results.csv --csv-full-history --host=https://www.google.com -L DEBUG --logfile results/mylog.log --html run_report
"""

from locust import HttpUser, task, constant, between, constant_pacing


class MyUser(HttpUser):
    wait_time = constant(1)

    @task
    def launch(self):
        response = self.client.get("/mail")
        print(response.status_code)
