#%%

def option_pnl(
    delta,
    gamma,
    theta,
    vega,
    dS,
    days,
    dIV
):
    """
    delta  : option delta
    gamma  : option gamma
    theta  : per-day theta
    vega   : per 1.0 IV change
    dS     : expected stock price change
    days   : holding period (days)
    dIV    : expected IV change
    """

    price_pnl = delta * dS
    gamma_pnl = 0.5 * gamma * (dS ** 2)
    theta_pnl = theta * days
    vega_pnl  = vega * dIV

    return price_pnl + gamma_pnl + theta_pnl + vega_pnl


delta = 0.3337
gamma = 0.1069
theta = -0.0088
vega  = 0.0435
dS    = 2
days  = 77
dIV   = 1

for dS in [-1, 0, 1, 2]:
    pnl = option_pnl(delta, gamma, theta, vega, dS, days=2, dIV=0)
    print(dS, pnl)

