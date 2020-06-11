gitlab-runner role
=========

[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-gitlab-runner/master/LICENSE)
[![Build Status](https://travis-ci.org/lean-delivery/ansible-role-gitlab-runner.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-gitlab-runner)
[![Build Status](https://gitlab.com/lean-delivery/ansible-role-gitlab-runner/badges/master/pipeline.svg)](https://gitlab.com/lean-delivery/ansible-role-gitlab-runner/pipelines)
[![Galaxy](https://img.shields.io/badge/galaxy-lean__delivery.gitlab__runner-blue.svg)](https://galaxy.ansible.com/lean_delivery/gitlab_runner)
![Ansible](https://img.shields.io/ansible/role/d/29089.svg)
![Ansible](https://img.shields.io/badge/dynamic/json.svg?label=min_ansible_version&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F29089%2F&query=$.min_ansible_version)

## Summary

This Ansible role has the following features:

 - Install gitlab-runner

Requirements
------------

 - Version of the ansible for installation: 2.8
 - **Supported OS**:
   - EL (RedHat, CentOS)
     - 7, 8
   - Amazon2 Linux
   - Ubuntu
     - 16.04
     - 18.04
   - Debian
     - 8, 9

## Role Variables

- required
  - `gitlab_version`  
  Specific version of Gitlab-Runner. Default value is `latest`.
  - `gitlab_api_token`  
  A token you need to access Gitlab API. Default value is `''`.
  - `gitlab_ci_token`  
  A Token you obtained to register the Runner. Default value is `''`.
  - `gitlab_runner_description`  
  The unique name of the runner. Default value:   
```
    {{ ansible_fqdn }}
    {{ ansible_distribution }}
    {{ ansible_distribution_major_version }}
```

- defaults
  - `no_logs`  
  Hide sensitive information from logs. Default value is `true`
  - `gitlab_runner_skip_registration`  
  Skip gitlab-runner registration after installation. Default value is `false`
  - `gitlab_host`   
  Docker gitlab server. Default value is `gitlab.com`
  - `gitlab_url`   
  Gitlab url address. Default value: `https://{{ gitlab_host }}/`
  - `gitlab_runner_tags`  
  The tags associated with the Runner. Should be comma delimited. Default value is `delegated`
  - `gitlab_runner_access_level: not_protected`  
  Determines if a runner can pick up jobs from protected branches. Available values: `ref_protected` `not_protected` Default value is `not_protected`
  - `gitlab_runner_untagged_builds_run`  
  Config that prevents it from picking untagged jobs. Default value is `false`
  - `gitlab_runner_lock_to_project`  
  Config that lock the Runner to current project. Default value is `false`
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
  - `gitlab_runner_package`
  Gitlab-runner package name. Default: `gitlab-runner`
  - `gitlab_runner_packages_additional`  
  Install additional packages for all installs. Default value is `[]`
  - `gitlab_runner_gpg`  
  GPG key for Debian. Default value is `https://packages.gitlab.com/gpg.key`
  - `gitlab_global_section`   
  Global section of gitclab config. Default is dictionary:
  ```yaml
    concurrent: '{{ gitlab_runner_request_concurrency }}'
    check_interval: 0
  ```

  - `gitlab_session_server_section`   
  Server section of gitlab config. Default is dictionary:
    `session_timeout: 1800`
  - `gitlab_runners_section`   
  Runners section of gitlab config. Default is dictionary:
  ```yaml
    name: '{{ gitlab_runner_description }}'
    url: '{{ gitlab_url }}'
    token: '{{ gitlab_runner.runner.token | default(omit) }}'
    executor: '{{ gitlab_runner_executor }}'
    environment: '{{ gitlab_runner_env_vars }}'
  ```

- advanced configuration
  - `gitlab_runner_config`  
  Dictionary used for advanced configs:
    - `params`  
    Environment variables used during the registration process
    - `global_values`  
    Dictionary with *key:value* used to add/change ***non string values*** in the file "config.toml"
    - `global_strings`  
    Dictionary with *key:value* used to add/change ***string values*** in the file "config.toml"

- additional variables
  - `yum_libselinux_python_library`  
  Selinux python library name. Default value: `libselinux-python`
  For RedHat 8 or Fedora library name may be different, e.g. `python3-libselinux`.  
  - `yum_libselinux_config_libraries`  
  Selinux config libraries. Default value is list: `[policycoreutils-python, libsemanage-python]`. 
  For RedHat 8 or Fedora value may be different:
    - python3-policycoreutils
    - python3-libsemanage
  - `epel_repository_url`  
  URL of EPEL repo package. Default: `https://dl.fedoraproject.org/pub/epel/epel-release-latest-{{ ansible_distribution_major_version }}.noarch.rpm`  
  - `epel_rpm_key`  
  EPEL rpm key. Default value: `/etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-{{ ansible_distribution_major_version }}`  
  - `gitlab_runner_python_module_version`  
  Version of python-gitlab library. Default: `'1.12.1'`
  - `pip_executable`  
  Name of pip executable binary. Default:
    - `pip` for RedHat based targets
    - `pip3` for Debian based targets
  - `python_executable`   
  Name of python executable. Default:
    - `python` for RedHat based targets
    - `python3` for Debian based targets

## Some examples of the installing current role

With [playlabs](https://yourlabs.io/oss/playlabs) you can install this role with just one command, ie:

    playlabs install lean_delivery.gitlab_runner @localhost gitlab_ci_token=yourcommand gitlab_host=yourlabs.io gitlab_runner_limit=4 gitlab_version=11.6

Or, without playlabs, install with galaxy so that you can use with your playbook:

ansible-galaxy install lean_delivery.gitlab_runner

Example Playbook
----------------

### Installing gitlab-runner without registration:
```yaml
- name: Converge
  hosts: gitlab_runner
  roles:
    - role: lean_delivery.gitlab_runner
  vars:
    gitlab_runner_concurrent: 1
    gitlab_runner_skip_registration: true
```

### Installing gitlab-runner with registration and config:
```yaml
- name: Converge
  hosts: gitlab_runner
  roles:
    - role: lean_delivery.gitlab_runner
      gitlab_runner_concurrent: 4
      gitlab_runner_skip_registration: false
      gitlab_api_token: >-
        {{ lookup('env', 'GITLAB_API_TOKEN') }}
      gitlab_ci_token: >-
        {{ lookup('env', 'GITLAB_REGISTRATION_TOKEN') }}
      gitlab_runner_description: 'My Great Runner'
      gitlab_runner_tags:
        - deploy_test
        - shell
      gitlab_runner_untagged_builds_run: false
      gitlab_runner_concurrent: 1
      gitlab_version: '12.5.1'
      gitlab_runner_skip_registration: false
```

License
-------

Apache

[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-gitlab-runner/master/LICENSE)

Author Information
------------------

authors:
  - Lean Delivery Team <team@lean-delivery.com>
