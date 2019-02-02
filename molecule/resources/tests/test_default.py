import os

import testinfra.utils.ansible_runner

group_name = 'all'

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(group_name)


def test_gitlab_runner_package_is_installed(host):
    flag = False
    for package in ["gitlab-runner", "gitlab-ci-multi-runner"]:
        with host.sudo():
            package = host.package(package)
            if package.is_installed and package.version.startswith("10.5"):
                flag = True
    assert flag


def test_gitlab_runner_service_running_and_enabled(host):
    flag = False
    for service in ["gitlab-runner", "gitlab-ci-multi-runner"]:
        with host.sudo():
            service = host.service(service)
            if service.is_running and service.is_enabled:
                flag = True
    assert flag
