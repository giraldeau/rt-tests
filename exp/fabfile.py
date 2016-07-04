#!/usr/bin/env python

from fabric.api import task, run, local, parallel
from fabric.operations import put, get

@task
def push():
    put("go-rttest", "~/", mode=0755)

@task
@parallel
def exp():
    run("~/go-rttest experiments --duration 600")

@task
def fetch():
    local("mkdir -p results/")
    get("/tmp/go-rttest/*", "results/%(host)s/%(basename)s")

@task
def clean():
    run("rm -rf /tmp/go-rttest")
