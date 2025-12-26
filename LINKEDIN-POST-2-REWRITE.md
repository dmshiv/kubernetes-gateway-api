# 🔄 Kubernetes Gateway API Series - Post 2: Hostname Rewrite

**Previous Post:** [Basic Gateway Setup](#)

---

## 💡 Why Gateway API for Rewrites?

**With Ingress:** Need vendor-specific annotations (nginx.ingress.kubernetes.io/rewrite-target)
**With Gateway API:** Standardized `urlRewrite` filter works across all implementations!

This is a perfect example of Gateway API's advantage - built-in support for common patterns without custom annotations.

---

## 🎯 What is Hostname Rewrite?

Ever rebranded your company but backend still expects the old domain? Hostname rewrite solves this!

**The Problem:**
- Users visit: house-of-batiatis.com
- Backend expects: house-of-ashur.com
- Without rewrite: ❌ Request fails

**The Solution:**
Gateway rewrites the HTTP Host header before sending to backend!

**How It Works:**

```
User Types:          house-of-batiatis.com
                            ↓
                     [Gateway + Envoy]
                            ↓
                     REWRITES HOSTNAME
                            ↓
Backend Receives:    house-of-ashur.com
```

**Real-World Use Cases:**
1. **Company Rebrand:** Keep old domain working while backend uses new domain
2. **Domain Migration:** Gradually move from old to new domain
3. **Multi-brand:** Same backend serves multiple brand domains

**What Gets Rewritten:**
```http
BEFORE (User sends):
Host: house-of-batiatis.com

AFTER (Backend receives):
Host: house-of-ashur.com
```

**Important:** Browser URL NEVER changes - only the HTTP Host header changes!

**Configuration:**
```yaml
urlRewrite:
  hostname: house-of-ashur.com
```

**Testing:**
- Browser: http://house-of-batiatis.com:32089
- Result: Page loads successfully (backend got rewritten hostname)
- User sees: Original URL in browser
- Backend sees: Rewritten hostname in Host header

**Key Insight:**
This is invisible to users but crucial for backend compatibility. Perfect for migrations!

📊 Visual Diagram: hostname-rewrite-flow.png
📝 Testing Guide: 02-url-rewrite/TESTING-GUIDE.md

---

**Next Post:** Traffic Splitting - How to A/B test with 50/50 traffic distribution!

#Kubernetes #GatewayAPI #DevOps #Migration #HostnameRewrite #CloudNative

---

*Following the series? Post 3 covers traffic splitting for A/B testing!*
