import pandas as pd
import streamlit as st

from medibench.benchmarks.ground_truth import RETIRED_QUESTIONS_REGISTRY
from medibench.database import BenchmarkQuestion, SessionLocal

st.set_page_config(page_title="Benchmark Explorer | MediBench", page_icon="🎯", layout="wide")

st.title("🎯 Healthcare Benchmark Explorer")
st.caption("60 Verified Benchmark Questions with Deterministic Ground-Truth Answers")

db = SessionLocal()
try:
    questions = db.query(BenchmarkQuestion).all()

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Questions", len(questions))
    c2.metric("Categories", len(set(q.category for q in questions)))
    c3.metric("Verified Ground Truth", "100%", delta="Deterministic")
    c4.metric("Retired Questions", len(RETIRED_QUESTIONS_REGISTRY))

    st.markdown("---")

    view_mode = st.radio("Select View", ["Active Benchmarks (60)", "Retired Questions Registry (3)"], horizontal=True)

    if view_mode == "Active Benchmarks (60)":
        # Filters
        f1, f2, f3 = st.columns(3)
        with f1:
            categories = ["All"] + sorted(list(set(q.category for q in questions)))
            sel_cat = st.selectbox("Filter by Category", categories)
        with f2:
            difficulties = ["All"] + sorted(list(set(q.difficulty for q in questions)))
            sel_diff = st.selectbox("Filter by Difficulty", difficulties)
        with f3:
            freshness = ["All"] + sorted(list(set(q.freshness_category for q in questions)))
            sel_fresh = st.selectbox("Filter by Freshness", freshness)

        filtered = questions
        if sel_cat != "All":
            filtered = [q for q in filtered if q.category == sel_cat]
        if sel_diff != "All":
            filtered = [q for q in filtered if q.difficulty == sel_diff]
        if sel_fresh != "All":
            filtered = [q for q in filtered if q.freshness_category == sel_fresh]

        st.caption(f"Displaying {len(filtered)} of {len(questions)} questions")

        table_data = []
        for q in filtered:
            ans = q.answers[0] if q.answers else None
            table_data.append({
                "ID": q.id,
                "Category": q.category,
                "Difficulty": q.difficulty,
                "Question": q.question,
                "Method": q.evaluation_method,
                "Ground Truth": ans.expected_answer if ans else None,
                "Freshness": q.freshness_category,
            })

        df_bench = pd.DataFrame(table_data)
        st.dataframe(df_bench, use_container_width=True)

        st.markdown("### Question Inspector")
        q_ids = [q.id for q in filtered]
        if q_ids:
            selected_qid = st.selectbox("Inspect Question Details", q_ids)
            selected_q = next(q for q in filtered if q.id == selected_qid)
            ans = selected_q.answers[0] if selected_q.answers else None

            st.json({
                "id": selected_q.id,
                "category": selected_q.category,
                "difficulty": selected_q.difficulty,
                "question": selected_q.question,
                "dataset_version": selected_q.dataset_version,
                "reference_solution": selected_q.reference_solution,
                "evaluation_method": selected_q.evaluation_method,
                "tolerance": selected_q.tolerance,
                "freshness_category": selected_q.freshness_category,
                "status": selected_q.status,
                "verified_ground_truth": {
                    "expected_answer": ans.expected_answer if ans else None,
                    "answer_type": ans.answer_type if ans else None,
                    "verification_hash": ans.verification_hash if ans else None,
                    "notes": ans.verification_notes if ans else None,
                },
            })

    else:
        st.subheader("Feature 1: Retired Question Registry")
        st.markdown("""
        Documenting questions retired due to institutional data quality limits or domain expert review.
        """)
        ret_data = []
        for r in RETIRED_QUESTIONS_REGISTRY:
            ret_data.append({
                "Question ID": r.question_id,
                "Original Question": r.original_question,
                "Reason for Retirement": r.reason_for_retirement,
                "Data Owner Feedback": r.data_owner_feedback,
                "Replacement ID": r.replacement_question_id,
                "Review Date": r.review_date,
                "Status": r.status,
            })
        st.dataframe(pd.DataFrame(ret_data), use_container_width=True)

finally:
    db.close()
