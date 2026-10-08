from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm.groq_model import get_llm


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = get_llm()


# ---------------------------------------------------------
# WRITER PROMPT
# ---------------------------------------------------------

writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert academic research writer.

Your job is to write a rigorous research paper using ONLY
the academic evidence supplied by the research system.

Important rules:

1. Do not invent research findings.
2. Do not invent papers or sources.
3. Do not make unsupported claims.
4. Prefer information directly supported by the evidence.
5. When making a claim, preserve the relationship between
   the claim and its source paper.
6. Use professional academic language.
7. Clearly distinguish established findings from observations.
8. Do not mention that you are an AI.
9. Do not discuss the internal pipeline.
10. Use the supplied paper metadata and URLs when creating
    the references.

Structure the paper as:

# Title

## Abstract

## 1. Introduction

## 2. Background

## 3. Key Findings

## 4. Technical Analysis

## 5. Comparison and Discussion

## 6. Challenges and Limitations

## 7. Future Directions

## 8. Conclusion

## References

The final paper should be detailed, coherent and academically
written.
""",
        ),
        (
            "human",
            """
Research Topic:

{topic}


Academic Evidence:

{evidence}


Write the research paper now.
""",
        ),
    ]
)


writer_chain = writer_prompt | llm | StrOutputParser()


# ---------------------------------------------------------
# CRITIC PROMPT
# ---------------------------------------------------------

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a strict academic research reviewer.

Review the research draft against the supplied academic
evidence.

Your job is NOT to rewrite the paper.

Identify:

1. Unsupported claims
2. Claims that appear stronger than the evidence
3. Missing important findings
4. Incorrect or weak source attribution
5. Logical inconsistencies
6. Repetition
7. Structural problems
8. Technical inaccuracies
9. Missing limitations
10. Problems in the references

Be specific.

For every important criticism, explain what should be
changed.

Give an overall score from 1 to 10.

Use this structure:

# Academic Review

## Overall Score

Score: X/10

## Strengths

- ...

## Critical Problems

- ...

## Evidence Problems

- ...

## Missing Information

- ...

## Structural Problems

- ...

## Recommended Changes

- ...

## Final Verdict
""",
        ),
        (
            "human",
            """
Research Topic:

{topic}


Academic Evidence:

{evidence}


Research Draft:

{draft}


Review this research draft carefully.
""",
        ),
    ]
)


critic_chain = critic_prompt | llm | StrOutputParser()


# ---------------------------------------------------------
# REVISION PROMPT
# ---------------------------------------------------------

revision_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a senior academic researcher revising a research
paper after peer review.

Rewrite the research paper using:

1. The original research draft
2. The critic's feedback
3. The original academic evidence

Rules:

- Correct unsupported claims.
- Do not invent information.
- Do not add facts that are absent from the evidence.
- Preserve accurate findings from the original draft.
- Improve academic structure.
- Improve clarity and logical flow.
- Remove unnecessary repetition.
- Strengthen source attribution.
- Keep references connected to the supplied papers.
- Include limitations.
- Make the final paper professional and publication-style.

Return ONLY the revised research paper.
Do not discuss the revision process.
""",
        ),
        (
            "human",
            """
Research Topic:

{topic}


Academic Evidence:

{evidence}


Original Research Draft:

{draft}


Critic Feedback:

{critique}


Produce the final revised research paper.
""",
        ),
    ]
)


revision_chain = revision_prompt | llm | StrOutputParser()