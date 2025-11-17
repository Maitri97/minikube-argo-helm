import shutil
from .common_functions import run_cmd_and_exit_on_error
from .cluster_setup import main_cluster_flow

def ensure_chocolatey():
    print("Checking Chocolatey...")
    if shutil.which("choco") is None:
        print("Installing Chocolatey...")
        run_cmd_and_exit_on_error([
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-Command",
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "[System.Net.ServicePointManager]::SecurityProtocol = "
            "[System.Net.SecurityProtocolType]::Tls12; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
        ])

def ensure_docker_running():
    print("Checking for Docker Desktop...")
    if shutil.which("docker") is None:
        print("Docker Desktop is not installed. Please install it manually:")
        print("  https://www.docker.com/products/docker-desktop/")
        exit(1)

def install_tools():
    print("Installing kubectl, Minikube, Helm via Chocolatey...")
    run_cmd_and_exit_on_error(["choco", "install", "kubernetes-cli", "-y"])
    run_cmd_and_exit_on_error(["choco", "install", "minikube", "-y"])
    run_cmd_and_exit_on_error(["choco", "install", "kubernetes-helm", "-y"])

def main():
    ensure_docker_running()
    ensure_chocolatey()

    if shutil.which("kubectl") is None or shutil.which("minikube") is None or shutil.which("helm") is None:
        install_tools()

    main_cluster_flow()
