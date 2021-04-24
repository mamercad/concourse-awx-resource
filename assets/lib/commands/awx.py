#!/usr/bin/env python3

import logging
import os
import json
from pprint import pprint
import requests
import time


class AWX:

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, args, sleep=10):
        self.sleep = sleep
        if not self._validate_args(args):
            raise Exception("Invalid arguments")
        self.source = args["source"]
        self.params = args["params"]
        self.endpoint = self.source["awx"]["endpoint"]
        self.headers = {
            "Content-type": "application/json",
            "Authorization": self.source["awx"]["auth"],
        }
        self.workflow = self.params["awx"]["workflow"]

    def _validate_args(self, args):
        if args.get("source", None) is None:
            return False
        if args["source"].get("awx", None) is None:
            return False
        if args["source"]["awx"].get("endpoint", None) is None:
            return False
        if args["source"]["awx"].get("auth", None) is None:
            return False
        if args.get("params", None) is None:
            return False
        if args["params"].get("awx", None) is None:
            return False
        if args["params"]["awx"].get("workflow", None) is None:
            return False
        return True

    def ping(self):
        url = "{0}/api/v2/ping/".format(self.endpoint)
        r = requests.get(url=url)
        if r.status_code != 200:
            raise Exception("Could not hit AWX")
        logging.debug("{0}: {1}".format(url, str(r.status_code)))

    def launch_job_template(self):
        # launch the job template
        url = "{0}/api/v2/job_templates/{1}/launch/".format(
            self.endpoint, self.workflow
        )
        jt_launch = requests.post(url=url, headers=self.headers)
        if jt_launch.status_code != 201:
            raise Exception("Could not launch workflow")
        logging.debug("{0}: {1}".format(url, str(jt_launch.status_code)))
        jt_response = jt_launch.json()

        # follow the job
        if jt_response.get("url", None) is None:
            raise Exception("Job url not found")

        done = False
        while not done:
            url = "{0}{1}".format(self.endpoint, jt_response["url"])
            job_url_get = requests.get(url=url, headers=self.headers)
            if job_url_get.status_code != 200:
                raise Exception("Could not query job")
            logging.debug("{0}: {1}".format(url, str(job_url_get.status_code)))
            job_response = job_url_get.json()
            finished = job_response.get("finished", False)
            if finished is not None:
                done = True
            else:
                logging.debug("Not done, sleeping for {0}s".format(self.sleep))
                time.sleep(self.sleep)

        logging.debug(str(job_response))

        return job_response


def main():
    args = {
        "source": {
            "awx": {
                "endpoint": os.environ.get("TOWER_HOST"),
                "auth": "Bearer {0}".format(os.environ.get("TOWER_OAUTH_TOKEN")),
            },
        },
        "params": {"awx": {"workflow": 9}},
    }
    a = AWX(args)
    a.ping()
    j = a.launch_job_template()
    pprint(j)


if __name__ == "__main__":
    main()
