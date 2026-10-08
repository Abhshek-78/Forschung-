**Using Natural Language Processing Techniques in Language‑Conversion Systems: Insights from an Educational Workshop**  

*Ludovica Pannitto, Lucia Busso, Claudia Roberta Combei, Lucio Messina, Alessio Miaschi, Gabriele Sarti, Malvina Nissim*  

---  

### Abstract  
Language‑conversion tools such as machine translation and speech‑to‑text systems rely on a variety of Natural Language Processing (NLP) techniques. This paper provides a conceptual analysis of how foundational NLP concepts can be introduced to secondary‑school learners through an interactive workshop, and how the workshop’s activities relate to the components of modern language‑conversion pipelines. The analysis is based on the design and implementation details reported by Pannitto *et al.* (2021), who described a hands‑on activity set that simulates voice‑recognition, statistical language modelling with Markov chains, and syntactic parsing. We outline the pedagogical rationale of each activity, discuss its relevance to language‑conversion technology, and highlight the broader educational context in which the workshop was delivered. Limitations of the current evidence—including the absence of systematic evaluation data—are acknowledged, and directions for future empirical work are proposed.  

### 1. Introduction  
Everyday digital services—search engines, voice assistants, automatic translators, and spelling‑correction tools—embed NLP techniques that most users encounter without explicit awareness of the underlying algorithms. While the pervasiveness of these tools is well documented, formal education at the secondary‑school level often omits systematic instruction in computational linguistics and related computer‑science topics (Pannitto *et al.*, 2021). Consequently, students may lack the conceptual vocabulary needed to engage critically with language‑conversion technologies or to consider computational linguistics as a viable university pathway.  

This paper examines how an activity‑driven workshop can introduce core NLP ideas to high‑school students and how those ideas map onto the functional blocks of contemporary language‑conversion systems. By analysing the workshop described by Pannitto *et al.* (2021), we aim to (i) clarify the educational objectives of the activities, (ii) situate the activities within the broader landscape of language‑conversion pipelines, and (iii) identify gaps that future research should address.  

### 2. Background  

#### 2.1. NLP in the Italian High‑School Curriculum  
Pannitto *et al.* (2021) report that Italian secondary‑school curricula traditionally overlook “young disciplines” such as linguistics and computer science, resulting in limited exposure to NLP and its applications. Students frequently interact with NLP‑driven services (e.g., Google search, voice assistants, spam filters) yet remain unaware of the computational mechanisms that enable these services (p. 1).  

#### 2.2. The Workshop as a Dissemination Activity  
The authors, members of the Italian Association for Computational Linguistics (AILC), designed an interactive workshop to bridge this knowledge gap. The workshop is described as the first activity of its kind promoted by AILC and, to the authors’ knowledge, among the earliest such initiatives in Italy (p. 2). It was delivered at “numerous outlets in Italy between 2019 and 2021, both face‑to‑face and online” (p. 2). The workshop adopts a game‑based format in which participants assume the role of a machine tasked with solving three prototypical NLP problems:

1. **Voice recognition** – a simplified simulation of converting spoken input into text.  
2. **Statistical language modelling with Markov chains** – an activity that illustrates how word‑sequence probabilities can be estimated.  
3. **Syntactic parsing** – a hands‑on exercise that reveals how grammatical structure can be extracted from sentences.  

These activities are intended to make abstract computational concepts tangible for learners aged 13–18.  

### 3. Pedagogical Activities and Their Relation to Language‑Conversion Systems  

| Activity | Description (as reported) | Conceptual link to language‑conversion pipelines |
|----------|---------------------------|---------------------------------------------------|
| **Voice‑recognition simulation** | Students act as “machines” that must map an oral utterance onto a textual representation, using cues such as phonetic similarity and contextual hints. | Illustrates the first stage of speech‑to‑text converters, where acoustic signals are transformed into a textual hypothesis. |
| **Markov‑chain language modelling** | Participants construct simple probabilistic tables that predict the next word given the previous one, thereby experiencing the mechanics of statistical sequence prediction. | Demonstrates the idea of language modelling, a component that underlies both speech synthesis and