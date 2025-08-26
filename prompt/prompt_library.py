from langchain_core.prompts import ChatPromptTemplate

# Prompt for document analysis
prompt_to_analyze_document_metadata = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}
""")
