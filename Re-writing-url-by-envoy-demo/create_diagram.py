from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Envoy
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.compute import Pod
from diagrams.generic.device import Mobile

with Diagram("Hostname Rewrite Flow", filename="/home/dom/K8-abhishek-veeramalla/learned-topics/K8-Gate-way-API/kubernetes-gateway-api/02-url-rewrite/hostname-rewrite-flow", show=False, direction="TB"):
    
    user = Mobile("User Browser\nTypes:\nhouse-of-batiatis.com:32089")
    
    with Cluster("envoy-gateway-system namespace"):
        gateway_svc = Service("Gateway Service\nNodePort: 32089")
        envoy = Envoy("Envoy Proxy Pod\nRewrites Hostname")
    
    with Cluster("default namespace"):
        httproute = Ingress("HTTPRoute\nhost-of-batiatis.com\n↓ REWRITE ↓\nhouse-of-ashur.com")
        
        backend_svc = Service("backend:80")
        backend_pod = Pod("backend-8gkmk\nReceives:\nHost: house-of-ashur.com")
    
    # Traffic flow with rewrite
    user >> Edge(label="1. Request\nHost: house-of-batiatis.com", color="blue") >> gateway_svc
    gateway_svc >> Edge(label="2. Forward") >> envoy
    envoy >> Edge(label="3. Check Rules") >> httproute
    httproute >> Edge(label="4. REWRITTEN Request\nHost: house-of-ashur.com", color="red") >> backend_svc >> backend_pod
    
    # Response
    backend_pod >> Edge(label="5. Response", style="dashed") >> user
