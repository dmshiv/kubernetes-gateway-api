# Hostname Rewrite - Testing Guide

## 📊 See the Diagram
Open: `hostname-rewrite-flow.png`

**Key Visual:**
- 🔵 Blue arrow: User sends "house-of-batiatis.com"
- 🔴 Red arrow: Backend receives "house-of-ashur.com" (REWRITTEN!)

---

## 🎯 What is Hostname Rewrite?

```
User Types:          house-of-batiatis.com
                            ↓
                     [Envoy Proxy]
                            ↓
                     REWRITES HOSTNAME
                            ↓
Backend Receives:    house-of-ashur.com
```

**Browser URL NEVER changes** - Only the HTTP Host header sent to backend changes!

---

## 🔍 Understanding the Rewrite

**HTTP Request (Before Rewrite):**
```http
GET / HTTP/1.1
Host: house-of-batiatis.com
User-Agent: curl/8.12.1
```

**HTTP Request (After Rewrite):**
```http
GET / HTTP/1.1
Host: house-of-ashur.com    ← CHANGED!
User-Agent: curl/8.12.1
```

---

## 🧪 Test 1: Terminal (Verify It Works)

```bash
curl -v http://house-of-batiatis.com:32089
```

**What to check:**
1. ✅ Request succeeds (200 OK)
2. ✅ You see HTML response from nginxdemos/hello

**Why it works:** Envoy accepts "house-of-batiatis.com" and routes to backend!

---

## 🌐 Test 2: Browser (Visual Test)

1. **Open browser:** `http://house-of-batiatis.com:32089`

2. **What you see:**
   - ✅ URL bar shows: `house-of-batiatis.com:32089` (original)
   - ✅ Page loads successfully
   - ✅ Server name visible on page

3. **What's hidden:**
   - Backend received "Host: house-of-ashur.com" header
   - Backend processed it as if you visited house-of-ashur.com
   - Response came back to your browser

✅ **Success:** Page loads even though backend expects different hostname!

---

## 🔬 Test 3: Compare With/Without Rewrite

**Test WITHOUT rewrite (direct to backend service):**
```bash
# This would fail if backend checks Host header strictly
curl -H "Host: house-of-batiatis.com" http://backend:80
```

**Test WITH rewrite (through Gateway):**
```bash
# This works because Envoy rewrites the hostname
curl http://house-of-batiatis.com:32089
```

✅ **Success:** Gateway + Rewrite makes incompatible hostnames work!

---

## 🎬 Real-World Use Case

### Scenario: Company Rebrand

```
Old Domain: OldCompany.com
New Domain: NewCompany.com

Problem:
  ├─ Backend updated to expect "NewCompany.com"
  ├─ Customers still bookmarked "OldCompany.com"
  └─ Need both to work!

Solution: Hostname Rewrite
  ├─ User visits: OldCompany.com
  ├─ Gateway rewrites to: NewCompany.com
  ├─ Backend processes: NewCompany.com
  └─ User happy, backend happy!
```

**Another Example:**
```
house-of-batiatis.com (Old owner)
       ↓ REWRITE ↓
house-of-ashur.com (New owner)
```

---

## ✅ Verification Commands

**1. Quick test:**
```bash
curl -s http://house-of-batiatis.com:32089 | grep -i "server name"
```

**Expected:** HTML with server name shown (proves backend responded)

**2. Verbose test (see HTTP headers):**
```bash
curl -v http://house-of-batiatis.com:32089 2>&1 | grep -i "host:"
```

**Expected:** 
```
> Host: house-of-batiatis.com:32089
```

(This shows what YOU sent, but backend receives rewritten version)

**3. Check HTTPRoute is active:**
```bash
kubectl get httproute http-filter-url-rewrite
```

**Expected:**
```
NAME                      HOSTNAMES                   AGE
http-filter-url-rewrite   ["house-of-batiatis.com"]   10m
```

---

## 🔑 Key Points

1. **URL in browser NEVER changes** ← Always shows what you typed
2. **HTTP Host header DOES change** ← Backend sees rewritten hostname
3. **Invisible to users** ← Seamless experience
4. **Useful for migrations** ← Keep old URLs working

---

## 🎯 Test Summary

| Test | Command | What You See |
|------|---------|-------------|
| **Browser** | Open `http://house-of-batiatis.com:32089` | Page loads, URL unchanged |
| **Terminal** | `curl http://house-of-batiatis.com:32089` | HTML response (200 OK) |
| **Verify** | `kubectl get httproute` | Route shows house-of-batiatis.com |

**All tests should succeed!** ✅
