# Steps to deploy Gateway with custom NodePort

# 1. Apply Gateway resources
kubectl apply -f gateway_class.yaml
kubectl apply -f gateway.yaml
kubectl apply -f svc_account.yaml
kubectl apply -f deploy.yaml
kubectl apply -f svc.yaml
kubectl apply -f httproute.yaml

# 2. Wait for Gateway service to be created (takes ~30 seconds)
sleep 30

# 3. Apply NodePort patch to use port 30080 instead of random port
kubectl apply -f gateway-nodeport-patch.yaml

<!-- You can't set the NodePort directly in the Gateway YAML because the service is created automatically by Envoy Gateway controller. But I can create a patch file you can apply: -->

# 4. Verify
kubectl get svc -n envoy-gateway-system

# 5. Access app
# Add to /etc/hosts: 127.0.0.1 spartacus.com
curl http://spartacus.com:30080
# Or browser: http://spartacus.com:30080
