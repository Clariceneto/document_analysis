from crewai_tools import tool

@tool
def analyze_page(page_text, doc_type):
    """
    Analyze the given page text based on the document type.

    Args:
        page_text (str): The text content of the page.
        doc_type (str): The type of the document (e.g., relatório, artigo, contrato).

    Returns:
        dict: The analysis result of the page including critique, suggestions, and improvements.
    """
    if doc_type == "relatório":
        analysis = f"Analysis for relatório: {page_text[:500]}"
        critique = "The content is detailed but lacks bullet points for key findings."
        suggestions = "Improve clarity and structure. Use bullet points for key findings."
        improvements = "Consider adding a summary at the end of the page."
    elif doc_type == "artigo":
        analysis = f"Analysis for artigo: {page_text[:500]}"
        critique = "The arguments are clear, but the references could be more robust."
        suggestions = "Enhance argument clarity and strengthen references."
        improvements = "Add more recent studies to support your claims."
    elif doc_type == "contrato":
        analysis = f"Analysis for contrato: {page_text[:500]}"
        critique = "The language is precise but could be more concise."
        suggestions = "Identify ambiguities and improve wording for precision."
        improvements = "Use simpler terms where possible to avoid misunderstandings."
    else:
        analysis = f"General analysis: {page_text[:500]}"
        critique = "The content is informative but lacks a clear structure."
        suggestions = "Provide clear structure and improve readability."
        improvements = "Add headings and subheadings to organize the content."

    return {
        "analysis": analysis,
        "critique": critique,
        "suggestions": suggestions,
        "improvements": improvements
    }

@tool
def suggest_contextual_improvements(page_text):
    """
    Provide contextual improvements based on the page content.

    Args:
        page_text (str): The text content of the page.

    Returns:
        str: Contextual improvement suggestions.
    """
    improvements = []
    if "meeting" in page_text.lower():
        improvements.append("Consider summarizing key points discussed in the meeting.")
    if "report" in page_text.lower():
        improvements.append("Include a conclusion section to summarize the findings.")
    if "contract" in page_text.lower():
        improvements.append("Ensure that all terms are clearly defined and unambiguous.")
    
    return "\n".join(improvements)
