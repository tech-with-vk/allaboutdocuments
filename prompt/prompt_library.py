# === LangChain Core Prompt Templates ===
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

# --------------------------------------------
# Prompt for analyzing and summarizing a single document's metadata.
# This prompt expects a valid JSON response conforming to the schema defined by the parser.
# Used in DocumentMetadataAnalyzer.
# --------------------------------------------
prompt_to_analyze_document_metadata = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}
""")

# --------------------------------------------
# Prompt for comparing two documents.
# - It performs a page-wise comparison.
# - If no change is found on a page, it must return "No Change".
# - The format of output must match what the parser instructs via `format_instruction`.
# `combined_docs` is constructed from text content of both PDFs.
# --------------------------------------------
prompt_to_compare_documents = ChatPromptTemplate.from_template("""
You will be provided with content from two documents. Your tasks are as follows:

1. Compare the content in both documents.
2. Identify the difference in content and note down the page numbers.
3. The output you provide should be page-wise comparison content.
4. If any page content is not changed, mention as "No Change".

Input documents:

{combined_docs}

Your response should follow the below format:

{format_instruction}
""")

# --------------------------------------------
# Prompt for rewriting a question in a standalone format using chat history.
# - Used in conversational RAG to ensure the current user query makes sense independently.
# - MessagesPlaceholder dynamically injects prior history during runtime.
# --------------------------------------------
prompt_to_contextualize_question = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Given a conversation history and the most recent user query, rewrite the query as a standalone question "
                "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
                "question if necessary; otherwise, return it unchanged."
            ),
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# --------------------------------------------
# Prompt for answering a user question using only the provided context.
# - If the context does not contain the answer, the assistant must say "I don't know."
# - The response must be short (≤3 sentences).
# --------------------------------------------
prompt_to_context_qa = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an assistant designed to answer questions using the provided context. Rely only on the retrieved "
                "information to form your response. If the answer is not found in the context, respond with 'I don't know.' "
                "Keep your answer concise and no longer than three sentences.\n\n{context}"
            ),
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# --------------------------------------------
# Prompt registry for convenient access across the application.
# Keys are used by modules such as the document analyzer, comparator, and RAG pipeline.
# --------------------------------------------
PROMPT_REGISTRY = {
    "document_analyzer": prompt_to_analyze_document_metadata,
    "document_comparator": prompt_to_compare_documents,
    "contextualize_question": prompt_to_contextualize_question,
    "context_qa": prompt_to_context_qa,
}
