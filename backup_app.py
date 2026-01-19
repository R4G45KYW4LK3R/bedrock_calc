#python -m streamlit run app.py
# backup_app.py
import streamlit as st
from sample_data import MODELS
# ERROR FIXED: Import the correct function name
from roi_function import calculate_metrics 


st.set_page_config(page_title="LLM ROI Calculator", page_icon="📊", layout="wide")

st.title("📊 ROI Calculator for Distilled Models")
st.markdown("Styled similar to **AWS Pricing Calculator**")
st.divider()

col1, col2 = st.columns(2)
# Ensure Teacher is the larger, more expensive model
with col1:
    teacher = st.selectbox("Select Teacher Model (Original)", list(MODELS.keys()), index=0)
with col2:
    # Ensure Student is the smaller, cheaper model
    student = st.selectbox("Select Student Model (Distilled)", list(MODELS.keys()), index=1)

application = st.selectbox("Select Application", ["qa", "summarization"])
num_requests = st.number_input("Number of Requests (scalability view)", min_value=1000, step=1000, value=100000)

if st.button("🔍 Compare Models"):
    # Ensure the selected models are different
    if teacher == student:
        st.error("Please select different models for Teacher and Student comparison.")
        st.stop()
        
    t = MODELS[teacher]
    s = MODELS[student]
    # ERROR FIXED: Call the correct function name
    results = calculate_metrics(teacher, student, application, num_requests)

    st.subheader("📑 Comparison Summary")
    
    # ERROR FIXED: Updated dictionary keys to match the new MODELS structure
    data = {
        "Metric": [
            "Cost per request ($)",
            f"Total cost for {num_requests:,} requests ($)",
            f"Accuracy ({application.upper()}) (%)",
            "Human Eval (1-5)",
            "Latency (avg ms)",
            "Latency (P95 ms)",
            "Throughput (req/s)",
            "Memory (GB)",
            "Compute"
        ],
        teacher: [
            f"${t['cost_per_request']:.6f}",
            f"${results['teacher_total_cost']:.2f}",
            f"{t['accuracy'][application]*100:.1f}%",
            f"{t['human_eval']}",
            f"{t['latency_ms']} ms",
            f"{t['p95_latency_ms']} ms",
            f"{t['throughput_rps']}/s",
            f"{t['resource_util']['memory_gb']}",
            f"{t['resource_util']['compute']}"
        ],
        student: [
            f"${s['cost_per_request']:.6f}",
            f"${results['student_total_cost']:.2f}",
            f"{s['accuracy'][application]*100:.1f}%",
            f"{s['human_eval']}",
            f"{s['latency_ms']} ms",
            f"{s['p95_latency_ms']} ms",
            f"{s['throughput_rps']}/s",
            f"{s['resource_util']['memory_gb']}",
            f"{s['resource_util']['compute']}"
        ]
    }
    st.table(data)
    
    st.divider()

    st.subheader("📈 ROI Analysis: Cost vs. Performance Trade-off")
    c1, c2, c3 = st.columns(3)
    c1.metric("Cost Savings %", f"{results['cost_savings_pct']:.1f}%", delta="High Savings!")
    c2.metric("Accuracy Drop %", f"-{results['acc_drop_pct']:.1f}%", delta_color="inverse")
    # ERROR FIXED: Handle the 'inf' case gracefully
    tradeoff_value = "∞" if results['performance_tradeoff'] == float("inf") else f"{results['performance_tradeoff']:.2f}x"
    c3.metric("Trade-off Ratio (Cost/Acc Drop)", tradeoff_value, help="Higher is better: Cost savings relative to the drop in accuracy.")

    st.markdown("### Performance Visualisation")
    
    chart_data = {
        "Metric": ["Total Cost ($)", "Average Latency (ms)", f"Accuracy (%)"],
        teacher: [results['teacher_total_cost'], t["latency_ms"], t["accuracy"][application]*100],
        student: [results['student_total_cost'], s["latency_ms"], s["accuracy"][application]*100]
    }
    
    # Use st.dataframe and st.bar_chart for better side-by-side visualisation
    st.bar_chart(chart_data, x="Metric", use_container_width=True)