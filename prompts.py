from langchain.prompts import PromptTemplate

prompts = {
    "case_brief": PromptTemplate.from_template(
        """Based on the context below, generate a comprehensive case brief containing:
        - Facts: The essential factual background leading to the dispute.
        - Issues: The specific legal questions or points of contention the court addressed.
        - Point of Law: The primary legal principle(s) or statute(s) applied by the court.
        - Analysis with reasoning and precedents: A detailed explanation of the court's legal reasoning, how it applied the law to the facts, and its reliance on cited precedents.
        - Conclusion: The final decision or outcome of the case.

        Ensure the brief is concise yet covers all critical elements.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "facts_extraction": PromptTemplate.from_template(
        """From the provided legal context, accurately identify and summarize the key facts of the case.
        Present them clearly and concisely, focusing only on the factual background that led to the legal dispute.
        Do not include legal analysis or the court's decision.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "reasoning": PromptTemplate.from_template(
        """Read the judgment carefully and explain the court's complete reasoning for its final decision.
        Detail the legal logic, principles, and precedents the court relied upon to reach its conclusion.

        Context:
        {context}

        Question:
        {question}
        """
    ),

    "decision_check": PromptTemplate.from_template(
        """Based on the provided legal context, clearly state the final decision regarding the appellant/parties involved.
        Was the appellant granted bail, acquitted, convicted, or was any other specific relief granted or denied?
        Quote the exact portion from the judgment that states the decision if possible.

        Context:
        {context}

        Question:
        {question}
        """
    ),

    "citations_list": PromptTemplate.from_template(
        """From the provided legal context, identify and list all distinct legal citations mentioned.
        Include cases (e.g., 'Mohd. Ahmed Khan v. Shah Bano Begum'), specific sections of Acts (e.g., 'Section 125 of CrPC'), and constitutional articles (e.g., 'Article 21 of the Constitution').
        List each citation clearly.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "extraction": PromptTemplate.from_template(
        """Extract all key legal sections, acts, or provisions that are central to the court's judgment or reasoning, beyond just explicit citations.
        Focus on the substantive legal references directly discussed or applied.

        Context:
        {context}

        Question:
        {question}
        """
    ),

    # --- Newly Added Prompts ---

    "procedural_history": PromptTemplate.from_template(
        """Outline the procedural history of this case based on the provided legal context.
        Describe the key stages the case went through in the legal system, including decisions at each court level, appeals, or remands.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "legal_definition": PromptTemplate.from_template(
        """Based on the provided legal context, define the legal term or concept mentioned in the user's question.
        Explain its meaning and how it is applied or discussed within this specific judgment.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "statutory_interpretation": PromptTemplate.from_template(
        """Explain how the court has interpreted or applied the specific statute, section, or legal provision mentioned in the user's question, based on the provided legal context.
        Detail any specific nuances, clarifications, or rulings provided by the court regarding its meaning and application.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "dissenting_opinion_summary": PromptTemplate.from_template(
        """If the provided legal context contains any dissenting or concurring opinions, summarize the key arguments or points of disagreement/agreement presented by the dissenting/concurring judge(s).
        If no such opinions are present, state so.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "case_implications": PromptTemplate.from_template(
        """Based on the court's decision and reasoning in the provided legal context, analyze and describe the key legal implications or potential impacts of this judgment.
        Consider how it might affect future cases, the interpretation of the law, or legal practice.

        Context:
        {context}

        User Question:
        {question}
        """
    ),

    "general": PromptTemplate.from_template(
        """You are an expert legal researcher and assistant. Use the following legal context to answer the question in depth.
        Ensure your answer is accurate, comprehensive, and directly supported by the provided text.
        If the context does not contain enough information, state that clearly.

        Context:
        {context}

        Question:
        {question}
        """
    )
}