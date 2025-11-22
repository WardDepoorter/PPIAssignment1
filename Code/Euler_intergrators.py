import numpy as np

def euler_upward(y0, h , x_max, dydx):
    """
    Upward Euler method for solving ODEs:
    y_i = y_i-1 + h * y'(x_i-1) 
    
    Parameters:
    y0 : float
        Initial value of the dependent variable.
    h : float
        Step size.
    x_max : float
        max value of the domain.
    dxdy : callable
        Function that computes the derivative at x_i-1.
    """
    #set initial conditions, starting at r=0 (center of body)
    # eg in case of moon mass integration, y = M, x=r, h = dr, x_max = R_moon, dydx = dM/dr
    #initialize arrays to store results

    x_values = np.arange(0, x_max, h)
    y_values = np.zeros(len(x_values))
    y_values[0] = y0


    #perform Euler integration
    for i in range(1, len(x_values)):
        dydx_val = dydx(x_values[i-1])
        y_values[i] = y_values[i-1] + dydx_val * h
    return x_values, y_values


def euler_downward(y0, h , x_max, dydx):
    """
    Downward Euler method for solving ODEs:
    y_i-1 = y_i - h * y'(x_i)
    """
    #set initial conditions, starting at r=R_moon (surface of body)
    # eg in case of moon pressure integration, y = P,x=r, h = dr, x_max = R_moon, dydx = dP/dr thus we integrate from bottom to top of the r-array
    #initialize arrays to store results:
    
    x_values = np.arange(0, x_max, h)
    y_values = np.zeros(len(x_values))
    y_values[-1] = y0  # set initial condition at end of the interval (last element)
    #perform Euler integration
    for i in range(len(x_values)-1, 0, -1):
        dydx_val = dydx(x_values[i])
        y_values[i-1] = y_values[i] - dydx_val * h
    return x_values, y_values