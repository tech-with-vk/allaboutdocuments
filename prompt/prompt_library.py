from langchain_core.prompts import ChatPromptTemplate

# Prompt for document analysis
prompt_to_analyze_document_metadata = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}
""")

# format_instruction is coming from parser, combined_docs is coming from data ingestion
prompt_to_compare_documents = ChatPromptTemplate.from_template(
    """ You will be provided with content from two documents.  Your tasks are as follows:

    1. Compare the content in both documents
    2. Identify the difference in content and note down the page numbers
    3. The output you provide should be page wise comparison content
    4. If any page content is not changed, mention as "No Change"

    Input doucments:
    
    {combined_docs}

    Your response should follow the below format

    {format_instruction}
    """
)

PROMPT_REGISTRY = {
    "document_analyzer": prompt_to_analyze_document_metadata,
    "document_comparator": prompt_to_compare_documents,
}
