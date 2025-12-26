from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Envoy
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.compute import Pod
from diagrams.generic.device import Mobile

with Diagram("Weighted Traffic Routing (80/20)", filename="/home/dom/K8-abhishek-veeramalla/learned-topics/K8-Gate-way-API/kubernetes-gateway-api/04-weighted/weighted-routing-flow", show=False, direction="TB"):
    
    user = Mobile("User Browser\narena.com:32089\n10 Requests")
    
    with Cluster("envoy-gateway-system namespace"):
        gateway_svc = Service("Gateway Service\nNodePort: 32089")
        envoy = Envoy("Envoy Proxy Pod\nReads HTTPRoute\n80/20 Weight")
    
    with Cluster("default namespace"):
        httproute = Ingress("HTTPRoute\narena.com\nWeight: 8:2")
        
        with Cluster("Backend Services"):
            backend_svc = Service("backend:80\nWeight: 8")
            backend2_svc = Service("backend-2:80\nWeight: 2")
        
        with Cluster("Backend Pods"):
            backend_pod = Pod("backend-8gkmk\n(Stable Version)\n8 requests")
            backend2_pod = Pod("backend-2-g8d6c\n(Canary Version)\n2 requests")
    
    # Traffic flow
    user >> Edge(label="1. HTTP Request") >> gateway_svc
    gateway_svc >> Edge(label="2. Forward") >> envoy
    envoy >> Edge(label="3. Check Rules") >> httproute
    
    # Weighted traffic
    httproute >> Edge(label="4. 80% traffic\n(8 out of 10)", color="green", penwidth="3") >> backend_svc >> backend_pod
    httproute >> Edge(label="4. 20% traffic\n(2 out of 10)", color="orange", penwidth="1.5") >> backend2_svc >> backend2_pod
    
    # Responses
    backend_pod >> Edge(label="5. Response", color="green", style="dashed") >> user
    backend2_pod >> Edge(label="5. Response", color="orange", style="dashed") >> user
