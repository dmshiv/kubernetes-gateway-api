# 🎲 Kubernetes Gateway API Series - Post 3: Traffic Splitting (50/50)

**Previous Posts:** [Basic Gateway](#) | [Hostname Rewrite](#)

---

## 💡 Why Gateway API for Traffic Splitting?

**With Ingress:** Not possible! Need service mesh or custom controllers
**With Gateway API:** Native support via multiple backendRefs - no extra tools needed!

This showcases Gateway API's power - advanced traffic management built into the standard.

---

## 🎯 What is Traffic Splitting?

Split incoming traffic equally between two versions of your app - perfect for A/B testing!

**The Concept:**

```
10 Users Visit gladiators.com
         ↓
   [Envoy Proxy]
    Splits 50/50
         ↓
    _____|_____
   |           |
   5 users     5 users
      ↓           ↓
  Backend     Backend-2
  (v1.0)      (v2.0)
```

**Real-World Analogy:**
Restaurant with 2 kitchens - waiter randomly sends customers to either kitchen equally.

**Use Cases:**
1. **A/B Testing:** Test new UI with 50% of users
2. **Feature Flags:** Roll out features gradually
3. **Load Distribution:** Balance between two identical deployments
4. **Blue-Green Testing:** Before full switch, test both versions

**How It Works:**

**Configuration:**
```yaml
backendRefs:
  - name: backend      # Gets 50% traffic
    port: 80
  - name: backend-2    # Gets 50% traffic
    port: 80
```

No weights specified = equal distribution!

**What Happens:**
1. User visits gladiators.com:32089
2. Envoy Proxy reads HTTPRoute
3. Randomly picks backend or backend-2
4. Routes request to chosen backend
5. Next request might go to different backend

**Testing Results:**
Sent 20 requests:
- ✅ backend-8gkmk: 10 hits (50%)
- ✅ backend-2-g8d6c: 10 hits (50%)

**Browser Test:**
- Open: http://gladiators.com:32089
- Look at "Server name" field
- Press F5 (refresh) multiple times
- Server name alternates between pods!

**Key Components:**
- 2 Deployments (backend & backend-2)
- 2 Services (backend:80 & backend-2:80)
- 1 HTTPRoute (splits traffic between both)
- 1 Gateway (entry point)

**When To Use:**
- ✅ A/B testing new features
- ✅ Comparing performance of two versions
- ✅ User experience experiments
- ✅ Equal load distribution

**When NOT To Use:**
- ❌ Production rollouts (use weighted routing instead)
- ❌ When you need control over traffic percentage

📊 Visual Diagram: traffic-splitting-flow.png
📝 Testing Guide: 03-traffic-spiltting/TESTING-GUIDE.md

---

**Next Post:** Weighted Routing (80/20) - Safer canary deployments with controlled traffic!

#Kubernetes #GatewayAPI #ABTesting #DevOps #TrafficSplitting #CloudNative

---

*Final post coming soon: Weighted routing for safe production rollouts!*
