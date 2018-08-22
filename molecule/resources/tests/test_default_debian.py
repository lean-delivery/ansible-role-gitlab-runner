import os

import testinfra.utils.ansible_runner

group_name = 'ansible_role_gitlab_runner_ubuntu_ct'

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(group_name)


def test_gitlab_runner_package_is_installed(host):
    gitlab_runner_pkg = host.package("gitlab-runner")
    assert gitlab_runner_pkg.is_installed
    assert gitlab_runner_pkg.version.startswith("10.5")


def test_gitlab_runner_service_running_and_enabled(host):
    gitlab_runner_svc = host.service("gitlab-runner")
    assert gitlab_runner_svc.is_running
    assert gitlab_runner_svc.is_enabled
