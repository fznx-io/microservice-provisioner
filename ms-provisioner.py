#!/usr/bin/env python3
import requests
import sys

# Bitbucket Configuration
bb_url          = 'https://bitbucket.somecompany.com'
bb_auth_user    = 'bitbucket_auth_user'           # BITBUCKET_AUTH_USER
bb_auth_pass    = 'bitbucket_auth_password'       # BITBUCKET_AUTH_PASSWORD
bb_project      = 'MS'

# Jenkins Configuration
jenkins_url         = 'https://jenkins.somecompany.com'
jenkins_auth_user   = 'jenkins_auth_user'         # JENKINS_AUTH_USER
jenkins_auth_pass   = 'jenkins_auth_password'     # JENKINS_AUTH_PASSWORD
