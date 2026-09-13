import streamlit as st
import plotly.express as px
from mni.core import UserState, estimate_struggle, choose_minimum_intervention
from mni.simulate import generate_population, evaluate_strategies, summarize, simulate_episode, threshold_sweep, robustness_suite, heterogeneity_suite, ablation_suite

st.set_page_config(page_title="MNI — Minimum Necessary Intervention",page_icon="🧭",layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1rem}.hero{padding:1.4rem 1.6rem;border-radius:22px;background:linear-gradient(135deg,rgba(40,40,40,.04),rgba(120,120,120,.12));border:1px solid rgba(128,128,128,.18)}.muted{opacity:.72}[data-testid="stMetric"]{border:1px solid rgba(128,128,128,.16);padding:12px;border-radius:16px}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🧭 MNI</h1><h3>Minimum Necessary Intervention</h3><p>Help only as much as necessary for successful progress, verify recovery, then withdraw.</p><p class="muted">Research demonstrator for adaptive assistance across digital systems.</p></div>',unsafe_allow_html=True)

tabs=st.tabs(["Live Decision","Closed-Loop Episode","Benchmark","Robustness","Ablations","Architecture"])
with tabs[0]:
    c1,c2=st.columns(2)
    with c1:
        dwell=st.slider("Hesitation / dwell z-score",-2.,4.,.5,.1); errors=st.slider("Errors",0,8,1); retries=st.slider("Retries",0,8,1); reversals=st.slider("Navigation reversals",0,8,0); helpq=st.slider("Help requests",0,6,0); progress=st.slider("Progress ratio",0.,1.,.5,.05); skill=st.slider("Estimated skill",.05,.95,.5,.05); tau=st.slider("Required recovery probability",.5,.95,.7,.01)
    state=UserState(dwell,errors,retries,reversals,helpq,progress); struggle=estimate_struggle(state); action,p=choose_minimum_intervention(struggle,tau,skill)
    with c2:
        st.metric("Struggle estimate",f"{struggle:.1%}"); st.metric("Selected intervention",action.name.title()); st.metric("Predicted recovery",f"{p:.1%}"); st.progress(p); st.caption("The selector returns the least intervention whose predicted recovery reaches the required threshold.")
with tabs[1]:
    skill2=st.slider("Episode skill",.05,.95,.55,.05); ep=simulate_episode(skill=skill2,steps=14,threshold=.70); st.dataframe(ep,use_container_width=True,hide_index=True); st.plotly_chart(px.line(ep,x="step",y=["difficulty","struggle","recovery_probability"]),use_container_width=True)
with tabs[2]:
    pop=generate_population(1200,42); res=evaluate_strategies(pop); summary=summarize(res); st.dataframe(summary,use_container_width=True,hide_index=True); st.plotly_chart(px.bar(summary,x="strategy",y=["completion_rate","mean_burden","independent_recovery","repeat_success_without_help","mean_intervention_debt"],barmode="group"),use_container_width=True); st.subheader("Threshold sensitivity"); ts=threshold_sweep(pop); st.dataframe(ts,use_container_width=True,hide_index=True); st.plotly_chart(px.line(ts,x="threshold",y=["completion_rate","mean_burden","mean_intervention_debt"]),use_container_width=True)
with tabs[3]:
    rob=robustness_suite(generate_population(1200,42)); st.dataframe(rob,use_container_width=True,hide_index=True); st.plotly_chart(px.bar(rob,x="case",y=["completion_rate","mean_burden","independent_recovery","mean_intervention_debt"],barmode="group"),use_container_width=True); st.subheader("User heterogeneity"); st.dataframe(heterogeneity_suite(),use_container_width=True,hide_index=True)
with tabs[4]:
    ab=ablation_suite(generate_population(1200,42)); st.dataframe(ab,use_container_width=True,hide_index=True); st.plotly_chart(px.bar(ab,x="ablation",y=["completion_rate","mean_burden","independent_recovery","mean_intervention_debt"],barmode="group"),use_container_width=True)
with tabs[5]:
    st.code("Interaction telemetry\n      ↓\nStruggle estimator\n      ↓\nRecovery model\n      ↓\nMinimum intervention selector\n      ↓\nEscalation / intervention ladder\n      ↓\nRecovery verification\n      ↓\nWithdrawal / fading\n      ↓\nIntervention-debt tracking\n      ↺")
    st.warning("Synthetic controlled evidence only. This software is not human-subject validation and is not a safety-critical decision system.")
