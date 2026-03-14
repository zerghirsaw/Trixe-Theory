import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# PLOT SETTINGS FOR Q1 JOURNAL STANDARDS
# ==========================================
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'legend.fontsize': 11,
    'figure.dpi': 300 # High resolution
})

def rk4_step_S(S, mu, alpha, beta, dt):
    """
    4th-Order Runge-Kutta (RK4) integration for the deterministic stabilizer ODE.
    Equation: dS/dt = -alpha * S + beta * mu
    """
    def f(s_val):
        return -alpha * s_val + beta * mu

    k1 = f(S)
    k2 = f(S + 0.5 * dt * k1)
    k3 = f(S + 0.5 * dt * k2)
    k4 = f(S + dt * k3)
    
    return S + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def simulate_trixe_v2(alpha, beta, k_pull=2.0, sigma_0=2.5, kappa=1.0, gamma=0.8, T_total=10.0, dt=0.01, N_particles=1000):
    """
    Core Trixe framework V2: Implements Bidirectional Coupling (Adaptive Noise).
    Uses Euler-Maruyama for the stochastic differential equation (SDE) and RK4 for the ODE.
    """
    N_steps = int(T_total / dt)
    time_array = np.linspace(0, T_total, N_steps)
    
    # System Initialization
    x_particles = np.random.normal(loc=-4.0, scale=2.0, size=N_particles) 
    S_current = 4.0 
    sigma_eff = sigma_0

    # Data arrays for logging system state
    S_history = np.zeros(N_steps)
    mu_history = np.zeros(N_steps)
    var_history = np.zeros(N_steps)
    sigma_eff_history = np.zeros(N_steps)
    x_sample_history = np.zeros((N_steps, 10)) 

    for i in range(N_steps):
        # A. Extract Statistical Moments (Expectation and Variance)
        mu_x = np.mean(x_particles)
        var_x = np.var(x_particles)
        
        # B. Calculate Non-Linear Coupling Force H(S, P)
        H_n = kappa * S_current * var_x
        
        # C. Evolve Stabilizer (0Xe) using RK4 (Deterministic)
        S_next = rk4_step_S(S_current, mu_x, alpha, beta, dt)
        
        # Prevent extreme overflow in the runaway/collapse scenario
        if abs(S_next) > 1e4: 
            S_next = 1e4 * np.sign(S_next)
            
        # D. Bidirectional Coupling: Exponential Noise Suppression
        # Effective noise decays asymptotically only if the system is stable (alpha > beta)
        if alpha > beta:
            sigma_eff = sigma_eff * np.exp(-gamma * abs(H_n) * dt)
        
        # E. Evolve Probabilistic Chaos (<Xe) using Euler-Maruyama (Stochastic)
        dW = np.random.normal(0, np.sqrt(dt), N_particles)
        dx = -k_pull * (x_particles - S_current) * dt + sigma_eff * dW
        x_particles += dx
        
        # Update state variable
        S_current = S_next
        
        # Record state dynamics
        S_history[i] = S_current
        mu_history[i] = mu_x
        var_history[i] = var_x
        sigma_eff_history[i] = sigma_eff
        x_sample_history[i, :] = x_particles[:10]

    return time_array, S_history, mu_history, var_history, sigma_eff_history, x_sample_history, S_current

def plot_paper_dynamics(time_array, S_history, mu_history, x_sample_history, filename):
    """Generates standard two-panel macro/micro dynamics plots for the manuscript."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(time_array, S_history, label=r'Stabilizer $S(t)$', color='red', linewidth=2.5)
    ax1.plot(time_array, mu_history, label=r'Expectation $\mu(t)$', color='blue', linestyle='--', linewidth=2)
    ax1.set_title('Macrodynamics: Transition to $O_v$')
    ax1.set_xlabel('Time (t)')
    ax1.set_ylabel('Spatial Position (x)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    for j in range(10):
        ax2.plot(time_array, x_sample_history[:, j], color='gray', alpha=0.4, linewidth=0.8)
    ax2.plot(time_array, S_history, label=r'Deterministic Path', color='red', linewidth=2.5)
    ax2.set_title(r'Microdynamics: Chaos Collapse')
    ax2.set_xlabel('Time (t)')
    ax2.set_ylabel('Spatial Position (x)')
    
    import matplotlib.lines as mlines
    gray_line = mlines.Line2D([], [], color='gray', label=r'$<Xe$ Probability Samples')
    red_line = mlines.Line2D([], [], color='red', linewidth=2.5, label=r'Deterministic Path ($>Xe$)')
    ax2.legend(handles=[gray_line, red_line])
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def plot_variance_decay(time_array, var_history, sigma_eff_history):
    """Generates the plot demonstrating the asymptotic decay of variance to zero."""
    plt.figure(figsize=(8, 6))
    plt.plot(time_array, var_history, label=r'Population Variance ($\sigma^2_x$)', color='purple', linewidth=2.5)
    plt.plot(time_array, sigma_eff_history, label=r'Effective Noise ($\sigma_{eff}$)', color='orange', linestyle='--', linewidth=2.5)
    plt.title('Bidirectional Coupling: Variance Decay to Zero')
    plt.xlabel('Time (t)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('trixe_variance_decay_proof.png', bbox_inches='tight')
    plt.close()

def generate_bifurcation_diagram():
    """Generates the bifurcation diagram to demonstrate the critical boundary."""
    alpha = 1.5
    betas = np.linspace(0.5, 2.5, 30)
    final_S_values = []
    
    print("Generating Bifurcation Diagram...")
    for beta in betas:
        _, _, _, _, _, _, S_final = simulate_trixe_v2(alpha=alpha, beta=beta, T_total=10.0)
        final_S_values.append(abs(S_final))

    plt.figure(figsize=(8, 6))
    plt.plot(betas, final_S_values, marker='o', color='darkred', linewidth=2)
    plt.axvline(x=alpha, color='blue', linestyle='--', linewidth=2, label=rf'Critical Boundary ($\beta = \alpha = {alpha}$)')
    plt.title('Trixe System Collapse (Bifurcation Diagram)')
    plt.xlabel(r'Probability Response Strength ($\beta$)')
    plt.ylabel('Stabilizer Final Deviation (Symlog Scale)')
    plt.yscale('symlog')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('trixe_bifurcation.png', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Initializing Trixe V2 Framework (Bidirectional Coupling)...")
    
    # 1. Stable Scenario Execution
    print("Running Stable Scenario (alpha=1.5, beta=0.5)...")
    t, S_hist, mu_hist, var_hist, sig_hist, x_hist, _ = simulate_trixe_v2(alpha=1.5, beta=0.5)
    plot_paper_dynamics(t, S_hist, mu_hist, x_hist, 'trixe_stable_scenario.jpg')
    plot_variance_decay(t, var_hist, sig_hist) 
    
    # 2. Collapse Scenario Execution
    print("Running Collapse Scenario (alpha=1.5, beta=1.6)...")
    t, S_hist, mu_hist, _, _, x_hist, _ = simulate_trixe_v2(alpha=1.5, beta=1.6)
    plot_paper_dynamics(t, S_hist, mu_hist, x_hist, 'trixe_collapse_scenario.jpg')
    
    # 3. Bifurcation Analysis Execution
    generate_bifurcation_diagram()
    
    print("Simulation complete. High-resolution figures generated successfully.")
