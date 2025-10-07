# tests/test_fortigate.py
import pytest
import paramiko


def pytest_addoption(parser):
    """Register custom command-line options for pytest."""
    parser.addoption("--fortigate-version", action="store", default=None, help="FortiGate version under test")
    parser.addoption("--fortigate-host", action="store", default=None, help="FortiGate host/IP")
    parser.addoption("--fortigate-user", action="store", default=None, help="FortiGate username")
    parser.addoption("--fortigate-pass", action="store", default=None, help="FortiGate password")


@pytest.fixture(scope="session")
def fortigate_config(request):
    """Expose FortiGate connection parameters as a fixture."""
    return {
        "version": request.config.getoption("--fortigate-version"),
        "host": request.config.getoption("--fortigate-host"),
        "user": request.config.getoption("--fortigate-user"),
        "password": request.config.getoption("--fortigate-pass"),
    }


@pytest.fixture(scope="session")
def ssh_client(fortigate_config):
    """Open an SSH connection to FortiGate."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=fortigate_config["host"],
        username=fortigate_config["user"],
        password=fortigate_config["password"],
        look_for_keys=False,
        allow_agent=False,
    )
    yield client
    client.close()


def run_command(client, command):
    """Helper to run CLI commands on FortiGate."""
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if error:
        raise RuntimeError(f"Error running '{command}': {error}")
    return output


def test_fortigate_version(fortigate_config, ssh_client):
    """Verify FortiGate version matches the expected one."""
    output = run_command(ssh_client, "get system status")
    assert fortigate_config["version"] in output, f"Expected version {fortigate_config['version']} not found"


def test_fortigate_interface_up(ssh_client):
    """Example test: check at least one interface is up."""
    output = run_command(ssh_client, "get system interface")
    assert "up" in output.lower(), "No active interfaces found"


def test_fortigate_license_valid(ssh_client):
    """Example test: check license status."""
    output = run_command(ssh_client, "get system license status")
    assert "valid" in output.lower(), "FortiGate license not valid"
