import subprocess
import sys

def start_port_forwards():
    """
    Start port-forwarding for:
      - ArgoCD UI  -> localhost:8080 -> argocd-server:443
      - Demo App   -> localhost:8081 -> demo-app:80

    Runs both port-forwards in the BACKGROUND using subprocess.Popen,
    so the main script does not block.

    Prints:
      - The PIDs of the background processes
      - OS-specific instructions for stopping them
      - A warning about leaving port-forwards open (security risk)
    """

    print("\n=== Starting Background Port-Forwards ===")

    # ArgoCD UI port-forward
    argocd_proc = subprocess.Popen(
        [
            "kubectl", "port-forward",
            "svc/argocd-server", "-n", "argocd", "8080:443"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Demo App port-forward
    demo_proc = subprocess.Popen(
        [
            "kubectl", "port-forward",
            "svc/demo-app", "-n", "demo-app", "8081:80"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("\nBackground port-forwards started:")
    print(f"  ArgoCD UI PID:    {argocd_proc.pid}")
    print(f"  Demo App PID:     {demo_proc.pid}")

    print("\nYou can now access:")
    print("  ArgoCD UI:        https://localhost:8080")
    print("  Demo Application: http://localhost:8081")

    print("\n=== How to Stop These Port-Forwards ===")

    if sys.platform.startswith("win"):
        # Windows
        print("\nOn Windows (PowerShell or CMD):")
        print("  To stop the ArgoCD port-forward:")
        print(f"    taskkill /PID {argocd_proc.pid} /F")
        print("  To stop the Demo App port-forward:")
        print(f"    taskkill /PID {demo_proc.pid} /F")
        print("\nYou can also use Task Manager and kill these PIDs manually.")
    else:
        # Linux / macOS
        print("\nOn Linux / macOS:")
        print("  To stop the ArgoCD port-forward:")
        print(f"    kill {argocd_proc.pid}")
        print("  To stop the Demo App port-forward:")
        print(f"    kill {demo_proc.pid}")
        print("\nIf you lose the PIDs, you can kill all kubectl port-forwards with:")
        print("    pkill -f 'kubectl port-forward'")

    print("\n=== Security Note ===")
    print("These port-forwards expose cluster services on localhost ports.")
    print("If you forget to stop them, local tools or browser plugins could")
    print("talk to ArgoCD or the demo app without you realizing it.")
    print("Always stop these port-forwards once you are done testing.\n")

    print("If you want to remove all demo namespaces and optionally the Minikube")
    print("cluster itself, you can run:")
    print("  python3 -m scripts.cleanup")

    return argocd_proc.pid, demo_proc.pid


def main():
    # Allow running directly: python -m scripts.port_forwarder
    start_port_forwards()


if __name__ == "__main__":
    main()
