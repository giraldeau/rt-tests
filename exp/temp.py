#!/usr/bin/env python2

from fabric.api import task, run, env, sudo, local, cd, settings, execute
from fabric.operations import get
from fabric.contrib.files import append
from StringIO import StringIO
import time
import sys
import os
import re

import pprint
import numpy as np
import matplotlib.pyplot as plt

"""
TODO
- run all experiments
- generate all charts
- three types of comparison: machine

"""

# use root by default
env.user = "root"
env.password = "testtest"

data_ext = ".data"
results_dir = "results"

cyclictest_defaults = {
    "threads": 1,
    "mlockall": None,
    "distance": 0,
    "duration": 1,
    "histogram": 300,
    "interval": 1000,
    "affinity": 3,
    "notrace": None,
    "quiet": None,
    "priority": 99,
    "policy": "fifo",
}

experiments = {
    "isolcpu": {
        "cyclictest": {
            "affinity": 3,
        },
    },
    "no_isolcpu": {
        "cyclictest": {
            "affinity": 0,
        },
    },
}

class Setup(object):
    def before(self):
        pass
    def after(self):
        pass

stress = {
    "hdd": { 
        "cmd": "stress --io 8 --hdd-bytes 4096B --hdd 8",
    },
    "mem": {
        "cmd": "stress --vm 8 --vm-bytes 128M",
    },
    "cpu": {
        "cmd": "stress --cpu 8",
    },
    "mix": {
        "cmd": "stress --cpu 8 --io 4 --vm 2 --vm-bytes 128M",
    },
#    "net": {
#        "cmd": "netperf -H localhost -l10",
#    },
}

def get_command(name, opts):
    cmd = [name]
    for opt, val in opts.items():
        cmd.append("--" + opt)
        if val:
            cmd.append(str(val))
    return " ".join(cmd)


def run_experiment(opts):
    cmd = get_command("cyclictest",  opts)
    print(cmd)
    buf = StringIO()
    run(cmd + " > /tmp/hist.data 2> /dev/null")

    # FIXME: there is a bug in the image, the search path for sftp-server is wrong
    run("mkdir -p /usr/lib/openssh/")
    run("test -e /usr/libexec/ || ln -s /usr/libexec/sftp-server /usr/libexec/")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    get("/tmp/hist.data", os.path.join(results_dir, opts["sample_file"]))

@task
def cyclictest(experiment="basic"):

    if not experiment in experiments:
        raise Exception("experiment not found " + repr(experiments.keys()))

    exp = experiments[experiment]
    exp["name"] = experiment
    
    params = exp.get("cyclictest", {})
    p = dict_product(params)
    for item in p:
        # override parameters
        opts = cyclictest_defaults
        sample_file = experiment
        for k, v in item.items():
            opts[k] = v
            sample_file += "-" + k + str(v)
        sample_file += data_ext
        opts["sample_file"] = sample_file
        run_experiment(opts)
    sys.exit(0)

def normalize_serie(serie):
    total = sum(serie)

    # avoid division by zero
    if total == 0:
        total = 1
    norm = []
    for v in serie:
        norm.append(float(v) / total)
    return norm

def process_hist(data_path):
    pattern = re.compile("([0-9]+)\s+([0-9]+\s+)*")
    data = {} # [bucket][cpu]
    with open(data_path, "r") as xin:
        for line in xin.readlines():
            if pattern.match(line):
                items = [x for x in re.split("\s*", line) if len(x) > 0]
                bucket = int(items[0])
                data[bucket] = []
                for i, item in enumerate(items[1:]):
                    data[bucket].append(int(item))

    series = len(data[data.keys()[0]])
    # transpose the data
    y = []
    for serie in range(series):
        samples = []
        for key in data.keys():
            samples.append(data[key][serie])
        norm = normalize_serie(samples)
        y.append(norm)
    x = data.keys()

    return { "x": x, "series": y }

color_list = (
    '#8d0000',
    '#00007f',
    '#ff7000',
    '#00c6ff',
    '#b7ff46',
)

def make_figure(data, exp):
    plt.figure()
    # axes does not applies to bar colors
    #plt.rc('axes', prop_cycle=(cycler('color', color_list)))
    for i, serie in enumerate(data["series"]):
        plt.plot(data["x"], serie,
            color=color_list[i % len(color_list)])
    plt.grid(True)
    title = exp.get("plot", {}).get("title", exp["name"])
    plt.title(title)
    plt.yscale('log')
    plt.savefig(os.path.join(data["path"], data["base"] + ".png"))
    plt.close()

@task
def hist():
    data[]
    for base, dirnames, fnames in os.walk("results/"):
        for fname in fnames:
            if not fname.endswith(data_ext):
                continue
            exp_name = fname.split("-")[0]
            data_path = os.path.join(base, fname)
            data = process_hist(data_path)


