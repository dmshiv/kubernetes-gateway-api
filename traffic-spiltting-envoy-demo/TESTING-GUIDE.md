# Traffic Splitting - Quick Testing Guide

## 📊 See the Diagram
Open: `traffic-splitting-flow.png`

---

## 🧪 Test 1: Terminal (See the Split)

Run 10 requests and see which backend responds:
```bash
for i in {1..10}; do 
  echo -n "Request $i: "
  curl -s http://gladiators.com:32089 | grep "Server&nbsp;name:" | grep -o "backend[^<]*"
done
```

**Expected Result:**
```
Request 1: backend-7f64676864-8gkmk    ← Version 1
Request 2: backend-2-7b5d6b96dc-g8d6c  ← Version 2
Request 3: backend-7f64676864-8gkmk    ← Version 1
Request 4: backend-2-7b5d6b96dc-g8d6c  ← Version 2
...
```

✅ **Success:** You see BOTH backend names appearing randomly!

---

## 🌐 Test 2: Browser (Visual Test)

1. **Open browser:** `http://gladiators.com:32089`

2. **Look for this line:**
   ```
   Server name: backend-7f64676864-8gkmk
   ```

3. **Press F5 to refresh** (or Ctrl+R)

4. **Check the Server name again** - it might change to:
   ```
   Server name: backend-2-7b5d6b96dc-g8d6c
   ```

5. **Keep refreshing 5-10 times** - You'll see it alternate!

✅ **Success:** Server name changes between refreshes!

---

## 📈 Test 3: Count Distribution

Send 20 requests and count hits per backend:
```bash
for i in {1..20}; do 
  curl -s http://gladiators.com:32089 | grep "Server&nbsp;name:" | grep -o "backend[^<]*"
done | sort | uniq -c
```

**Expected Result:**
```
  10 backend-7f64676864-8gkmk     ← ~50% hits
  10 backend-2-7b5d6b96dc-g8d6c   ← ~50% hits
```

✅ **Success:** Both backends get roughly equal hits!

---

## 🎯 What You're Testing

```
User Request → Gateway → Envoy Proxy
                            ↓
                    [50/50 Split]
                      ↙        ↘
              Backend Pod   Backend-2 Pod
              (Version 1)   (Version 2)
```

**Each request randomly goes to one of two pods!**

---

## ✅ Quick Verification

Run this single command to see the split:
```bash
for i in {1..5}; do curl -s http://gladiators.com:32089 | grep -o "backend-[^ ]*" | head -1; done
```

You should see different pod names!
