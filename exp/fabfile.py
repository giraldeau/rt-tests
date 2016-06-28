#!/usr/bin/env python

from fabric.api import task, run, local
from fabric.operations import put, get

@task
def push():
    put("go-rttest", "~/", mode=0755)

@task
def exp():
    run("~/go-rttest experiments")

@task
def fetch():
    local("mkdir -p results/")
    get("/tmp/go-rttest/*", "results/%(host)s/%(basename)s")
