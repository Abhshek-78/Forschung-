**Title**  
Minimizing Neural‑Network Footprint in Containerized Environments: A Synthesis of Workflow‑Containerization Insights and Model‑Compression Techniques  

---

**Abstract**  
Container orchestration platforms such as Kubernetes (K8s) enable portable deployment of machine‑learning (ML) workloads, yet the combined overhead of container images, runtime libraries, and scheduler behavior can obscure the benefits of neural‑network (NN) compression (pruning, quantization, knowledge distillation, etc.). This paper integrates the limited evidence on workflow containerization—principally the *KubeAdaptor* framework—with the extensive literature on NN size‑reduction and container‑image optimization. We (i) summarize the characteristics of the K8s scheduler that affect deterministic execution, (ii) review established NN‑compression methods and container‑image minimization practices, (iii) identify concrete gaps where container scheduling may interfere with compression‑aware deployment, and (iv) outline an experimental agenda to quantify image‑size, memory, and latency impacts. The analysis clarifies that while existing workflow‑container research does not directly address NN minimization, its observations about two‑level scheduling and scheduler unpredictability constitute a useful foundation for future work on container‑aware model compression.

---

### 1. Introduction  

Deploying NN models inside containers has become the de‑facto strategy for reproducible ML services. Containerization isolates dependencies, while orchestration systems such as Kubernetes provide