# ⚖️ Kubernetes Gateway API Series - Post 4: Weighted Routing (80/20)

**Previous Posts:** [Basic Gateway](#) | [Hostname Rewrite](#) | [Traffic Splitting](#)

---

## 💡 Why Gateway API for Weighted Routing?

**With Ingress:** Impossible without service mesh (Istio, Linkerd)
**With Gateway API:** Simple `weight` field in backendRefs - production-ready canary deployments!

This is THE killer feature - safe deployments without adding complex service mesh infrastructure.

---

## 🎯 What is Weighted Routing?

Control exactly HOW MUCH traffic goes to each backend - perfect for safe canary deployments!

**The Difference:**

```
Traffic Splitting (50/50):     Weighted Routing (80/20):
Equal split                     Controlled split
Higher risk                     Lower risk
A/B testing                     Canary deployments
```

**The Concept:**

```
10 Users Visit arena.com
         ↓
   [Envoy Proxy]
   Applies Weights
         ↓
    _____|_____
   |           |
   8 users     2 users
      ↓           ↓
  Backend     Backend-2
  (Stable)    (Canary)
  80%         20%
```

**Real-World Scenario - Canary Deployment:**

```
Day 1: Deploy new feature
  ├─ 80% users → Old stable version (safe)
  └─ 20% users → New version (testing)

Monitor for 24 hours:
  ├─ Check error rates
  ├─ Check performance
  └─ Gather user feedback

If new version is good:
  ├─ Increase to 50/50
  ├─ Then 20/80 (flip it!)
  └─ Finally 0/100 (fully deployed)

If new version has issues:
  └─ Set to 100/0 (instant rollback!)
```

**Configuration:**
```yaml
backendRefs:
  - name: backend
    port: 80
    weight: 8      # 80% traffic
  - name: backend-2
    port: 80
    weight: 2      # 20% traffic
```

**Testing Results:**
Sent 20 requests:
- ✅ backend (stable): 15 hits = 75%
- ✅ backend-2 (canary): 5 hits = 25%

Close to 80/20 split - it's probabilistic!

**Visual Diagram Key:**
- 🟢 Green thick line = 80% traffic (stable version)
- 🟠 Orange thin line = 20% traffic (canary version)

**Why 80/20 is SAFER:**
- Most users stay on proven stable version
- Small subset tests new features
- Quick rollback if issues found
- Gradual confidence building

**Common Weight Patterns:**

| Phase | Stable | Canary | Purpose |
|-------|--------|--------|---------|
| Initial | 95% | 5% | Minimal risk testing |
| Testing | 80% | 20% | Confident in canary |
| Expansion | 50% | 50% | Equal confidence |
| Flip | 20% | 80% | New is now stable |
| Complete | 0% | 100% | Full rollout |

**Use Cases:**
1. **Canary Deployments:** Gradual rollout of new versions
2. **Risk Mitigation:** Test with subset before full release
3. **Performance Testing:** Compare load handling
4. **Feature Flags:** Controlled feature releases

**Browser Test:**
- Open: http://arena.com:32089
- Refresh 10 times
- Count appearances:
  - Stable backend: ~8 times
  - Canary backend: ~2 times

**Key Advantages Over 50/50:**
✅ Lower risk (most traffic on stable)
✅ Precise control (any weight ratio)
✅ Easy rollback (change weight to 100/0)
✅ Production-safe (proven pattern)

**Best Practices:**
1. Start small (95/5 or 90/10)
2. Monitor metrics closely
3. Increase gradually
4. Have rollback plan ready
5. Automate weight changes

📊 Visual Diagram: weighted-routing-flow.png
📝 Testing Guide: 04-weighted/TESTING-GUIDE.md

---

## 🎉 Series Complete!

We covered:
1. ✅ Basic Gateway - Entry point setup
2. ✅ Hostname Rewrite - Domain compatibility
3. ✅ Traffic Splitting - A/B testing
4. ✅ Weighted Routing - Safe deployments

**All scenarios include:**
- Python-generated diagrams
- Step-by-step testing guides
- Real-world use cases
- Working examples

**Key Takeaways:**
- Gateway API is powerful and flexible
- Envoy Gateway auto-creates infrastructure
- Different patterns for different needs
- Visual diagrams help understanding

#Kubernetes #GatewayAPI #CanaryDeployment #DevOps #WeightedRouting #CloudNative #ProductionReady

---

*Thanks for following the series! All code and diagrams available in the kubernetes-gateway-api repo.*

**Want to learn more?** Drop a comment or DM - happy to help! 🚀
