from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Envoy
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.compute import Pod
from diagrams.generic.device import Mobile

with Diagram("Traffic Splitting Flow", filename="/home/dom/K8-abhishek-veeramalla/learned-topics/K8-Gate-way-API/kubernetes-gateway-api/03-traffic-spiltting/traffic-splitting-flow", show=False, direction="TB"):
    
    user = Mobile("User Browser\ngladiators.com:32089")
    
    with Cluster("envoy-gateway-system namespace"):
        gateway_svc = Service("Gateway Service\nNodePort: 32089")
        envoy = Envoy("Envoy Proxy Pod\nReads HTTPRoute\n50/50 Split")
    
    with Cluster("default namespace"):
        httproute = Ingress("HTTPRoute\ngladiators.com\nSplit: 50/50")
        
        with Cluster("Backend Services"):
            backend_svc = Service("backend:80")
            backend2_svc = Service("backend-2:80")
        
        with Cluster("Backend Pods"):
            backend_pod = Pod("backend-8gkmk\n(Version 1)")
            backend2_pod = Pod("backend-2-g8d6c\n(Version 2)")
    
    # Traffic flow
    user >> Edge(label="1. HTTP Request") >> gateway_svc
    gateway_svc >> Edge(label="2. Forward") >> envoy
    envoy >> Edge(label="3. Check Rules") >> httproute
    
    # Split traffic
    httproute >> Edge(label="4. 50% traffic", color="green") >> backend_svc >> backend_pod
    httproute >> Edge(label="4. 50% traffic", color="blue") >> backend2_svc >> backend2_pod
    
    # Responses
    backend_pod >> Edge(label="5. Response", color="green", style="dashed") >> user
    backend2_pod >> Edge(label="5. Response", color="blue", style="dashed") >> user
