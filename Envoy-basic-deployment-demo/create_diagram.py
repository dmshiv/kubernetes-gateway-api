#!/usr/bin/env python3
"""
Gateway API Flow - Visual Diagram
Shows how traffic flows through Gateway API components
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.controlplane import APIServer
from diagrams.onprem.client import User

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
}

with Diagram(
    "Scenario 1: Basic Gateway API Flow",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    filename="01-basic-deploy-flow"
):
    
    user = User("Browser\nspartacus.com:30080")
    
    with Cluster("envoy-gateway-system namespace"):
        gateway_svc = Service("Gateway Service\n(NodePort 30080)")
    
    with Cluster("default namespace"):
        with Cluster("Gateway Components"):
            gateway_class = APIServer("GatewayClass\n(eg)\nUse Envoy")
            gateway = Ingress("Gateway\n(eg)\nPort 80")
            httproute = APIServer("HTTPRoute\nspartacus.com\n→ backend:80")
            envoy_pod = Pod("Envoy Proxy Pod\n(Auto-created)")
        
        with Cluster("Your Application"):
            backend_svc = Service("Service\nbackend:80")
            backend_deploy = Deployment("Deployment\nbackend")
            backend_pod = Pod("Pod\nnginxdemos/hello")
    
    # Traffic flow
    user >> Edge(label="1. HTTP Request", color="blue") >> gateway_svc
    gateway_svc >> Edge(label="2. Forward", color="blue") >> envoy_pod
    envoy_pod >> Edge(label="3. Check rules", color="orange") >> httproute
    httproute >> Edge(label="4. Route to", color="orange") >> backend_svc
    backend_svc >> Edge(label="5. Load balance", color="green") >> backend_pod
    
    # Management relationships
    gateway_class >> Edge(label="defines", style="dashed", color="gray") >> gateway
    gateway >> Edge(label="creates", style="dashed", color="gray") >> envoy_pod
    gateway >> Edge(label="creates", style="dashed", color="gray") >> gateway_svc
    backend_deploy >> Edge(label="manages", style="dashed", color="gray") >> backend_pod

print("✅ Diagram generated!")
print("📁 Output: 01-basic-deploy-flow.png")
print("\nTo view:")
print("  xdg-open 01-basic-deploy-flow.png")
print("  # or")
print("  open 01-basic-deploy-flow.png")
