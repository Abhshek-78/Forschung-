**Title**  
Implications of Changing Data Sources for Machine Learning in Official Statistics: Considerations for Japanese Encephalitis Virus (JEV) Surveillance  

---

**Abstract**  
Machine learning (ML) is increasingly integrated into the production of official statistics, offering more timely and granular information than traditional survey‑based approaches. A central vulnerability of ML‑driven statistical systems is the inevitability of data‑source changes, which can induce concept drift, bias, and loss of continuity. Drawing on the systematic review by De Boom and Reusens (2023), this paper summarises the identified risks, the dimensions of change, and the precautionary measures recommended for official statistics. Although no empirical JEV‑specific studies are available in the source material, the general findings are extrapolated to illustrate how they may affect ML‑based JEV surveillance and forecasting. The paper concludes with concise recommendations for statistical agencies and public‑health institutions that seek to harness ML while preserving data integrity.

---

### 1. Introduction  
The production of official statistics has traditionally relied on censuses and sample surveys. Recent advances in data science have enabled the incorporation of ML techniques, promising faster, richer, and more cost‑effective statistical outputs (De Boom & Reusens, 2023). In the public‑health arena, such capabilities are attractive for monitoring infectious diseases, including Japanese Encephalitis Virus (JEV). However, the reliability of ML‑derived estimates depends critically on the stability and quality of the underlying data streams. This paper reviews the evidence on data‑source volatility in official statistics and discusses its relevance for ML‑based JEV surveillance, explicitly acknowledging that the linkage is an extrapolation rather than a result of empirical JEV research.

---

### 2. Background  
De Boom and Reusens (2023) provide a comprehensive overview of the risks that arise when data sources evolve in the context of ML for official statistics. Their analysis distinguishes four broad dimensions of change:

| Dimension | Description |
|-----------|-------------|
| **Technical** | Modifications to data formats, granularity, collection methods, or underlying technologies (e.g., API updates, sensor‑network revisions). |
| **Ownership** | Shifts in who controls the data, affecting access rights and licensing conditions. |
| **Ethical/Regulatory** | New privacy constraints, legal frameworks, or compliance requirements. |
| **Public Perception** | Changes in trust, acceptance, or perceived legitimacy of the data source. |

These dimensions can trigger statistical issues such as **concept drift** (the statistical relationship between predictors and target changes), **bias introduction**, reduced **accuracy and validity**, and potential **discontinuation** of statistical series. The authors also highlight two methodological opportunities that are particularly relevant for official statistics:

* **Unsupervised learning** – can uncover hidden similarities among entities (e.g., citizens,