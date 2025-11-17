# Minikube + ArgoCD + Helm Demo (Version 10)

This project is a small, practical setup that installs **Minikube**, **ArgoCD**, 
and deploys a simple **NGINX Helm chart** automatically. It was built to create 
a repeatable, quick lab environment for testing ArgoCD and understanding the GitOps flow.

The goal is to make it easy for anyone (including future team members) to spin up
ArgoCD locally and see a real Helm deployment in action with minimal manual commands.

---

# 🚀 What This Project Does

When you run:

```
python3 startup.py
```

The project:

1. **Detects your OS (Linux/macOS/Windows)**  
2. **Installs tools** if needed (Linux/macOS auto-install; Windows uses Chocolatey)
3. **Starts Minikube**
4. **Installs ArgoCD**
5. **Creates `demo-app` namespace**
6. **Applies ArgoCD Application YAML**
7. **Waits until the demo NGINX pod is Running**
8. **Prints ArgoCD admin credentials**
9. **Gives port-forward commands** for:
   - ArgoCD UI → https://localhost:8080  
   - NGINX App → http://localhost:8081  

---

# 📁 Project Structure

```
minikube-argo-helm-project-v10/
├── startup.py
├── argocd-application.yaml
├── .gitignore
├── scripts/
│   ├── common_functions.py
│   ├── linux_setup.py
│   ├── windows_setup.py
│   ├── argocd_port_forward.py
│   └── cleanup.py
├── nginx/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
└── docs/
    └── project-explainer-for-me.md
```

---

# 🧩 Prerequisites

### ✔ Docker  
You must install Docker Desktop:

https://www.docker.com/products/docker-desktop/

### ✔ Python 3.7+

### ✔ Linux / macOS / Windows 10+

### ✔ Chocolatey (Windows only)  
If not installed, the script will install it automatically.

---

# ▶️ How To Run

### **Linux / macOS**
```
python3 startup.py
```

### **Windows**
```
python startup.py
```

The script handles everything automatically.

---

# 🔑 Accessing ArgoCD

### Port-forward:
```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### Open in browser:
```
https://localhost:8080
```

### Login:
- **Username:** admin  
- **Password:** printed by the script  

---

# 🌐 Accessing the Demo Application

Since the Service is **ClusterIP**, it is accessed using port-forward:

```
kubectl port-forward svc/demo-app -n demo-app 8081:80
```

Open:

```
http://localhost:8081
```

This shows the NGINX page deployed by ArgoCD using the Helm chart.

---

# 🧹 Cleanup

Run:

```
python3 -m scripts.cleanup
```

This will:

- Delete ArgoCD Application  
- Delete resources defined in the Application  
- Delete namespaces `demo-app` and `argocd`  
- Ask whether to delete the Minikube cluster  

No tools (kubectl, helm, minikube) are removed automatically.

---

# ⚠️ Constraints & Assumptions

These are intentionally simple to keep the scripts readable:

### ✔ Designed for **local testing only**  
Not production-grade configuration.

### ✔ Namespace is fixed to `demo-app`  
For predictable behavior during the demo.

### ✔ No TLS/Ingress for NGINX app  
The demo shows only basic functionality.

### ✔ Minikube starts with default resources  
The script uses standard Minikube defaults.

### ✔ Windows-specific installs handled via Chocolatey  
To keep behavior consistent across OS types.

---

# 🔧 Possible Improvements (Scoped to Minikube, Scripts & ArgoCD Only)

- Add option to specify a different namespace or Helm path at runtime.
- Allow switching between NodePort and ClusterIP for the demo Service.
- Add basic verification that ArgoCD Application has synced successfully.
- Add uninstall flags for kubectl, minikube, and helm if user wants them removed.
- Add support for running multiple demo apps (multi-Application support).

(These are intentionally scoped to your requirement.)

---

# 🛠️ How This Was Built

This project reflects the approach I personally take when building internal 
DevOps tooling:

- Automate repetitive setup steps  
- Keep scripts clear, readable, and self-explanatory  
- Use standard tools (kubectl, helm, minikube, choco)  
- Keep configuration declarative where possible (Helm + ArgoCD)

A GPT-based coding assistant was used to help draft and refine file structures, 
YAML manifests, and Python scripting.  
However, the overall architecture, sequence of steps, tool choices, and final 
validation were done by me so that I can explain any part of the project 
in detail during an interview or demo.

---

# 🎯 Summary

This project gives a **hands-on, fully automated GitOps demo** using:

- Minikube  
- ArgoCD  
- Helm  
- Kubernetes basics  
- Simple port-forwarding for app/UI  
- Clean Python scripting for cross-platform setup  

It's built to be simple to use, easy to present, and useful as a practical 
POC for GitOps discussions.

