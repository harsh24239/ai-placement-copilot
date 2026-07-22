from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END

from tools.pdf_reader import extract_text_from_pdf
from agents.resume.agent import analyze_resume
from agents.job_description.agent import analyze_jd
from agents.skill_gap.agent import analyze_skill_gap


class PlacementState(TypedDict):
    resume_bytes: bytes
    jd_bytes: bytes
    resume_text: Optional[str]
    jd_text: Optional[str]
    resume_analysis: Optional[dict]
    jd_analysis: Optional[dict]
    skill_gap: Optional[dict]


def extract_resume_node(state: PlacementState) -> dict:
    text = extract_text_from_pdf(state["resume_bytes"])
    return {"resume_text": text}


def extract_jd_node(state: PlacementState) -> dict:
    text = extract_text_from_pdf(state["jd_bytes"])
    return {"jd_text": text}


def resume_agent_node(state: PlacementState) -> dict:
    analysis = analyze_resume(state["resume_text"])
    return {"resume_analysis": analysis}


def jd_agent_node(state: PlacementState) -> dict:
    analysis = analyze_jd(state["jd_text"])
    return {"jd_analysis": analysis}


def skill_gap_node(state: PlacementState) -> dict:
    gap = analyze_skill_gap(
        resume_skills=state["resume_analysis"]["skills_found"],
        jd_technical_skills=state["jd_analysis"]["technical_skills"],
        jd_soft_skills=state["jd_analysis"]["soft_skills"]
    )
    return {"skill_gap": gap}


# Build the graph
graph_builder = StateGraph(PlacementState)

graph_builder.add_node("extract_resume", extract_resume_node)
graph_builder.add_node("extract_jd", extract_jd_node)
graph_builder.add_node("resume_agent", resume_agent_node)
graph_builder.add_node("jd_agent", jd_agent_node)
graph_builder.add_node("skill_gap", skill_gap_node)

graph_builder.add_edge(START, "extract_resume")
graph_builder.add_edge(START, "extract_jd")
graph_builder.add_edge("extract_resume", "resume_agent")
graph_builder.add_edge("extract_jd", "jd_agent")
graph_builder.add_edge("resume_agent", "skill_gap")
graph_builder.add_edge("jd_agent", "skill_gap")
graph_builder.add_edge("skill_gap", END)

placement_graph = graph_builder.compile()
