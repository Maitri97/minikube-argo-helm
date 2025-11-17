import os
import sys

# Allow:
# - python -m scripts.cleanup   (from project root)
# - python scripts/cleanup.py   (from scripts/ folder)
if __name__ == "__main__" and __package__ is None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)
    from common_functions import run_cmd
else:
    from .common_functions import run_cmd


def kube_cluster_reachable():
    """
    Check if the Kubernetes cluster is reachable by running:
      kubectl get pods -A

    If this fails, we skip Kubernetes deletions but still allow
    Minikube cleanup.
    """
    print("Checking Kubernetes cluster availability (kubectl get pods -A)...")
    code = run_cmd(["kubectl", "get", "pods", "-A"])
    if code != 0:
        print(
            "Kubernetes cluster is not reachable or kubectl is not configured.\n"
            "Skipping Kubernetes resource cleanup."
        )
        return False
    return True


def main():
    print("This will remove:")
    print("  - ArgoCD Application (demo-app)")
    print("  - Resources defined in argocd-application.yaml")
    print("  - Namespaces: demo-app, argocd")
    print("  - (Optional) Minikube cluster")

    choice = input("\nAre you sure you want to continue? (y/n): ").strip().lower()
    if choice != "y":
        print("Cleanup cancelled.")
        return

    cluster_ok = kube_cluster_reachable()

    if cluster_ok:
        print("\nDeleting ArgoCD Application (if it exists)...")
        run_cmd(["kubectl", "delete", "application", "demo-app", "-n", "argocd"])

        print("\nDeleting ArgoCD Application manifest resources (if present)...")
        run_cmd(["kubectl", "delete", "-n", "argocd", "-f", "argocd-application.yaml"])

        print("\nDeleting namespaces (if they exist)...")
        run_cmd(["kubectl", "delete", "namespace", "demo-app"])
        run_cmd(["kubectl", "delete", "namespace", "argocd"])
    else:
        print("\nSkipping Kubernetes deletions because cluster is not reachable.")

    delete_mk = input(
        "\nDo you want to delete the Minikube cluster as well? (y/n): "
    ).strip().lower()

    if delete_mk == "y":
        print("Deleting Minikube cluster...")
        mk_code = run_cmd(["minikube", "delete"])
        if mk_code != 0:
            print(
                "\nMinikube delete did not complete successfully.\n"
                "If you suspect a corrupted or stale Minikube profile, "
                "you can run a full reset with:\n"
                "  minikube delete --all --purge\n"
            )
    else:
        print("Skipping Minikube delete.")

    print("\nCleanup complete.")


if __name__ == "__main__":
    main()
