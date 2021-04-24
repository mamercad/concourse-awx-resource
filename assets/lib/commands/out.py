#!/usr/bin/env python

import json
import sys
from awx import AWX
from pprint import pprint

_stdin = "".join(sys.stdin.readlines())
_in = json.loads(_stdin)

awx = AWX(_in)
job_results = awx.launch_job_template()

metadata = []
for k in sorted(job_results.keys()):
    metadata.append({"name": k, "value": json.dumps(job_results[k])})

_out = {
    "version": {},
    "metadata": metadata,
}

print(json.dumps(_out))
