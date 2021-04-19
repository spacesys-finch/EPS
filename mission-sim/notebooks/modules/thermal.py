import numpy as np
import csv


boltzman = 5.67*np.power(10.0, -8.0)  # watt m^-2 K^-1
solar_flux = 1361  # watt m^-2

# Primary Structure heat calculations
# Q_str_batt means heat IN to the structure
def Q_str_batt(T_str, T_batt,structure_constants):
  R = 1/structure_constants['R_str_batt']
  Q_str_batt = - R * (T_str - T_batt)
  return Q_str_batt

def Q_str_pay(T_str, T_pay,structure_constants):
  R = 1/structure_constants['R_str_pay']
  Q_str_pay = - R * (T_str - T_pay)
  return Q_str_pay

def Q_str_sun(area_s, T_str,structure_constants):
  T = T_str ** 4
  #heat radiated from structure surface
  rad_out = structure_constants['e'] * boltzman * structure_constants['area_t'] * T
  #heat absorbed from sun
  abs_in = structure_constants['a'] * area_s * solar_flux 
  net_in = abs_in - rad_out
  return net_in

def Q_str_net(area_s, T_str, T_pay, T_batt,structure_constants):
  net = Q_str_sun(area_s, T_str,structure_constants) + Q_str_pay(T_str, T_pay,structure_constants) + Q_str_batt(T_str, T_batt,structure_constants)
  return net

def T_str_dt(Q_str, T_str, T_pay, T_batt, dt,structure_constants): 
  Q = Q_str
  T_str = T_str + (1/structure_constants['c_str'])*dt*Q;
  return T_str



# Battery Calculations
def Q_batt_self(I_t,structure_constants):
  Q_batt_self = 4*(structure_constants['r_batt'] * I_t)**2
  return Q_batt_self

def Q_batt_heaters(batt_heat,structure_constants):
  if batt_heat == True:
    return 1.28; #value from Eric in watts
  if batt_heat == False:
    return 0.00;

def Q_batt_str(T_str, T_batt,structure_constants):
  R = 1/(structure_constants['R_str_batt'])
  Q_batt_str = - R * (T_batt - T_str)
  return Q_batt_str

def Q_batt_net(T_str, T_batt, batt_heat, I_t,structure_constants):
  Q_batt_net = Q_batt_str(T_str, T_batt, structure_constants) + Q_batt_heaters(batt_heat, structure_constants) + Q_batt_self(I_t, structure_constants)
  return Q_batt_net

def T_batt_dt(Q_batt, T_str, T_batt, dt,structure_constants): 
  Q = Q_batt
  T_batt = T_batt + (1/structure_constants['c_batt'])*dt*Q;
  return T_batt


#Payload calculations
def Q_pay_heaters(pay_heat):
  if pay_heat == True:
    return 2.5 #watts
  else:
    return 0.0;

def Q_pay_str(T_str, T_pay,structure_constants):
  R = 1/(structure_constants['R_str_batt'])
  Q_str_pay = - R * (T_pay - T_str)
  return Q_str_pay

def Q_pay_bott(Area_paycap, T_str,structure_constants):
  T = T_str ** 4

  #heat radiated from structure surface
  rad_out = structure_constants['e'] * boltzman * structure_constants['area_t'] * T
  #heat absorbed from sun
  abs_in = Area_paycap * structure_constants['a'] * solar_flux
  net_in = abs_in - rad_out
  return net_in

def Q_pay_net(T_str, T_pay, pay_heat, A_paycap,structure_constants):
  net = Q_pay_str(T_str, T_pay,structure_constants) + Q_pay_heaters(pay_heat) + Q_pay_bott(A_paycap, T_str,structure_constants)
  return net

def T_pay_dt(Q_pay, T_str, T_pay, dt,structure_constants): 
  Q = Q_pay
  T_pay = T_pay + (1/structure_constants['c_pay'])*dt*Q;
  return T_pay
