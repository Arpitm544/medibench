import pandas as pd
import streamlit as st

from medibench.database import EvaluationResult, EvaluationRun, SessionLocal
from medibench.evaluation.model_client import ModelClient
from medibench.evaluation.runner import EvaluationRunner

st.set_page_config(page_title="AI Model Evaluations | MediBench", page_icon="🤖", layout="wide")

st.title("🤖 AI Model Benchmark Evaluations")
st.caption("Scoring AI Models Against Deterministic Healthcare Ground Truth")

db = SessionLocal()
try:
    runs = db.query(EvaluationRun).order_by(EvaluationRun.started_at.desc()).all()

    st.subheader("Completed Evaluation Runs")
    if runs:
        run_data = []
        for r in runs:
            run_data.append({
                "Run ID": r.id,
                "Model Name": r.model_name,
                "Score (%)": r.overall_score,
                "Passed": f"{r.passed_questions}/{r.total_questions}",
                "Status": r.status,
                "Started At": r.started_at.strftime("%Y-%m-%d %H:%M:%S") if r.started_at else None,
            })
        df_runs = pd.DataFrame(run_data)
        st.dataframe(df_runs, use_container_width=True)

        selected_run_id = st.selectbox("Inspect Run Details", [r.id for r in runs])
        selected_run = next(r for r in runs if r.id == selected_run_id)

        results = db.query(EvaluationResult).filter(EvaluationResult.run_id == selected_run_id).all()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Overall Score", f"{selected_run.overall_score}%")
        col2.metric("Passed Questions", f"{selected_run.passed_questions} / {selected_run.total_questions}")
        avg_lat = round(sum((r.latency_ms or 0) for r in results) / max(len(results), 1), 1)
        col3.metric("Avg Latency", f"{avg_lat} ms")
        tot_tok = sum((r.tokens_used or 0) for r in results)
        col4.metric("Total Tokens", f"{tot_tok:,}")

        st.markdown("---")

        tab_res, tab_err, tab_run = st.tabs(["Question-Level Results", "Deviations & Failure Analysis", "Run New Evaluation"])

        with tab_res:
            res_rows = []
            for res in results:
                res_rows.append({
                    "Benchmark ID": res.benchmark_id,
                    "Model": res.model,
                    "Score": res.score,
                    "Status": res.status,
                    "Latency (ms)": res.latency_ms,
                    "Predicted": res.predicted_answer,
                    "Expected": res.expected_answer,
                })
            df_res = pd.DataFrame(res_rows)
            st.dataframe(df_res, use_container_width=True)

        with tab_err:
            failed_res = [r for r in results if r.status != "passed"]
            st.write(f"**Total Deviations / Failures**: {len(failed_res)}")
            if failed_res:
                err_data = []
                for fr in failed_res:
                    err_data.append({
                        "Benchmark ID": fr.benchmark_id,
                        "Error Classification": fr.error_message or "MISMATCH",
                        "Predicted": fr.predicted_answer[:120],
                        "Expected": fr.expected_answer,
                    })
                st.dataframe(pd.DataFrame(err_data), use_container_width=True)
            else:
                st.success("No failures in this run! 100% accuracy achieved.")

        with tab_run:
            st.subheader("Launch On-Demand Model Evaluation")
            with st.form("new_eval_form"):
                model_name = st.text_input("Model Identifier", value="Custom-Healthcare-LLM")
                category_filter = st.selectbox("Category Filter", ["All Categories", "sql_analytics", "statistical_reasoning", "data_interpretation", "data_quality", "business_decision_making", "contradictory_evidence"])
                mock_acc = st.slider("Simulated Accuracy (Mock Mode)", min_value=0.5, max_value=1.0, value=0.85, step=0.05)
                submitted = st.form_submit_button("Start Evaluation Run")

                if submitted:
                    cat = None if category_filter == "All Categories" else category_filter
                    client = ModelClient(model_name=model_name, mock_mode=True, mock_accuracy=mock_acc)
                    runner = EvaluationRunner(db=db, client=client)
                    with st.spinner(f"Evaluating model '{model_name}'..."):
                        new_res = runner.run_evaluation(model_name=model_name, category=cat)
                    st.success(f"Evaluation Complete! Score: {new_res['overall_score_pct']}% ({new_res['passed_questions']}/{new_res['total_questions']})")
                    st.rerun()

    else:
        st.info("No evaluation runs recorded yet. Use the API or scripts to trigger runs.")

finally:
    db.close()
