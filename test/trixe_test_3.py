import numpy as np
import matplotlib.pyplot as plt
import os

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

def simulate_trixe(alpha, beta, k_pull=2.0, sigma=1.5, T_total=10.0, dt=0.01, N_particles=1000, scenario_name="stable"):
    """
    Core Trixe framework integrating PDE (via sample paths) and ODE.
    Uses Euler-Maruyama for the SDE and RK4 for the ODE.
    """
    N_steps = int(T_total / dt)
    time_array = np.linspace(0, T_total, N_steps)
    
    # 1. Initialization (Probabilistic Chaos)
    x_particles = np.random.normal(loc=-4.0, scale=2.0, size=N_particles) 
    S_current = 4.0 

    # Data containers
    S_history = np.zeros(N_steps)
    mu_history = np.zeros(N_steps)
    x_sample_history = np.zeros((N_steps, 10)) 

    # 2. Dual-Scheme Numerical Integration
    for i in range(N_steps):
        # A. Extract probability expectation E[x]
        mu_x = np.mean(x_particles)
        
        # B. Evolve Stabilizer (0Xe) using RK4 (Deterministic)
        S_next = rk4_step_S(S_current, mu_x, alpha, beta, dt)
        
        # Prevent extreme overflow in runaway scenario
        if abs(S_next) > 1e4:
            S_next = 1e4 * np.sign(S_next)
            
        S_current = S_next
        
        # C. Evolve Probabilistic Chaos (<Xe) using Euler-Maruyama (Stochastic)
        # Langevin Eq: dX = -k(X - S)dt + sigma * dW
        dW = np.random.normal(0, np.sqrt(dt), N_particles)
        dx = -k_pull * (x_particles - S_current) * dt + sigma * dW
        x_particles += dx
        
        # D. Record state
        S_history[i] = S_current
        mu_history[i] = mu_x
        x_sample_history[i, :] = x_particles[:10]

    return time_array, S_history, mu_history, x_sample_history, S_current

def plot_dynamics(time_array, S_history, mu_history, x_sample_history, filename):
    """Generates and exports high-quality macro/micro dynamics plots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Macroscopic Trajectory
    ax1.plot(time_array, S_history, label=r'Stabilizer $S(t)$', color='red', linewidth=2.5)
    ax1.plot(time_array, mu_history, label=r'Expectation $\mu(t)$', color='blue', linestyle='--', linewidth=2)
    ax1.set_title('Macrodynamics: Transition to Orbital Variable $O_v$')
    ax1.set_xlabel('Time (t)')
    ax1.set_ylabel('Spatial Position (x)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Microscopic View (Particle Collapse)
    for j in range(10):
        ax2.plot(time_array, x_sample_history[:, j], color='gray', alpha=0.4, linewidth=0.8)
    ax2.plot(time_array, S_history, label=r'Transition Path $0Xe$', color='red', linewidth=2.5)
    ax2.set_title(r'Microdynamics: Chaos Collapse ($>Xe$ Effect)')
    ax2.set_xlabel('Time (t)')
    ax2.set_ylabel('Spatial Position (x)')
    
    # Custom legend for samples
    import matplotlib.lines as mlines
    gray_line = mlines.Line2D([], [], color='gray', label=r'$<Xe$ Probability Samples')
    red_line = mlines.Line2D([], [], color='red', linewidth=2.5, label=r'Deterministic Path ($>Xe$)')
    ax2.legend(handles=[gray_line, red_line])
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{filename}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_bifurcation_diagram():
    """Generates the bifurcation diagram demonstrating the critical boundary."""
    alpha = 1.5
    betas = np.linspace(0.5, 2.5, 30)
    final_S_values = []
    
    print("Generating Bifurcation Diagram...")
    for beta in betas:
        _, _, _, _, S_final = simulate_trixe(alpha=alpha, beta=beta, T_total=10.0)
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
    plt.savefig('trixe_bifurcation.eps', format='eps', bbox_inches='tight')
    plt.savefig('trixe_bifurcation.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Initializing Trixe Framework Simulation Suite...")
    
    # Ensure output directory exists (optional, saves in current dir by default)
    
    # 1. Stable Scenario (Alpha > Beta)
    print("Running Stable Scenario (alpha=1.5, beta=0.5)...")
    t, S_hist, mu_hist, x_hist, _ = simulate_trixe(alpha=1.5, beta=0.5, scenario_name="stable")
    plot_dynamics(t, S_hist, mu_hist, x_hist, 'trixe_stable_scenario')
    
    # 2. Collapse/Runaway Scenario (Beta > Alpha)
    print("Running Collapse Scenario (alpha=1.5, beta=1.6)...")
    t, S_hist, mu_hist, x_hist, _ = simulate_trixe(alpha=1.5, beta=1.6, scenario_name="collapse")
    plot_dynamics(t, S_hist, mu_hist, x_hist, 'trixe_collapse_scenario')
    
    # 3. Bifurcation Analysis
    generate_bifurcation_diagram()
    
    print("Simulation complete. High-resolution EPS and PNG files generated.")
