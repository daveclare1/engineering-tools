from dataclasses import dataclass
import numpy as np
import pandas as pd
import control as ct

@dataclass
class DCBrushedMotor():
    R: float    # winding resistance [Ω]
    b: float    # damping constant [Nm/(rad/s)]
    K: float    # both torque and back emf constant (same fundamental units) [Nm/A or V/(rad/s)]
    J: float = None   # inertia [kg.m2]
    L: float = None   # winding inductance [H]
    state_names = ["shaft speed", "current"]
    state_units = ["rad/s", "A"]


    def __post_init__(self):
        if self.J is None and self.L is None:
            # Fine to have the class, but can't do dynamic analysis
            self.sys = None
            return

        # set up state space representation
        # state vector x is [theta_dot, current]
        # input vector u is [V, t_load]
        self._A = [[-self.b/self.J, self.K/self.J], [-self.K/self.L, -self.R/self.L]]
        self._B = [[0, -1/self.J], [1/self.L, 0]]
        self._C = [1, 1]
        self._D = 0
        self.sys = ct.ss(self._A, self._B, self._C, self._D)


    @classmethod
    def from_free_run_data(cls, free_current:float, free_speed:float, R:float, K:float, J:float=None, L:float=None):
        # derive damping constant from measured point
        # derivation makes V magically disappear
        b = K * free_current / free_speed
        return cls(R, b, K, J, L)

    
    def steady_state(self, voltage:float, load_torque:float) -> tuple[float, float]:
        # a bit of derivation gets you to this, where J and L are irrelevant
        w = (self.K*voltage - load_torque*self.R) / (self.K**2 + self.b*self.R)
        i = (voltage - self.K*w) / self.R
        return w, i

    
    def simulate(self, voltage:np.array, load_torque:np.array, dt:float, x0=[0,0]) -> pd.DataFrame:
        if self.sys is None:
            raise AttributeError("J and L must be defined to simulate dynamics")
        if len(voltage) != len(load_torque):
            raise ValueError("voltage and load torque arrays must be the same length")

        samples = len(voltage)
        times = np.arange(0, samples)*dt
        timeData = ct.forced_response(self.sys, times, U=np.vstack([voltage, load_torque]), X0=x0, return_x=True)
        df = pd.DataFrame(
            {
                'time': times,
                'voltage': voltage,
                'torque': load_torque,
                'speed': timeData.states[0],
                'current': timeData.states[1],
            }
        )
        return df

    
    def stall_torque(self, voltage:float) -> float:
        return self.K * voltage / self.R


    def time_constant_mech(self, voltage:float, max_time_s=0.05) -> float:
        samples = 1000
        df = self.simulate(voltage=np.ones(samples)*voltage, load_torque=np.zeros(samples), dt=max_time_s/samples)
        threshold_speed = 0.635*df.speed.max()
        idx = np.argmax(df.speed > threshold_speed)
        return df.time[idx]

    
    def characterisation(self, voltage:float, samples=100) -> pd.DataFrame:
        df = pd.DataFrame({"torque": np.linspace(0, self.stall_torque(voltage), samples, endpoint=True)})
        df[['speed', 'current']] = df.apply(
            lambda row: pd.Series(self.steady_state(voltage, row['torque'])),
            axis=1)
        df['power_e'] = df.current * voltage
        df['power_m'] = df.speed * df.torque 
        df['efficiency'] = df.power_m / df.power_e
        return df
