import pint, os, sys
import numpy as np
ureg = pint.UnitRegistry()

def estimate_the_pressure():
    # the only required argument is mu_K
    # mu_K is assumed to be provided as a positive number
    # mu_K is assumed to be in K

    mu_K = np.float32(sys.argv[1])*ureg.kelvin

    T = 300 * ureg.kelvin
    kB =  1.380649e-23 * ureg.joule/ureg.kelvin # J/K
    Na = 6.022141e23/ureg.mol # mol-1
    h = 6.626e-34 * ureg.joule*ureg.second # Js
    mass_g_mol = 44.01 * ureg.gram/ureg.mol
    mass =(mass_g_mol / Na).to_base_units() # kg
    deBroglie_wavelength = np.sqrt(h**2/(2*np.pi*mass*kB*T)).to_base_units()
    mu_J = (mu_K*kB).to_base_units()
    P_Pa = kB*T/deBroglie_wavelength**3 * np.exp(-mu_J/kB/T)
    P_bar = P_Pa.to("bar")
    return np.round(P_bar,4)

def update_pressure_in_input():
    P_bar = estimate_the_pressure()
    initial_file = open("input.gomc", "r")
    all_lines = []
    for line in initial_file:
        if "Fugacity" in line:
            line = "Fugacity CO2 "+str(P_bar.magnitude)+"\n"
        all_lines.append(line)
    initial_file.close()

    new_file = open("input.gomc", "w")
    for line in all_lines:
        new_file.write(line)
    new_file.close()

if __name__ == "__main__":
    update_pressure_in_input()