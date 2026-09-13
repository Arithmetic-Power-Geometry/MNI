import streamlit as st
import pandas as pd
import plotly.express as px
from mni.core import UserState, estimate_struggle, choose_minimum_intervention
from mni.simulate import generate_population, evaluate_strategies, summarize

st.set_page_config(page_title='MNI — Minimum Necessary Intervention', page_icon='🧭', layout='wide')
st.markdown("""
<style>
.block-container {padding-top:1.4rem;padding-bottom:2rem}
.hero {padding:1.3rem 1.5rem;border-radius:24px;background:linear-gradient(135deg,rgba(30,30,30,.04),rgba(100,100,100,.09));border:1px solid rgba(128,128,128,.18)}
.small {opacity:.75;font-size:.93rem}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🧭 MNI — Minimum Necessary Intervention</h1><p>Help only as much as needed, verify recovery, then withdraw.</p><p class="small">A general adaptive assistance engine for web, apps, learning, services, AI and simulation.</p></div>', unsafe_allow_html=True)

tab1,tab2,tab3=st.tabs(['Live Decision','Benchmark Lab','Architecture'])
with tab1:
    st.subheader('Live intervention decision')
    c1,c2=st.columns(2)
    with c1:
        dwell=st.slider('Hesitation / dwell (z-score)',-2.0,4.0,0.5,0.1)
        errors=st.slider('Errors',0,6,1)
        retries=st.slider('Retries',0,6,1)
        reversals=st.slider('Navigation reversals',0,6,0)
        helpq=st.slider('Help requests',0,5,0)
        progress=st.slider('Progress ratio',0.0,1.0,0.5,0.05)
        skill=st.slider('Estimated skill',0.05,0.95,0.50,0.05)
        tau=st.slider('Required recovery probability',0.50,0.95,0.70,0.01)
    state=UserState(dwell,errors,retries,reversals,helpq,progress)
    struggle=estimate_struggle(state)
    action,p=choose_minimum_intervention(struggle,threshold=tau,skill=skill)
    with c2:
        st.metric('Estimated struggle',f'{struggle:.1%}')
        st.metric('Minimum intervention',action.name.replace('_',' ').title())
        st.metric('Predicted recovery',f'{p:.1%}')
        st.progress(min(max(p,0),1))
        st.info('The controller escalates only until the recovery threshold is met. After successful recovery, assistance should be faded.')
with tab2:
    st.subheader('Synthetic cross-domain benchmark')
    n=st.slider('Synthetic users',200,5000,1200,200)
    tau2=st.slider('MNI threshold',0.55,0.90,0.70,0.01,key='tau2')
    df=generate_population(n_users=n,seed=42)
    res=evaluate_strategies(df,threshold=tau2,seed=123)
    summary=summarize(res)
    st.dataframe(summary,use_container_width=True,hide_index=True)
    m=summary.melt(id_vars='strategy',value_vars=['completion_rate','mean_burden','independent_recovery','repeat_success_without_help','mean_intervention_debt'],var_name='metric',value_name='value')
    fig=px.bar(m,x='strategy',y='value',facet_col='metric',facet_col_wrap=2,barmode='group',height=650)
    st.plotly_chart(fig,use_container_width=True)
    domain=res.groupby(['domain','strategy'],as_index=False).agg(completion_rate=('success','mean'),mean_burden=('burden','mean'),debt=('intervention_debt','mean'))
    st.dataframe(domain,use_container_width=True,hide_index=True)
with tab3:
    st.subheader('Closed-loop architecture')
    st.code('Interaction telemetry\n      ↓\nStruggle estimator\n      ↓\nRecovery probability model\n      ↓\nMinimum intervention selector\n      ↓\nIntervention ladder\n      ↓\nRecovery verification\n      ↓\nAssistance fading / withdrawal\n      ↓\nIntervention-debt tracking\n      ↺')
    st.markdown('**Design rule:** minimize intervention burden and accumulated intervention debt while maintaining a required probability of successful continuation.\n\nThis prototype is a research demonstrator. It does not infer medical or protected attributes and should not be used as a safety-critical decision system without domain-specific validation.')
