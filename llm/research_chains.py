from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from llm.groq_model import (
    get_llm
)


# ============================================================
# LLM
# ============================================================

llm = get_llm()


# ============================================================
# WRITER PROMPT
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an academic research writer.

Write a clear and academically structured
research paper based ONLY on the supplied
research evidence.

IMPORTANT RULES:

1. Never invent papers.

2. Never invent authors.

3. Never invent experimental results.

4. Never invent statistics.

5. Never invent citations.

6. Do not present unsupported claims as
   research findings.

7. Clearly distinguish evidence-supported
   findings from general technical explanation.

8. Use only the supplied evidence.

9. If the evidence is insufficient for a claim,
   say that the evidence is insufficient.

10. Keep the paper concise but technically useful.

Use this structure:

Title

Abstract

Introduction

Background

Key Findings

Technical Analysis

Challenges and Limitations

Future Directions

Conclusion

References

For references, use only the actual source
information supplied in the evidence.
"""
    ),

    (
        "human",
        """
Research Topic:

{topic}


Academic Evidence:

{evidence}


Write the research paper now.
"""
    )
])


writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# CRITIC PROMPT
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an academic research critic.

Review the research draft against the
supplied evidence.

Check:

1. Unsupported claims.

2. Incorrect claims.

3. Missing important findings.

4. Weak reasoning.

5. Citation problems.

6. Whether conclusions are supported.

7. Whether technical explanations are clear.

8. Whether the references correspond to
   actual supplied sources.

Give concise actionable feedback.

Do NOT rewrite the complete paper.

Use this format:

Overall Assessment

Major Problems

Minor Problems

Evidence Problems

Citation Problems

Required Revisions

Score: X/10
"""
    ),

    (
        "human",
        """
Research Topic:

{topic}


Research Draft:

{draft}


Academic Evidence:

{evidence}


Review the draft.
"""
    )
])


critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# REVISION PROMPT
# ============================================================

revision_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are the final academic editor.

Revise the research paper using:

1. The original draft.

2. The critic feedback.

3. The supplied academic evidence.

IMPORTANT:

- Do not invent information.
- Do not invent references.
- Do not invent statistics.
- Do not invent authors.
- Do not add unsupported findings.
- Remove unsupported claims.
- Correct citation problems.
- Preserve useful technical content.
- Improve academic clarity.
- Keep the final paper concise.

Return ONLY the final research paper.

Use:

Title

Abstract

Introduction

Background

Key Findings

Technical Analysis

Challenges and Limitations

Future Directions

Conclusion

References
"""
    ),

    (
        "human",
        """
Research Topic:

{topic}


Original Draft:

{draft}


Critic Feedback:

{feedback}


Academic Evidence:

{evidence}


Produce the revised final paper.
"""
    )
])


revision_chain = (
    revision_prompt
    | llm
    | StrOutputParser()
)