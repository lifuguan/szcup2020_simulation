'''
@Author: lifuguan
@Date: 2020-07-23 19:17:56
@LastEditTime: 2020-07-25 08:50:17
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \szcup2020_simulation\py\battery_cal.py
'''
#%%
import xlrd
import sympy
import numpy as np
from scipy import linalg
#%% 
queue = [ 0, 29, 17, 2, 1, 20, 19, 26, 18, 25, 14, 6, 11, 7, 15, 9, 8, 12, 27, 16, 10, 13, 5, 4, 3, 22, 28, 24, 23, 21, 0]
def read_data_model():
    data = xlrd.open_workbook("../data/C2.xlsx")
    table = data.sheet_by_name("Sheet1")
    rowNum = table.nrows
    colNum = table.ncols
    consumes = []
    for i in range(1, rowNum):
        # ignore DC's consume
        if i == 1:
            pass
        else:
            consumes.append(0 if table.cell_value(i, 3) == '/' else table.cell_value(i, 3))
    return consumes

#%% get matrix A
def get_A_matrix(data):
    A = np.ones([29,29], dtype = float)
    diagonal = np.eye(29)
    for i in range(29):
        for j in range(29):
            A[i][j] = data['consumes'][j] / data['r']
    A = A - diagonal
    return A
#%%
def get_b_maatrix(data):
    b = np.ones([29,1], dtype=float)
    for i in range(29):
        b[i][0] = -data['dst']*data['consumes'][i]/data['velocity']+data['f']
        for j in range(29):
            b[i][0] = b[i][0] + data['f']*data['consumes'][i]/data['r']
    return b

#%% numerical solution
def numerical(data):
    data['velocity'] = 100
    data['dst'] = 39305
    data['r'] = 2000
    data['f'] = 2
    A = get_A_matrix(data)
    b = get_b_maatrix(data)
    x = linalg.solve(A, b)
    return x

#%% symbolic solution
def symbolic(data):
    data['velocity'] = sympy.symbols("v", integer = True)
    data['dst'] = 39305
    data['r'] = sympy.symbols("r", integer = True)
    data['f'] = sympy.symbols("f", integer = True)
#%% main function

if __name__ == '__main__':
    data = {}
    data['consumes'] = read_data_model()

    options = {"numerical":1, "symbolic":2}
    option = 1
    if option == options['numerical']:
        x = numerical(data)
    elif option == options['symbolic']:
        x = symbolic(data)
    else:
        print("WARN!!!")
#%%
