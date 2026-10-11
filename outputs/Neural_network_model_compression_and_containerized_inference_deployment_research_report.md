**Title**  
Random Neural Networks for Supervised Learning: Training Algorithms, a Time‑Series Case Study, and Open Questions for Model Compression and Containerised Inference  

---

**Abstract**  
Random Neural Networks (RNNs) are stochastic neural models that admit a product‑form stationary distribution and can be trained with gradient‑based and second‑order optimisation methods. This review summarises the empirically verified contributions of Basterrech and Rubino (2016), focusing on (i) the learning algorithms for supervised tasks, (ii) the Echo State Queuing Network (ESQN) application to 5‑minute Internet‑traffic forecasting, and (iii) the theoretical link between queuing theory and neural computation. The source material does not address model‑size reduction or containerised deployment. Consequently, we delineate the current evidence gap, relate it to established compression techniques (e.g., filter distillation; Molchanov et al., 2018), and outline concrete research directions for compressing RNNs and deploying them in containerised environments.

---

### 1. Introduction  
Deploying neural‑network services on edge devices or in cloud‑native platforms requires (a) compact models that meet memory and latency constraints and (b) reproducible inference pipelines encapsulated in containers (e.g., Docker, Kubernetes). While extensive literature exists for conventional deep‑learning architectures, the specific case of Random Neural Networks remains under‑explored. This paper extracts the verifiable findings from the tutorial by Basterrech and Rubino (2016) and uses them as a factual foundation to (i) assess the readiness of RNNs for compression and containerised inference, and (ii) propose a research agenda that bridges the identified gaps.

---

### 2. Background  

| Concept | Description | Evidence |
|---------|-------------|----------|
| **Random Neural Networks (RNNs)** | Stochastic neurons exchange excitatory and inhibitory spikes; the network admits a product‑form stationary distribution (Basterrech & Rubino, 2016, p. 2). | Basterrech & Rubino, 2016 |
| **Supervised learning algorithms** | The tutorial presents first‑order (gradient descent) and second‑order (Newton‑type) optimisation schemes adapted from classical neural‑network training (Basterrech & Rubino, 2016, §§ 3–4). | Basterrech & Rubino, 2016 |
| **Echo State Queuing Network (ESQN)** | An RNN variant that combines echo‑state dynamics with queuing‑theoretic spike processing; used for time‑series prediction (Basterrech & Rubino, 2016, p. 30). | Basterrech & Rubino, 2016 |
| **Model‑compression techniques (general)** | Filter distillation reduces convolutional filters by learning a compact representation of the original network’s output tensors (Molchanov *et al.*, 2018, p. 2). | Molchanov *et al.*, 2018 |
| **Containerised inference** | Packaging inference code and its dependencies into lightweight containers enables