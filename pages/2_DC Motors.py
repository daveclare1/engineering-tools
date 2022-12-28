import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("Brushed DC Motors")

st.markdown("""
    The steady state of a DC motor can be modelled (in an idealised fashion)
    with the following parameters:
    - $R$ the winding resistance in $\Omega$
    - $K_\\tau$ the motor torque constant in $Nm/A$
    - $K_v$ the back emf constant in $V/rad.s^{-1}$. An interesting quirk of
        using SI units means this is equal to $K_\\tau$.
    - $b$ the motor damping constant in $Nm/rad.s^{-1}$
    In order to model the dynamic system, the following parameters are also
    required:
    - $L$ the winding inductance in Henrys
    - $J$ the rotor inertia in $kg.m^2$
    These parameters define the bidirectional connection between the electrical
    power in the winding (current, $i$ and voltage, $V$) and the shaft 
    power (speed, $\omega$ and torque, $\\tau$).
    """)

with st.expander("Modelling approach"):
    st.markdown("""
    ### Dynamical system
    The state space method is used in the underlying code here. $K_\\tau$ and
    $K_V$ are both referred to as $K$ because they take the same value.
    The electrical side:

    $$V = Ri + K\omega + L\\frac{di}{dt}$$

    The mechanical side:

    $$Ki = \\tau_{load} + b\omega + J\dot{\omega}$$

    In state space form, $x$ as system state and $u$ as input vector (voltage
    control):
    
    $$x = \\begin{bmatrix} \omega \\\\ i \end{bmatrix} , \
        u = \\begin{bmatrix} V \\\\ \\tau_{load} \end{bmatrix}$$

    $$\dot{x} = \\begin{bmatrix} -\\frac{b}{J} & \\frac{K}{J}\\\\ \
        -\\frac{K}{L} & -\\frac{R}{L} \end{bmatrix} x + \
        \\begin{bmatrix} 0 & -\\frac{1}{J} \\\\ \\frac{1}{L} & 0 \
        \\end{bmatrix} u$$

    These matrices are usually referred to as $A$ and $B$

    ### Steady state
    In the steady state, where $\dot{x} = 0$, if you already have the
    $A$ and $B$ matrices you can do the following:

    $$ x = A^{-1}Bu $$

    However it is also possible to derive the following from the original
    equations. This is generally more convenient since $J$ and $L$ disappear, 
    and these parameters are not always known.

    $$ \omega = \\frac{KV - \\tau R}{K^2 + bR} $$

    $$ i = \\frac{V - K\omega}{R} $$
    """)

st.markdown("""
    ### References and Reading
    - [Simulink writeup of DC motor modelling](https://uk.mathworks.com/help/sps/ref/dcmotor.html)
    """)