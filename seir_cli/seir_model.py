import numpy as np
import click
import os
from pathlib import Path
from scipy.integrate import odeint
import plotly.graph_objects as go
from datetime import datetime

def ode_model(z, t, beta, sigma, gamma):
    """
    
    """
    S, E, I, R = z
    N = S + E + I + R
    dSdt = -beta*S*I/N
    dEdt = beta*S*I/N - sigma*E
    dIdt = sigma*E - gamma*I
    dRdt = gamma*I
    return [dSdt, dEdt, dIdt, dRdt]


def ode_solver(t, initial_conditions, params):
    initE, initI, initR, initN = initial_conditions
    beta, sigma, gamma = params
    initS = initN - (initE + initI + initR)
    res = odeint(ode_model, [initS, initE, initI, initR], t, args=(beta, sigma, gamma))
    return res


def seir_run(initE, initI, initR, initN, beta, sigma, gamma, days, country):
    initial_conditions = [initE, initI, initR, initN]
    params = [beta, sigma, gamma]
    tspan = np.arange(0, days, 1)
    sol = ode_solver(tspan, initial_conditions, params)
    S, E, I, R = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
    
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tspan, y=S, mode='lines+markers', name='Susceptible'))
    fig.add_trace(go.Scatter(x=tspan, y=E, mode='lines+markers', name='Exposed'))
    fig.add_trace(go.Scatter(x=tspan, y=I, mode='lines+markers', name='Infected'))
    fig.add_trace(go.Scatter(x=tspan, y=R, mode='lines+markers',name='Recovered'))
    
    if days <= 30:
        step = 1
    elif days <= 90:
        step = 7
    else:
        step = 30
    
    # Edit the layout
    fig.update_layout(title='Simulation of SEIR Model',
                       xaxis_title='Day',
                       yaxis_title='Counts',
                       title_x=0.5,
                      width=900, height=600
                     )
    fig.update_xaxes(tickangle=-90, tickformat = None, tickmode='array', tickvals=np.arange(0, days + 1, step))
    if not os.path.exists("images"):
        os.mkdir("images")
    date = datetime.now().strftime("%m_%d-%I:%M:%S_%p")
    if country:
        fig.write_image(f'images/seir_simulation_{country}_{date}.png')
    else:
        fig.write_image(f'images/seir_simulation_{date}.png')

    # fig.show()


@click.command()
@click.option('--init_E', '-ie', default=1.0, required=True,
              type=int, help='Initial value for population that is Exposed')
@click.option('--init_I', '-ii', default=1.0, required=True,
              type=int, help='Initial value for population that is Infectious')
@click.option('--init_R', '-ir', default=0.0, required=True,
              type=int, help='Initial value for population that is Recovered')
@click.option('--init_pop_size', '-ip', default=3.3e3, required=True,
              type=int, help='Initial value for Population Size')
@click.option('--infection_rate', default=4*(1/2.9), required=True,
              type=float, help='Value for Infection rate (beta value in equation)')
@click.option('--incubation_rate', default=(1/5.2), required=True,
              type=float, help='Value for Incubation rate (sigma value in equation)')
@click.option('--recovery_rate', default=(1/2.9), required=True,
              type=float, help='Value for Recovery rate (gamma value in equation)')
@click.option('--days', default=150.0, required=True,
              type=int, help='Value for number of days of simulation')
@click.option('--country', default='',
              type=str, help='Value for number of days of simulation')
def main(init_e, init_i, init_r, init_pop_size, infection_rate, incubation_rate, recovery_rate, days, country):
    """A CLI for seir model"""
    # initE = inite
    print(1/2.9)
    print(init_e, init_i, init_r, init_pop_size, infection_rate, incubation_rate, recovery_rate, days, country)
    initE = init_e
    initI = init_i
    initR = init_r
    initN = init_pop_size
    beta = infection_rate
    sigma = incubation_rate
    gamma = recovery_rate
    seir_run(initE, initI, initR, initN, beta, sigma, gamma, days, country)

if __name__ == "__main__":
    main()