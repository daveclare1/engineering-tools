from engpy.motors import DCBrushedMotor
import numpy as np

# This data comes from the data sheet for Delta Line 16DC26N-G9401. From page
# 34 of the 2022-23 catalog
# The tests don't expect perfect alignment between the modelling and the quoted
# values, as some of them may come from experimental data. In each test case
# suitable tolerances have been set manually.
motor_nominal_voltage = 6       # V
motor_speed_rated = 9400*2*np.pi/60   # rad/s
motor_torque_rated = 5.45e-3    # Nm
motor_current_rated = 1.28      # A
motor_torque_stall = 21.3e-3    # Nm
motor_current_stall = 4.79      # A
motor_speed_free = 12700*2*np.pi/60   # rad/s
motor_current_free = 0.0639     # A
motor_efficiency = 0.78
motor_time_constant = 6.35e-3   # s
J = 1 * 1e-7    # inertia in g.cm2 to kg.m2
b = 2.13e-7    # damping constant
K = 4.45e-3     # also the back emf constant because metric
L = 0.036e-3    # 0.036mH
R = 1.25


def test_derive_damping_constant():
    motor = DCBrushedMotor.from_free_run_data(motor_current_free, motor_speed_free, R, K)
    assert np.isclose(
        motor.b,
        b
        )


def test_simulation_guard():
    motor = DCBrushedMotor(R, b, K)
    assert np.isclose(
        motor.b,
        b
        )


def test_motor_simulates():
    motor = DCBrushedMotor(R, b, K, J, L)
    assert np.isclose(
        motor.time_constant_mech(motor_nominal_voltage),
        motor_time_constant,
        atol=1e-3
        )


def test_steady_state():
    motor = DCBrushedMotor(R, b, K)
    ss = motor.steady_state(motor_nominal_voltage, motor_torque_rated)
    assert all(np.isclose(
        ss,
        [motor_speed_rated, motor_current_rated],
        atol=[10, 0.01]
        ))


def test_effeciency():
    motor = DCBrushedMotor(R, b, K, J, L)
    df = motor.characterisation(motor_nominal_voltage)
    assert np.isclose(
        df.efficiency.max(),
        motor_efficiency,
        atol=0.02
        )