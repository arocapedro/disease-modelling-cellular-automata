import numpy as np
import click
import os
from pathlib import Path
from scipy.integrate import odeint
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def R_0(t, start_day, end_day):
    """
    R_0 function to calculate varying value of R

    :param t: time (day)
    :return: new value of R_0
    """ 
    if t > start_day and t < end_day:
        return 2.2
    else:
        return 3.8

def get_beta(t, gamma, start_day, duration_of_lockdown):
    """
    get_beta function to calculate new value of beta based on condition

    :param t: time (day)
    :return: new value of beta
    """
    return R_0(t, start_day, duration_of_lockdown) * gamma


def ode_model(z, t, beta, sigma, gamma, lockdown, start_day, duration_of_lockdown):
    """
    ode_model calculate the values for equation.

    :param z: array of [initS, initE, initI, initR]
    :param t: time
    :param beta: Infection rate
    :param sigma: Incubation rate
    :param gamma: Recovery rate
    :return: array of derivative values [dSdt, dEdt, dIdt, dRdt]
    """ 
    S, E, I, R = z
    N = S + E + I + R
    
    if lockdown:
        dSdt = -get_beta(t, gamma, start_day, duration_of_lockdown)*S*I/N
        dEdt = get_beta(t, gamma, start_day, duration_of_lockdown)*S*I/N - sigma*E
    else:
        dSdt = -beta*S*I/N
        dEdt = beta*S*I/N - sigma*E
    dIdt = sigma*E - gamma*I
    dRdt = gamma*I
    return [dSdt, dEdt, dIdt, dRdt]


def ode_solver(t, initial_conditions, params):
    initE, initI, initR, initN = initial_conditions
    beta, sigma, gamma, lockdown, start_day, duration_of_lockdown = params
    initS = initN - (initE + initI + initR)
    res = odeint(ode_model, [initS, initE, initI, initR], t, args=(beta, sigma, gamma, lockdown, start_day, duration_of_lockdown))
    return res


def seir_run(initE, initI, initR, initN, beta, sigma, gamma, days, country, lockdown, start_day, duration_of_lockdown):
    initial_conditions = [initE, initI, initR, initN]
    params = [beta, sigma, gamma, lockdown, start_day, duration_of_lockdown]
    tspan = np.arange(0, days, 1)
    sol = ode_solver(tspan, initial_conditions, params)
    S, E, I, R = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
    

    simulation = pd.DataFrame({"susceptible":S, "exposed":E, 
                "infectious":I, "removed":R})
    color_list = ["blue","red","green","purple"]

    sns.lineplot(data=simulation,palette=color_list).set(title = 'SEIR Model', xlabel = 'Days', ylabel = 'Population')

    if lockdown:
        plt.axvline(start_day, linestyle="--", color='gray')
        plt.axvline(start_day+duration_of_lockdown, linestyle="--", color='gray')

    if not os.path.exists("images"):
        os.mkdir("images")
    date = datetime.now().strftime("%m_%d-%I:%M:%S_%p")
    if country:
        plt.savefig(f'images/seir_simulation_{country}_{date}.png', bbox_inches="tight")
    else:
        plt.savefig(f'images/seir_simulation_{date}.png', bbox_inches="tight")

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
@click.option('--infection_rate', default=3.8, required=True,
              type=float, help='Value for Infection rate (beta value in equation)')
@click.option('--incubation_rate', default=(1/5.2), required=True,
              type=float, help='Value for Incubation rate (sigma value in equation)')
@click.option('--recovery_rate', default=(1/2.9), required=True,
              type=float, help='Value for Recovery rate (gamma value in equation)')
@click.option('--days', default=150.0, required=True,
              type=int, help='Value for number of days of simulation')
@click.option('--country', default='',
              type=str, help='Value for number of days of simulation')
@click.option('--is_lockdown', default=False,
              type=bool, help='Value if simulation is lockdown')
@click.option('--start_day', default=0,
              type=int, help='Value of lockdown start day')
@click.option('--duration_of_lockdown', default=1,
              type=int, help='Value for duration of lockdown')
def main(init_e, init_i, init_r, init_pop_size, infection_rate, incubation_rate, recovery_rate, days, country, is_lockdown, start_day, duration_of_lockdown):
    """A CLI for seir model"""
    initE = init_e
    initI = init_i
    initR = init_r
    initN = init_pop_size
    R_0 = infection_rate
    sigma = incubation_rate
    gamma = recovery_rate
    beta = R_0 * gamma

    seir_run(initE, initI, initR, initN, beta, sigma, gamma, days, country, is_lockdown, start_day, duration_of_lockdown)

if __name__ == "__main__":
    main()