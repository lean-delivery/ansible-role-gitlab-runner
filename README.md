gitlab-runner role
=========

[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-gitlab-runner/master/LICENSE)
[![Build Status](https://travis-ci.org/lean-delivery/ansible-role-gitlab-runner.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-gitlab-runner)
[![Build Status](https://gitlab.com/lean-delivery/ansible-role-gitlab-runner/badges/master/build.svg)](https://gitlab.com/lean-delivery/ansible-role-gitlab-runner)
[![Galaxy](https://img.shields.io/badge/galaxy-lean__delivery.gitlab__runner-blue.svg)](https://galaxy.ansible.com/lean_delivery/gitlab_runner)
![Ansible](https://img.shields.io/ansible/role/d/29089.svg)
![Ansible](https://img.shields.io/badge/dynamic/json.svg?label=min_ansible_version&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F29089%2F&query=$.min_ansible_version)

## Summary

This Ansible role has the following features:

 - Install gitlab-runner

Requirements
------------

 - Version of the ansible for installation: 2.5
 - **Supported OS**:  
   - EL
     - 7
   - Ubuntu
     - 18.04

## Role Variables

- required
  - `gitlab_version`  
  Specific version of Gitlab-Runner. Default value is `10.5`.
  - `gitlab_ci_token`
  A Token you obtained to register the Runner. Default value is ``.

- defaults
  - `gitlab_runner_skip_registration`  
  Skip gitlab-runner registration after installation. Default value is `False`    
  - `gitlab_host`  
  Docker gitlab server. Default value is `git.epam.com`
  - `gitlab_runner_tags`  
  The tags associated with the Runner. Should be comma delimited. Default value is `delegated`
  - `gitlab_runner_untagged_builds_run`  
  Config that prevents it from picking untagged jobs. Default value is `False`
  - `gitlab_runner_lock_to_project`  
  Config that lock the Runner to current project. Default value is `False`
  - `gitlab_runner_executor`  
  Runner executor. Default value is `shell`
  - `gitlab_runner_extra_options`  
  Extra option for runner registration process. Default value is `undefined`  
  - `gitlab_runner_limit`  
  Config that Limit how many jobs can be handled concurrently by this token. `0` simply means don't limit. Default value is `1`
  - `gitlab_runner_concurrent`  
  Limits how many jobs globally can be run concurrently.
  The most upper limit of jobs using all defined runners. 
  0 does not mean unlimited. Default value is `ansible_processor_vcpus`
  - `gitlab_runner_request_concurrency`  
  Limit number of concurrent requests for new jobs from GitLab. Default value is `1`
  - `gitlab_runner_env_vars`  
  Append or overwrite environment variables. Default value is `["ENV=value", "LC_ALL=en_US.UTF-8"]`
  - `packages_additional`  
  Install additional packages for all installs. Default value is `[]`
  - `gitlab_runner_gpg`  
  GPG key for Debian. Default value is `https://packages.gitlab.com/gpg.key`  

## Some examples of the installing current role

ansible-galaxy install lean_delivery.gitlab-runner

Example Playbook
----------------

### Installing gitlab-runner to centos 7:
```yaml
- name: Converge
  hosts: rhel_family
  roles:
    - role: ansible-role-gitlab-runner
      vars:
        gitlab_runner_concurrent: 1
        gitlab_runner_skip_registration: True
```

### Installing gitlab-runner to ubuntu 18.04:
```yaml
- name: Converge
  hosts: debian_family
  roles:
    - role: ansible-role-gitlab-runner
      vars:
        gitlab_runner_concurrent: 1
        gitlab_version: "10.5"
        gitlab_runner_skip_registration: True
```

License
-------

Apache

Author Information
------------------

authors:
  - Lean Delivery <team@lean-delivery.com>
