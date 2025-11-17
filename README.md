# Minikube + ArgoCD + Helm Demo (Version 11)

This project is a small, practical setup that installs **Minikube**, **ArgoCD**, 
and deploys a simple **NGINX Helm chart** automatically. It was built to create 
a repeatable, quick lab environment for testing ArgoCD and understanding the GitOps flow.

The goal is to make it easy for anyone (including future team members) to spin up
ArgoCD locally and see a real Helm deployment in action with minimal manual commands.

---

# 🚀 What This Project Does

When you run:

```bash
python3 startup.py
```

The project:

1. **Detects your OS (Linux/macOS/Windows)**  
2. **Installs tooling if needed**  
   - Linux/macOS → curl installers  
   - Windows → Chocolatey + choco packages  
3. **Starts Minikube** with Docker driver  
4. **Installs ArgoCD**  
5. **Creates the `demo-app` namespace**  
6. **Deploys the Helm chart via ArgoCD**  
7. **Waits until the demo NGINX pod is Running**  
8. **Prints ArgoCD admin credentials**  
9. **Automatically starts background port-forwards** for:  
   - ArgoCD UI → https://localhost:8080  
   - Demo NGINX App → http://localhost:8081  
10. **Prints instructions on how to stop port-forwards** per OS  
11. **Displays a security warning** about keeping port-forwards running

---

# 📁 Project Structure

```text
minikube-argo-helm-project-v11/
├── startup.py
├── argocd-application.yaml
├── .gitignore
├── scripts/
│   ├── common_functions.py
│   ├── linux_setup.py
│   ├── windows_setup.py
│   ├── cluster_setup.py
│   ├── port_forwarder.py
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
Install Docker Desktop:  
https://www.docker.com/products/docker-desktop/

### ✔ Python 3.7+

### ✔ Linux / macOS / Windows 10+

### ✔ Chocolatey (Windows only)  
Automatically installed if missing.

---

# ▶️ How To Run

### Linux / macOS
```bash
python3 startup.py
```

### Windows
```powershell
python startup.py
```

Script handles all setup steps automatically.

---

# 🔑 Accessing ArgoCD

ArgoCD is automatically port-forwarded in the background.

### UI:
```
https://localhost:8080
```

### Login:
- **Username:** admin  
- **Password:** printed by the script (read from ArgoCD secret)

---

# 🌐 Accessing the Demo Application

Also automatically port-forwarded to:

```
http://localhost:8081
```

Shows the NGINX page deployed via Helm + ArgoCD.

---

# 🌀 Background Port-Forward Behavior

The script uses **subprocess.Popen** to run two background port-forwards:

```
ArgoCD UI → 8080:443
Demo App  → 8081:80
```

You will see output like:

```
Background port-forwards started:
  ArgoCD UI PID:    12345
  Demo App PID:     12346
```

---

# 🛑 How To Stop Background Port-Forwards

### macOS / Linux
```bash
kill <PID_OF_ARGOCD>
kill <PID_OF_DEMO_APP>
```

If you lost the PIDs:
```bash
pkill -f "kubectl port-forward"
```

---

### Windows (PowerShell or CMD)

```powershell
taskkill /PID <PID_OF_ARGOCD> /F
taskkill /PID <PID_OF_DEMO_APP> /F
```

Or stop via Task Manager by searching for these PIDs.

---

# ⚠️ Security Warning

Port-forwards expose cluster services on:

- `localhost:8080` → ArgoCD  
- `localhost:8081` → Demo App  

If left running:

- Browser extensions  
- Local scripts  
- Developer tools  

**could access your cluster without your knowledge.**

Always stop port-forwards after testing.

---

# 🧹 Cleanup

To clean demo resources or delete the Minikube cluster:

```
python3 -m scripts.cleanup
```

This deletes:

- ArgoCD Application  
- Resources created by `argocd-application.yaml`  
- `argocd` and `demo-app` namespaces  
- (Optional) Minikube cluster  

If Minikube delete fails:

```
minikube delete --all --purge
```

---

# ⚙️ Constraints & Assumptions

- Simple configuration intended for **local testing only**  
- Fixed `demo-app` namespace for predictable behavior  
- Demo Service is **ClusterIP** (port-forward required)  
- No TLS/Ingress  
- Minikube uses default resource settings  
- Windows installs use Chocolatey for consistency  

---

# 🔧 Possible Improvements

- CLI flags for namespace / Helm chart path  
- Customizable port-forward ports  
- Add an option to disable auto port-forward  
- Basic Application Sync verification  
- Support multiple demo apps  
- More descriptive NGINX homepage  

---

# 🛠️ How This Was Built

This project is built using a DevOps-first approach:

- Automate everything end-to-end  
- Keep scripts simple, explainable, and easy to follow  
- Use declarative deployment (Helm + ArgoCD)  
- Provide cross-platform setup (Linux/macOS/Windows)  
- Include cleanup and background process handling  

A GPT coding assistant helped draft scripting and YAML structures,  
but the flow, architecture, decisions, troubleshooting, and validations 
were done by me so I can explain each part clearly during a demo.

---

# 🎯 Summary

This project provides a **fully automated GitOps demo** using:

- Minikube  
- ArgoCD  
- Helm  
- Cross-platform Python scripting  
- Background port-forward handling  
- Cleanup automation  

It is ideal for interviews, workshops, and personal GitOps experimentation.
