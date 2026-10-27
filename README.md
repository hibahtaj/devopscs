# QuickBite — Online Food Ordering System

A simple **Python Flask** project for the DevOps CI/CD case study. Features: Home, Menu, Cart, Order Confirmation, and a health endpoint. Food items are predefined; the cart uses Flask's signed cookie session. **Demo only:** no real payments, persistent orders, or database.

## 1. Open and run in VS Code (macOS)

Open the `QuickBite` folder in VS Code, then open Terminal → New Terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000 and try Menu → Add to Cart → Cart → Place Order.

For Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1` and use `python app.py`.

Run tests:

```bash
python -m unittest discover -s tests -v
```

## 2. Push to GitHub

Create an **empty** repository named `quickbite-devops` on GitHub (don't pre-add a README), then in the project folder run:

```bash
git init
git add .
git commit -m "Initial QuickBite Flask application"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/quickbite-devops.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME`. GitHub may ask for browser authentication or a personal access token.

## 3. Docker (after Git is working)

Start Docker Desktop:

```bash
docker build -t quickbite:local .
docker run --rm -p 5000:5000 -e SECRET_KEY=local-demo-secret quickbite:local
```

Visit http://localhost:5000. Stop with Ctrl+C.

## 4. Kubernetes (Docker Desktop Kubernetes or another local cluster)

Enable Kubernetes in Docker Desktop and ensure `kubectl get nodes` works. For a manual local deployment, create a secret and use the local Docker image (if your cluster can access it):

```bash
kubectl create secret generic quickbite-secret --from-literal=secret-key=local-demo-secret
sed 's|DOCKER_IMAGE_PLACEHOLDER|quickbite:local|g' k8s/deployment.yaml | kubectl apply -f -
kubectl apply -f k8s/service.yaml
kubectl port-forward service/quickbite-service 8080:80
```

Visit http://localhost:8080. If the image cannot be pulled by your cluster, push it to Docker Hub and use that image name instead.

## 5. Jenkins CI/CD (configure later)

`Jenkinsfile` is included for the assignment, but **it will not automatically work until Jenkins is configured**.

Prerequisites:
- Jenkins agent with `docker` and `kubectl` installed and permission to use Docker and the Kubernetes cluster.
- A Docker Hub repository named `quickbite` under your account.
- Jenkins username/password credential ID **`dockerhub-credentials`** (Docker Hub username and access token).
- A Kubernetes secret named `quickbite-secret` containing key `secret-key`, created **once** in the target namespace before running the pipeline.
- Replace `YOUR_DOCKERHUB_USERNAME` in `Jenkinsfile` with your actual Docker Hub username, commit, and push.
- Create a Jenkins **Pipeline** job configured as **Pipeline script from SCM**, select Git, set your repository URL, branch `*/main`, and script path `Jenkinsfile`.
- Configure a GitHub webhook to `https://YOUR_PUBLIC_JENKINS_URL/github-webhook/` with push events, and enable the **GitHub hook trigger for GITScm polling** in the Jenkins job. Jenkins must be reachable by GitHub; localhost alone is not reachable. The GitHub plugin/webhook support must be installed and configured.

On a push, Jenkins checks out code, builds a versioned Docker image, pushes it to Docker Hub, and updates the Kubernetes Deployment. Keep the Kubernetes secret and registry credentials out of Git.

**Note:** This is a student demonstration, not a production-ready food-ordering service. A stable secret is necessary to preserve Flask sessions across container restarts. Use a strong secret outside local demos.
