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

# Bitbucket API Endpoints
bb_repo_url             = bb_url + '/rest/api/1.0/projects/' + bb_project + '/repos'
bb_repo_hook_url        = bb_url + '/rest/api/1.0/projects/' + bb_project + '/repos/{repo}/settings/hooks/com.nerdwin15.stash-stash-webhook-jenkins%3Ajenkins-postreceive-webhook'
bb_branch_perm_url      = bb_url + '/branch-permissions/2.0/projects/' + bb_project + '/repos/{repo}/restrictions'
bb_merge_check_url      = bb_url + '/rest/split-diff/1.0/projects/' + bb_project + '/repos/{repo}/settings/general'
bb_merge_strategy_url   = bb_url + '/rest/default-reviewers/1.0/projects/' + bb_project + '/repos/{repo}/condition'
