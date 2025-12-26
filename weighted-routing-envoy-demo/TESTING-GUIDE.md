# Weighted Routing (80/20) - Testing Guide

## 📊 See the Diagram
Open: `weighted-routing-flow.png`

**Key difference from 50/50:** 
- 🟢 Green line is THICKER (80% traffic to stable version)
- 🟠 Orange line is THINNER (20% traffic to canary version)

---

## 🎯 What is 80/20 Weighted Routing?

```
10 Requests Come In
        ↓
   [Envoy Proxy]
        ↓
   Weights: 8:2
        ↓
    _____|_____
   |           |
   8 requests  2 requests
   go LEFT     go RIGHT
      ↓           ↓
  Backend     Backend-2
  (Stable)    (Canary)
  80%         20%
```

**Use Case:** Slowly test new version while keeping most traffic on stable version!

---

## 🧪 Test 1: Terminal (Count the Distribution)

Send 20 requests and count hits:
```bash
echo "Testing 20 requests..."
for i in {1..20}; do 
  curl -s http://arena.com:32089 | grep -o "backend-[^ ]*" | head -1
done | sort | uniq -c
```

**Expected Result:**
```
  16 backend-7f64676864-8gkmk     ← ~80% (16 out of 20)
   4 backend-2-7b5d6b96dc-g8d6c   ← ~20% (4 out of 20)
```

✅ **Success:** Backend gets 4x more hits than backend-2!

---

## 🌐 Test 2: Browser (Visual Test)

1. **Add hostname:**
```bash
echo "127.0.0.1 arena.com" | sudo tee -a /etc/hosts
```

2. **Open browser:** `http://arena.com:32089`

3. **Look for Server name:**
   ```
   Server name: backend-7f64676864-8gkmk
   ```

4. **Refresh 10 times (F5)** and count:
   - How many times you see: `backend-7f64676864-8gkmk` ← Should be ~8 times
   - How many times you see: `backend-2-7b5d6b96dc-g8d6c` ← Should be ~2 times

✅ **Success:** You see the stable backend MUCH MORE often!

---

## 📈 Test 3: Detailed Analysis

Run 50 requests to see clear distribution:
```bash
echo "=== Testing 50 Requests ==="
backend_count=0
backend2_count=0

for i in {1..50}; do 
  result=$(curl -s http://arena.com:32089 | grep -o "backend-[^ ]*" | head -1)
  if [[ $result == *"backend-2"* ]]; then
    backend2_count=$((backend2_count + 1))
    echo -n "🟠"
  else
    backend_count=$((backend_count + 1))
    echo -n "🟢"
  fi
done

echo ""
echo ""
echo "Results:"
echo "🟢 Backend (stable):  $backend_count hits (~$((backend_count * 2))%)"
echo "🟠 Backend-2 (canary): $backend2_count hits (~$((backend2_count * 2))%)"
```

**Expected Output:**
```
🟢🟢🟢🟢🟠🟢🟢🟢🟢🟢🟢🟠🟢🟢🟢...

Results:
🟢 Backend (stable):  40 hits (~80%)
🟠 Backend-2 (canary): 10 hits (~20%)
```

✅ **Success:** Clear 80/20 split!

---

## 🎬 Real-World Scenario

**Canary Deployment:**

```
Day 1: Deploy new feature
  ├─ 80% users → Old stable version (safe)
  └─ 20% users → New version (testing)

Monitor for 24 hours:
  ├─ Check error rates
  ├─ Check performance
  └─ Gather user feedback

If new version is good:
  ├─ Increase weight to 50/50
  ├─ Then 20/80 (flip it!)
  └─ Finally 0/100 (fully rolled out)

If new version has issues:
  └─ Set weight to 100/0 (instant rollback!)
```

---

## ✅ Quick Verification Commands

**1. Quick 10 request test:**
```bash
for i in {1..10}; do curl -s http://arena.com:32089 | grep -o "backend-[^ ]*" | head -1; done | sort | uniq -c
```

**Expected:** ~8 backend, ~2 backend-2

**2. Live monitoring (press Ctrl+C to stop):**
```bash
while true; do 
  result=$(curl -s http://arena.com:32089 | grep -o "backend-[^ ]*" | head -1)
  echo "$(date +%H:%M:%S) - $result"
  sleep 1
done
```

You'll see backend appear 4x more often!

---

## 🔑 Key Differences from 50/50 Split

| Feature | 50/50 Split | 80/20 Weighted |
|---------|-------------|----------------|
| **Use Case** | A/B testing | Canary deployment |
| **Risk** | Medium | Low |
| **Traffic** | Equal | Controlled |
| **Backend hits** | 5 / 5 | 8 / 2 |
| **Rollback** | Delete route | Change weight |

**80/20 is SAFER** because most users stay on stable version! 🛡️
