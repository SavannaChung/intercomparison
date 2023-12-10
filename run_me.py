import pandas as pd
import numpy as np
import PySimpleGUI as sg

import pypyodbc
import config as cg
import os
from datetime import datetime

import functions as fn
import figures as fg

import report as rp




def main():
    theme = 'DefaultNoMoreNagging'

    event, values, ndw_fetch_msg, window = fn.make_GUI(theme)

    # if event == "Exit":
    #     window.close()

    if event == 'Submit':

        # --- trouble-shooting --
        # event =  'Check Data'
        # for home
        # values = {'-DATETIME-': '2023-10-23 13:13:16', 'DATE + TIME': '', '-PERSON1-': 'KC', '-PERSON2-': '', '-GANTRY-': '1', '-GA-': '0', '-MATERIAL-': 'water', '-HUMIDITY-': '50.2', '-SSCH-': '3126', '-SS_ELE-': '92581', '-SS_ELE_RANGE-': 'Medium', '-SS_ELE_VOLT-': '-200', '-FCH-': '3131', '-F_ELE-': '92581', '-F_ELE_RANGE-': 'Medium', '-F_ELE_VOLT-': '-200', '-COMMENT-': 'testing data. I make up the data', '-NDW-': '84800000', '-ss_TEMP-': '22.4', '-ss_PRESSURE-': '1012', '-ss_TPC-': '1.0094', '-ssR1_240-': '6.510', '-ssR1_210-': '6.467', '-ssR1_180-': '6.453', '-ssR1_170-': '6.457', '-ssR1_160-': '6.466', '-ssR1_110-': '6.724', '-ssR1_70-': '8.019', '-ssR2_240-': '6.509', '-ssR2_210-': '6.472', '-ssR2_180-': '6.455', '-ssR2_170-': '6.456', '-ssR2_160-': '6.464', '-ssR2_110-': '6.724', '-ssR2_70-': '8.021', '-ssR3_240-': '6.507', '-ssR3_210-': '6.465', '-ssR3_180-': '6.454', '-ssR3_170-': '6.455', '-ssR3_160-': '6.455', '-ssR3_110-': '6.733', '-ssR3_70-': '8.023', '-ssR4_240-': '6.509', '-ssR4_210-': '6.460', '-ssR4_180-': '6.460', '-ssR4_170-': '6.460', '-ssR4_160-': '6.460', '-ssR4_110-': '6.730', '-ssR4_70-': '8.023', '-ssR5_240-': '6.507', '-ssR5_210-': '6.470', '-ssR5_180-': '6.460', '-ssR5_170-': '6.455', '-ssR5_160-': '6.458', '-ssR5_110-': '6.728', '-ssR5_70-': '8.020', '-ssAVE_240-': '6.508', '-ssAVE_210-': '6.467', '-ssAVE_180-': '6.456', '-ssAVE_170-': '6.457', '-ssAVE_160-': '6.461', '-ssAVE_110-': '6.728', '-ssAVE_70-': '8.021', '-ssSTD_240-': '0.001', '-ssSTD_210-': '0.005', '-ssSTD_180-': '0.003', '-ssSTD_170-': '0.002', '-ssSTD_160-': '0.004', '-ssSTD_110-': '0.004', '-ssSTD_70-': '0.002', '-f_TEMP-': '22.4', '-f_PRESSURE-': '1012', '-f_TPC-': '1.0094', '-fR1_240-': '6.636', '-fR1_210-': '6.606', '-fR1_180-': '6.584', '-fR1_170-': '6.588', '-fR1_160-': '6.598', '-fR1_110-': '6.852', '-fR1_70-': '8.178', '-fR2_240-': '6.640', '-fR2_210-': '6.601', '-fR2_180-': '6.584', '-fR2_170-': '6.590', '-fR2_160-': '6.598', '-fR2_110-': '6.856', '-fR2_70-': '8.177', '-fR3_240-': '6.634', '-fR3_210-': '6.608', '-fR3_180-': '6.583', '-fR3_170-': '6.586', '-fR3_160-': '6.601', '-fR3_110-': '6.857', '-fR3_70-': '8.180', '-fR4_240-': '6.645', '-fR4_210-': '6.608', '-fR4_180-': '6.588', '-fR4_170-': '6.587', '-fR4_160-': '6.547', '-fR4_110-': '6.852', '-fR4_70-': '8.175', '-fR5_240-': '6.654', '-fR5_210-': '6.658', '-fR5_180-': '6.590', '-fR5_170-': '6.570', '-fR5_160-': '6.550', '-fR5_110-': '6.860', '-fR5_70-': '8.170', '-fAVE_240-': '6.642', '-fAVE_210-': '6.616', '-fAVE_180-': '6.586', '-fAVE_170-': '6.584', '-fAVE_160-': '6.579', '-fAVE_110-': '6.855', '-fAVE_70-': '8.176', '-fSTD_240-': '0.008', '-fSTD_210-': '0.024', '-fSTD_180-': '0.003', '-fSTD_170-': '0.008', '-fSTD_160-': '0.028', '-fSTD_110-': '0.003', '-fSTD_70-': '0.004', '-ssr_TEMP-': '22.3', '-ssr_PRESSURE-': '1012', '-ssr_TPC-': '1.0091', '-ssrR1_240-': '6.510', '-ssrR1_210-': '6.467', '-ssrR1_180-': '6.453', '-ssrR1_170-': '6.457', '-ssrR1_160-': '6.466', '-ssrR1_110-': '6.724', '-ssrR1_70-': '8.019', '-ssrR2_240-': '6.490', '-ssrR2_210-': '6.450', '-ssrR2_180-': '6.460', '-ssrR2_170-': '6.460', '-ssrR2_160-': '6.470', '-ssrR2_110-': '6.730', '-ssrR2_70-': '8.020', '-ssrR3_240-': '6.512', '-ssrR3_210-': '6.460', '-ssrR3_180-': '6.454', '-ssrR3_170-': '6.460', '-ssrR3_160-': '6.470', '-ssrR3_110-': '6.730', '-ssrR3_70-': '8.020', '-ssrAVE_240-': '6.504', '-ssrAVE_210-': '6.459', '-ssrAVE_180-': '6.456', '-ssrAVE_170-': '6.459', '-ssrAVE_160-': '6.469', '-ssrAVE_110-': '6.728', '-ssrAVE_70-': '8.02', '-ssrSTD_240-': '0.012', '-ssrSTD_210-': '0.009', '-ssrSTD_180-': '0.004', '-ssrSTD_170-': '0.002', '-ssrSTD_160-': '0.002', '-ssrSTD_110-': '0.003', '-ssrSTD_70-': '0.001', '-RESULT_LOC-': 'C:/Users/savanna.c/Downloads', 'Browse': 'C:/Users/savanna.c/Downloads'}

        # # for uclh
        values = {'-DATETIME-': '2023-12-06 20:08:54', 'DATE + TIME': '', '-PERSON1-': 'SavC', '-PERSON2-': '', '-GANTRY-': '3', '-GA-': '0', '-MATERIAL-': 'solid water (RW3)', '-HUMIDITY-': '50.2', '-SSCH-': '3126', '-SS_ELE-': '92580', '-SS_ELE_RANGE-': 'Medium', '-SS_ELE_VOLT-': '-200', '-FCH-': '3128', '-F_ELE-': '92581', '-F_ELE_RANGE-': 'Medium', '-F_ELE_VOLT-': '-200', '-COMMENT-': '', '-NDW-': '0.08470', '-PREV-fNDW-': '0.08320', '-CALC-fNDW-': '0.08328', '-ss_TEMP-': '22.8', '-ss_PRESSURE-': '998.6', '-ss_TPC-': '1.0244', '-ssR1_240-': '6.442', '-ssR1_210-': '6.414', '-ssR1_180-': '6.394', '-ssR1_170-': '6.396', '-ssR1_160-': '6.409', '-ssR1_110-': '6.683', '-ssR1_70-': '8.206', '-ssR2_240-': '6.452', '-ssR2_210-': '6.415', '-ssR2_180-': '6.396', '-ssR2_170-': '6.407', '-ssR2_160-': '6.407', '-ssR2_110-': '6.688', '-ssR2_70-': '8.216', '-ssR3_240-': '6.443', '-ssR3_210-': '6.416', '-ssR3_180-': '6.397', '-ssR3_170-': '6.404', '-ssR3_160-': '6.411', '-ssR3_110-': '6.693', '-ssR3_70-': '8.212', '-ssR4_240-': '6.458', '-ssR4_210-': '6.42', '-ssR4_180-': '6.402', '-ssR4_170-': '6.405', '-ssR4_160-': '6.415', '-ssR4_110-': '6.693', '-ssR4_70-': '8.217', '-ssR5_240-': '6.448', '-ssR5_210-': '6.415', '-ssR5_180-': '6.396', '-ssR5_170-': '6.401', '-ssR5_160-': '6.409', '-ssR5_110-': '6.852', '-ssR5_70-': '8.212', '-ssAVE_240-': '6.449', '-ssAVE_210-': '6.416', '-ssAVE_180-': '6.397', '-ssAVE_170-': '6.403', '-ssAVE_160-': '6.41', '-ssAVE_110-': '6.722', '-ssAVE_70-': '8.213', '-ssSTD_240-': '0.00662', '-ssSTD_210-': '0.00235', '-ssSTD_180-': '0.003', '-ssSTD_170-': '0.00428', '-ssSTD_160-': '0.00303', '-ssSTD_110-': '0.0729', '-ssSTD_70-': '0.00434', '-f_TEMP-': '22.9', '-f_PRESSURE-': '998.6', '-f_TPC-': '1.0247', '-fR1_240-': '6.523', '-fR1_210-': '6.523', '-fR1_180-': '6.504', '-fR1_170-': '6.508', '-fR1_160-': '6.521', '-fR1_110-': '6.805', '-fR1_70-': '8.349', '-fR2_240-': '6.563', '-fR2_210-': '6.525', '-fR2_180-': '6.507', '-fR2_170-': '6.52', '-fR2_160-': '6.526', '-fR2_110-': '6.81', '-fR2_70-': '8.356', '-fR3_240-': '6.56', '-fR3_210-': '6.525', '-fR3_180-': '6.513', '-fR3_170-': '6.519', '-fR3_160-': '6.524', '-fR3_110-': '6.806', '-fR3_70-': '8.36', '-fR4_240-': '6.554', '-fR4_210-': '6.519', '-fR4_180-': '6.507', '-fR4_170-': '6.513', '-fR4_160-': '6.521', '-fR4_110-': '6.801', '-fR4_70-': '8.35', '-fR5_240-': '6.566', '-fR5_210-': '6.527', '-fR5_180-': '6.509', '-fR5_170-': '6.516', '-fR5_160-': '6.525', '-fR5_110-': '6.808', '-fR5_70-': '8.358', '-fAVE_240-': '6.553', '-fAVE_210-': '6.524', '-fAVE_180-': '6.508', '-fAVE_170-': '6.515', '-fAVE_160-': '6.523', '-fAVE_110-': '6.806', '-fAVE_70-': '8.355', '-fSTD_240-': '0.01746', '-fSTD_210-': '0.00303', '-fSTD_180-': '0.00332', '-fSTD_170-': '0.00487', '-fSTD_160-': '0.0023', '-fSTD_110-': '0.00339', '-fSTD_70-': '0.00488', '-ssr_TEMP-': '22.8', '-ssr_PRESSURE-': '998.6', '-ssr_TPC-': '1.0244', '-ssrR1_240-': '6.453', '-ssrR1_210-': '6.41', '-ssrR1_180-': '6.4', '-ssrR1_170-': '6.402', '-ssrR1_160-': '6.407', '-ssrR1_110-': '6.684', '-ssrR1_70-': '8.211', '-ssrR2_240-': '6.452', '-ssrR2_210-': '6.415', '-ssrR2_180-': '6.394', '-ssrR2_170-': '6.401', '-ssrR2_160-': '6.414', '-ssrR2_110-': '6.687', '-ssrR2_70-': '8.216', '-ssrR3_240-': '6.452', '-ssrR3_210-': '6.414', '-ssrR3_180-': '6.395', '-ssrR3_170-': '6.405', '-ssrR3_160-': '6.410', '-ssrR3_110-': '6.684', '-ssrR3_70-': '8.212', '-ssrAVE_240-': '6.452', '-ssrAVE_210-': '6.413', '-ssrAVE_180-': '6.396', '-ssrAVE_170-': '6.403', '-ssrAVE_160-': '6.41', '-ssrAVE_110-': '6.685', '-ssrAVE_70-': '8.213', '-ssrSTD_240-': '0.00058', '-ssrSTD_210-': '0.00265', '-ssrSTD_180-': '0.00321', '-ssrSTD_170-': '0.00208', '-ssrSTD_160-': '0.00351', '-ssrSTD_110-': '0.00173', '-ssrSTD_70-': '0.00265', '-f_ndw_240-': '0.08334', '-f_ndw_210-': '0.08326', '-f_ndw_180-': '0.08323', '-f_ndw_170-': '0.08321', '-f_ndw_160-': '0.08321', '-f_ndw_110-': '0.08346', '-f_ndw_70-': '0.08324', '-RESULT_LOC-': 'C:/Users/KAWCHUNG/Downloads', 'Browse': 'C:/Users/KAWCHUNG/Downloads'}
        # --- trouble-shooting --
        print(f'event: {event}')
        print(f'values: {values}')

        # get current directory, std_eqt.PNG, eqt_ndw.PNG
        home_dir = os.getcwd()
        eqt_ndw_path = os.path.join(home_dir, 'eqt_ndw.PNG')
        eqt_std_path = os.path.join(home_dir, 'eqt_std.PNG')

        print(f'eqt_ndw_path: {eqt_ndw_path}')

        path = values['-RESULT_LOC-']
        os.chdir(path)
        report_dir = os.getcwd()

        # make a folder to store the report
        mdate = str(datetime.strptime(values['-DATETIME-'], '%Y-%m-%d %H:%M:%S').date())
        mdate = mdate.replace('-', '_')

        ss_chamber = values['-SSCH-']
        f_chamber = values['-FCH-']

        folder_name = 'IC_' + mdate + '_SS_' + ss_chamber + '_F_' + f_chamber
        # make a folder
        os.makedirs(folder_name, exist_ok = True)
        os.chdir(os.path.join(path, folder_name))
        report_dir = os.getcwd()

        # create an object for ssChamber
        ssChamber = fn.Chamber('ss', values)
        fChamber = fn.Chamber('f', values)
        ssrChamber = fn.Chamber('ssr', values)

        # 1.) calculate NDW
        # 2.) for any energies out of 2 std of the average value, flag it to operator and re-measure
        fg.plot_drift(ssChamber.nRs, ssChamber.tpc, ssrChamber.nRs, ssrChamber.tpc)
        ss_drift_path = os.path.join(report_dir, 'ss_drift.PNG')

        fg.plot_fndws(values)
        fndws_path = os.path.join(report_dir, 'fndws.PNG')


        # ndw, ndw_outcome = fn.calc_ndw(ssChamber, fChamber, ssrChamber)

        # if ndw_outcome[0] == True:
        #     sg.popup_ok(f'The average ndw from {ndw_outcome[1:]} seems not to be within 2 std of the ndw mean from all other energies. Could you check your measured number/ remeasure those values? ')
        # else:
        #     window.close()

        Report = rp.Report(values, ndw_fetch_msg, eqt_ndw_path, eqt_std_path, ss_drift_path, fndws_path)
        Report.write_report()





# database - session
# date >> op1 >> op2 >> gantry >> material (water/RW3) >> ssChamber >> ss_NDW >> ss_electrometer >> ss_V >> ss_electrometer_range >> f_chamber >> f_NDW >> f_electrometer >> f_V >> f_electrometer_range >> Humidity >> comment >> MPE check
# date >> energy(MeV) >> T >> P >> TPC >> ssR1 >> ssR2 >> ssR3 >> ssR4 >> ssR5 >> ssrT >>ssRrP >> ssrTPC >> ssrR6 >> ssrR7 >>ssrR8 >> ft >> fp >> fTPC >> fR1 >> fR2 >> fR3 >> fR4 >> fR5






if __name__ == '__main__':

    main()
