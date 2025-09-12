"""
Constitution Retriever Tool - Retrieves relevant constitutional AI principles.
In a production environment, this would use vector embeddings and semantic search.
"""
from typing import Dict, Any
from ..constitution import CONSTITUTION

def constitution_retriever(query: str) -> str:
    """
    Retrieve relevant constitutional AI principles based on the query.
    In production, this would use vector embeddings and similarity search.
    """
    query_lower = query.lower()
    
    # Map query terms to relevant constitutional sections
    keyword_mappings = {
        "harm": ["SAFETY AND HARM PREVENTION", "HUMAN DIGNITY AND RESPECT"],
        "safety": ["SAFETY AND HARM PREVENTION"],
        "bias": ["FAIRNESS AND NON-DISCRIMINATION"],
        "discrimination": ["FAIRNESS AND NON-DISCRIMINATION", "HUMAN DIGNITY AND RESPECT"],
        "fairness": ["FAIRNESS AND NON-DISCRIMINATION"],
        "truth": ["TRUTHFULNESS AND ACCURACY"],
        "accuracy": ["TRUTHFULNESS AND ACCURACY"],
        "privacy": ["PRIVACY AND CONFIDENTIALITY"],
        "transparent": ["TRANSPARENCY AND ACCOUNTABILITY"],
        "ethical": ["BENEFICENCE AND SOCIAL GOOD", "HUMAN DIGNITY AND RESPECT"],
        "environment": ["ENVIRONMENTAL RESPONSIBILITY"],
        "dignity": ["HUMAN DIGNITY AND RESPECT"],
        "respect": ["HUMAN DIGNITY AND RESPECT"],
        "helpful": ["BENEFICENCE AND SOCIAL GOOD"],
        "beneficial": ["BENEFICENCE AND SOCIAL GOOD"]
    }
    
    # Find relevant sections based on query keywords
    relevant_sections = set()
    for keyword, sections in keyword_mappings.items():
        if keyword in query_lower:
            relevant_sections.update(sections)
    
    # If no specific keywords found, return core principles
    if not relevant_sections:
        relevant_sections = ["HUMAN DIGNITY AND RESPECT", "SAFETY AND HARM PREVENTION", "BENEFICENCE AND SOCIAL GOOD"]
    
    # Extract relevant sections from the constitution
    constitution_lines = CONSTITUTION.split('\n')
    result = "RELEVANT CONSTITUTIONAL PRINCIPLES:\n\n"
    
    current_section = None
    include_lines = False
    
    for line in constitution_lines:
        line = line.strip()
        
        # Check if this line is a section header we want
        if any(section in line for section in relevant_sections):
            current_section = line
            include_lines = True
            result += f"{line}\n"
        
        # Check if we've hit a new section we don't want
        elif line.isupper() and len(line) > 10 and current_section and not any(section in line for section in relevant_sections):
            include_lines = False
            current_section = None
        
        # Include lines if we're in a relevant section
        elif include_lines and line:
            result += f"   {line}\n"
        
        # Stop if we hit the guidelines section
        elif "Ethical Guidelines for Responses:" in line:
            break
    
    # Always include the ethical guidelines
    result += "\nETHICAL GUIDELINES FOR RESPONSES:\n"
    in_guidelines = False
    
    for line in constitution_lines:
        if "Ethical Guidelines for Responses:" in line:
            in_guidelines = True
            continue
        elif in_guidelines and line.strip().startswith('-'):
            result += f"   {line.strip()}\n"
        elif in_guidelines and line.strip() and not line.strip().startswith('-'):
            # End of guidelines section
            break
    
    return result

# Alternative function names
retrieve_constitution = constitution_retriever
get_constitutional_principles = constitution_retriever