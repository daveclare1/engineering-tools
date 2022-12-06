import streamlit as st
import plotly.graph_objects as go
import numpy as np

from engpy.binomial_reliability import sample_size_zero_fails, confidence_level

st.title("Binomial Reliability")

st.write(r"""
    The cumulative binomial equation can be used in a pass/fail experiment 
    to determine one of the following:
    * The number of samples needed to prove a claimed success rate with a known confidence
    * The success rate to be expected in the wider population, given test results and a desired level of confidence
    
    In an engineering context it is often used in simulated lifetime testing, 
    for example a 'cycles to failure' test. 
    
    An example of a statement based on this equation would be 'we are 95% 
    sure that 90% of our products would pass this test, because we tested 
    29 and saw no failures'.

    $$
    C_L=1-\sum_{i=0}^{f}\binom{n}{i}(1-R_L^i)R_L^{n-i}
    $$
    where $R_L$ = reliability level, $C_L$ = confidence level, 
    $n$ = sample size and $f$ = number of failures observed. The levels are
    always values between 0 and 1.
    """)

with st.expander("Exploration"):
    # Define the different slider possibilities for the plot control
    plot_ctrl_definitions = {
        "Reliability": {
            "min_value": 0.0,
            "max_value": 1.0,
            "value": 0.90,
            "step": 0.05
        },
        "Confidence": {
            "min_value": 0.0,
            "max_value": 1.0,
            "value": 0.95,
            "step": 0.05
        },
        "Sample Size": {
            "min_value": 0,
            "max_value": 100,
            "value": 10,
            "step": 1
        },
    }
    x_data = np.linspace(0.5, 0.99, 49, endpoint=True)

    cols = st.columns([1,2])
    cols[0].write(
        """Choose the fixed variable, then see the relationship 
        between the remaining two on the plot. This assumes
        0 failures and is only accurate to the nearest percentage point."""
        )
    fixed_var = cols[0].radio("Fixed variable", ["Reliability", "Confidence", "Sample Size"], 0)
    fixed_val = cols[0].slider(f"{fixed_var} Value", **plot_ctrl_definitions[fixed_var])

    plot_title = f"For {fixed_var} of {fixed_val:.0%}"
    y_format = '0'
    if fixed_var == "Reliability":
        y_data = sample_size_zero_fails(fixed_val, x_data)
    elif fixed_var == "Confidence":
        y_data = sample_size_zero_fails(x_data, fixed_val)
    elif fixed_var == "Sample Size":
        y_data = confidence_level(fixed_val, 0, x_data)
        y_format = ',.0%'
        plot_title = f"For {fixed_var} of {fixed_val}"

    x_label = 'Reliability' if fixed_var != 'Reliability' else 'Confidence'
    y_label = 'Sample Size' if fixed_var != 'Sample Size' else 'Confidence'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data,
                            y=y_data,
                            ))
    fig.update_layout(
        title=plot_title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis=dict(tickformat=',.0%'),
        yaxis=dict(tickformat=y_format),
        hovermode='x',
                   
    )

    cols[1].plotly_chart(fig, use_container_width=True)



