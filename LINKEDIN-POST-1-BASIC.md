# 🚀 Kubernetes Gateway API - Complete Learning Series

I spent time learning Kubernetes Gateway API and created 4 hands-on scenarios with real diagrams and testing guides. Here's the complete series:

---

## 🆕 Why Gateway API? (Alternative to Ingress)

**The Problem with Ingress:**
- Limited routing capabilities (basic path/host matching)
- Vendor-specific annotations for advanced features
- No standard way to configure traffic splitting, rewrites, etc.
- Single monolithic resource

**Gateway API Solution:**
✅ **Role-oriented:** Separate resources for different teams (GatewayClass for cluster ops, Gateway for platform team, HTTPRoute for app developers)
✅ **Expressive:** Built-in support for traffic splitting, header manipulation, rewrites
✅ **Extensible:** Standardized way to add custom features
✅ **Portable:** Same config works across different implementations (Envoy, NGINX, Istio)

**Migration Path:**
```
Ingress (old) → Gateway API (new)
├─ Ingress rules → HTTPRoute
├─ IngressClass → GatewayClass
└─ LoadBalancer → Gateway
```

**When to use Gateway API:**
- Need advanced routing (weights, splits, rewrites)
- Multi-team environments with different responsibilities
- Want vendor-neutral configuration
- Building modern cloud-native applications

---

## 📚 Post 1: Basic Gateway Setup - Your First Entry Point

**What I Learned:**
Set up a basic Gateway with Envoy Gateway controller to route external traffic to backend pods.

**Key Concepts:**
- GatewayClass = Blueprint (like choosing Toyota or BMW to build your gateway)
- Gateway = The actual front door (entry point on port 80)
- HTTPRoute = Routing rules (spartacus.com → backend service)

**Real-World Analogy:**
Think of Gateway as a building entrance where all visitors enter, and HTTPRoute as the directory sign showing which room to visit.

**Components Created:**
✅ Envoy Gateway Controller (factory that builds gateways)
✅ Gateway Service (auto-created with NodePort for external access)
✅ Envoy Proxy Pod (traffic handler that applies routing rules)
✅ Backend deployment (nginxdemos/hello app)

**What Happens:**
1. User visits spartacus.com:30080
2. Gateway Service receives request
3. Envoy Proxy checks HTTPRoute rules
4. Routes to backend service → backend pod
5. Response flows back to user

**Testing:**
- Browser: http://spartacus.com:30080
- Terminal: `curl http://spartacus.com:30080`

**Key Insight:**
Gateway Service is NOT in your YAML files - it's automatically created by Envoy Gateway Controller when you apply gateway.yaml!

📊 Visual Diagram: 01-basic-deploy-flow.png
📝 Full Guide: COMPLETE-EXPLANATION.md

---

**Next Post:** Hostname Rewrite - How to make old URLs work with new backend domains!

#Kubernetes #GatewayAPI #DevOps #CloudNative #EnvoyGateway #Learning

---

*Want to follow along? Check out the kubernetes-gateway-api repo with all diagrams and test guides!*
