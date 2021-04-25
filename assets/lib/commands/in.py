#!/usr/bin/env python

import json
import sys


def main():
    _stdin = "".join(sys.stdin.readlines())
    _in = json.loads(_stdin)

    _out = {
        "version": {},
        "metadata": [],
    }

    print(json.dumps(_out))


if __name__ == "__main__":
    main()
