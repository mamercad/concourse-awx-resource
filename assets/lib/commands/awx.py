#!/usr/bin/env python3

import logging
import os
import requests
import time


class AWX:
    def __init__(self, args, sleep=10):
        logging.basicConfig(level=logging.INFO)
        self.sleep = sleep
        if not self._validate_args(args):
            raise Exception("Invalid arguments")
        self.source = args["source"]
        self.params = args["params"]
        self.endpoint = self.source["awx"]["endpoint"]
        logging.info("AWX endpoint is {0}".format(self.endpoint))
        self.headers = {
            "Content-type": "application/json",
            "Authorization": self.source["awx"]["auth"],
        }
        self.type = self.params["awx"]["type"]
        self.id = self.params["awx"]["id"]
        if self.params["awx"].get("debug", False):
            logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Logging is set to {0}".format(logging.getLogger()))
        logging.info(
            "params.awx.debug is set to {0}".format(self.params["awx"]["debug"])
        )
        logging.info("Finished initialization, ready to go")

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
        if args["params"]["awx"].get("type", None) is None:
            return False
        if args["params"]["awx"].get("id", None) is None:
            return False
        logging.info("Argument validation passed, sweet")
        return True

    def ping(self):
        url = "{0}/api/v2/ping/".format(self.endpoint)
        r = requests.get(url=url)
        if r.status_code != 200:
            raise Exception("Could not hit AWX")
        logging.debug("{0}: {1}".format(url, str(r.status_code)))
        logging.info("Successfully talked to AWX, cool")

    def launch(self):
        # launch the job template or workflow job template
        url = "{0}/api/v2/{1}/{2}/launch/".format(self.endpoint, self.type, self.id)
        jt_launch = requests.post(url=url, headers=self.headers)
        if jt_launch.status_code != 201:
            raise Exception(
                "Could not launch job template, got a {0} hitting {1}".format(
                    jt_launch.status_code, url
                )
            )
        else:
            logging.info("Successfully launched {0}".format(url))
        logging.debug("{0}: {1}".format(url, str(jt_launch.status_code)))
        jt_response = jt_launch.json()

        # follow the job
        if jt_response.get("url", None) is None:
            raise Exception("Job url not found, check AWX for hints at {0}".format(url))

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
                logging.debug(
                    "The job isn't done, sleeping for {0}s and checking again".format(
                        self.sleep
                    )
                )
                time.sleep(self.sleep)

        logging.debug(str(job_response))
        logging.info("The job finished, sweet")
        return job_response


def main():
    args = {
        "source": {
            "awx": {
                "endpoint": os.environ.get("TOWER_HOST"),
                "auth": "Bearer {0}".format(os.environ.get("TOWER_OAUTH_TOKEN")),
            },
        },
        "params": {"awx": {"job_templates": os.environ.get("TOWER_JOB_TEMPLATES")}},
    }
    a = AWX(args)
    a.ping()
    j = a.launch()


if __name__ == "__main__":
    main()
