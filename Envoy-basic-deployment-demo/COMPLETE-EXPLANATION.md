# Gateway API - Complete Explanation

## 🏗️ THE SETUP (ONE TIME)

**Install Envoy Gateway Controller:**
```bash
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.6.1 -n envoy-gateway-system --create-namespace
```
This creates the **controller pod** that watches and auto-creates infrastructure.

---

## 📋 ALL COMPONENTS (12 Total)

### 🎯 YOUR 7 YAML FILES:

1. **GatewayClass** (`gateway_class.yaml`) - Blueprint saying "use Envoy"
2. **Gateway** (`gateway.yaml`) - **TRIGGERS AUTO-CREATION** of Envoy proxy infrastructure
3. **ServiceAccount** (`svc_account.yaml`) - Identity for pods
4. **Deployment** (`deploy.yaml`) - Your app (nginxdemos/hello)
5. **Service** (`svc.yaml`) - Load balancer for your app pods (backend:80)
6. **HTTPRoute** (`httproute.yaml`) - Routing rules: spartacus.com → backend:80
7. **Service Patch** (`gateway-nodeport-patch.yaml`) - Sets NodePort to 30080

### ⚡ 5 AUTO-CREATED RESOURCES:

**When you apply gateway.yaml, Envoy Gateway Controller automatically creates:**

1. **Envoy Proxy Deployment** (envoy-default-eg-e41e7b31)
2. **Envoy Proxy Pod** (envoy-default-eg-e41e7b31-xxxxx) - The traffic handler!
3. **Gateway Service** (envoy-default-eg-e41e7b31) - Entry point with NodePort 30080
4. **Backend ReplicaSet** (auto-created by your Deployment)
5. **Backend Pod** (backend-xxxxx) - Your actual app

---

## 🌊 TRAFFIC FLOW

```
Browser (spartacus.com:30080)
    ↓
NodePort 30080
    ↓
Gateway Service (Port 80 → 10080)
    ↓
Envoy Proxy Pod (Checks HTTPRoute rules)
    ↓
backend Service (Port 80)
    ↓
backend Pod (nginxdemos/hello)
```

---

## 🎯 KEY INSIGHTS

**Gateway Controller** (Helm installed) = Watches for Gateway resources
**gateway.yaml** = Triggers auto-creation of Envoy proxy + Gateway Service
**Envoy Proxy Pod** = The brain! Receives traffic, applies HTTPRoute rules, routes to backends
**Gateway Service** = NOT in your YAML! Auto-created with NodePort for external access
**HTTPRoute** = Config pushed to Envoy: "spartacus.com requests go to backend:80"

---

## ✅ QUICK VERIFICATION

```bash
# See the auto-created Envoy infrastructure
kubectl get svc -n envoy-gateway-system
kubectl get pods -n envoy-gateway-system | grep envoy-default

# See your application
kubectl get pods -l app=backend
kubectl get svc backend

# See Gateway API resources
kubectl get gateway
kubectl get httproute
```
