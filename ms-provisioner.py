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

def provision_bitbucket_repo(repo_name):
    """Create Bitbucket repository with hooks and branch permissions"""

    # Create repository
    payload = {'name': repo_name}
    response = requests.post(bb_repo_url, json=payload, auth=(bb_auth_user, bb_auth_pass))
    print(f'Repository created: {response.status_code}')

    # Enable Jenkins webhook
    hook_url = bb_repo_hook_url.format(repo=repo_name)
    hook_payload = {
        'jenkinsBase': jenkins_url,
        'gitRepoUrl': '',
        'ignoreCommitters': '',
        'ignoreBranches': ''
    }
    response = requests.put(hook_url, json=hook_payload, auth=(bb_auth_user, bb_auth_pass))
    response = requests.put(hook_url + '/enabled', auth=(bb_auth_user, bb_auth_pass))
    print(f'Jenkins webhook enabled: {response.status_code}')

    # Set branch permissions for develop
    perm_url = bb_branch_perm_url.format(repo=repo_name)
    perm_payload = {'type': 'no-deletes', 'matcher': {'id': 'refs/heads/develop', 'type': {'id': 'BRANCH'}}}
    response = requests.post(perm_url, json=perm_payload, auth=(bb_auth_user, bb_auth_pass))
    print(f'Develop branch protection: {response.status_code}')

    # Set branch permissions for staging
    perm_payload = {'type': 'no-deletes', 'matcher': {'id': 'refs/heads/staging', 'type': {'id': 'BRANCH'}}}
    response = requests.post(perm_url, json=perm_payload, auth=(bb_auth_user, bb_auth_pass))
    print(f'Staging branch protection: {response.status_code}')

    # Set branch permissions for master
    perm_payload = {'type': 'no-deletes', 'matcher': {'id': 'refs/heads/master', 'type': {'id': 'BRANCH'}}}
    response = requests.post(perm_url, json=perm_payload, auth=(bb_auth_user, bb_auth_pass))
    print(f'Master branch protection: {response.status_code}')

    # Enable merge checks
    merge_url = bb_merge_check_url.format(repo=repo_name)
    merge_payload = {'mergeConfig': {'type': 'REPOSITORY', 'strategies': [{'enabled': True, 'flag': 'MERGE_COMMIT', 'id': 'merge-commit'}]}}
    response = requests.post(merge_url, json=merge_payload, auth=(bb_auth_user, bb_auth_pass))
    print(f'Merge checks enabled: {response.status_code}')

    # Set merge strategy
    strategy_url = bb_merge_strategy_url.format(repo=repo_name)
    strategy_payload = {'mergeConfig': {'defaultStrategy': {'id': 'merge-commit'}}}
    response = requests.post(strategy_url, json=strategy_payload, auth=(bb_auth_user, bb_auth_pass))
    print(f'Merge strategy set: {response.status_code}')


def provision_jenkins_jobs(repo_name):
    """Create Jenkins pipeline jobs"""

    jenkins_job_path = 'job/microservices-pipelines'
    jenkins_job_url = f'{jenkins_url}/{jenkins_job_path}/createItem?name={repo_name}'

    jenkins_payload = '''<?xml version='1.1' encoding='UTF-8'?>
<org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin="workflow-multibranch@2.21">
  <actions/>
  <properties/>
  <folderViews class="jenkins.branch.MultiBranchProjectViewHolder" plugin="branch-api@2.5.4">
    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
  </folderViews>
</org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>'''

    headers = {'Content-Type': 'application/xml'}
    response = requests.post(jenkins_job_url, data=jenkins_payload, headers=headers, auth=(jenkins_auth_user, jenkins_auth_pass))
    print(f'Jenkins pipeline created: {response.status_code}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ms-provisioner.py <microservice-name>')
        sys.exit(1)

    repo_name = sys.argv[1]
    print(f'Provisioning microservice: {repo_name}')

    provision_bitbucket_repo(repo_name)
    provision_jenkins_jobs(repo_name)

    print(f'Provisioning complete for {repo_name}')
