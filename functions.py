import pandas as pd
import PySimpleGUI as sg
import database as db
from datetime import datetime
import PySimpleGUI as sg
import re

import config as cg

def calc_sample_std(list):
    ''' calculate the standard deviation of a sample in a list'''
    mean = sum(list)/len(list)

    # sum of all difference squared
    soads = sum([(l - mean)**2 for l in list])
    std = (soads/(len(list)-1))**0.5

    std = round(std, 5)

    return std

def is_float(num):
    ''' check whether the entry is a float '''
    try:
        float(num)
        return True
    except ValueError:
        return False

def calc_tpc(temp, pressure):
    '''
    temp = temperature
    pressure = hPa
    tpc = temperature-pressure correction factor

    '''
    tpc = (1013.25/pressure)*(273.2 + temp)/(273.2 + 20)
    tpc = round(tpc, 4)

    return tpc

def make_blocks(prefix, pro_en, nM, s):
    ''' prefix = string -SS for secondary standard, -F for Field
        pro_en = proton energy
        nM = no. measurement (int)
        s = size of input text in tuple

    '''
    # create top row for temperature, pressure and TPC
    factors = {'TEMP': 'T(°C): ', 'PRESSURE':'P(mbar): ', 'TPC': 'TPC: '}
    top_row = []
    for key, val in factors.items():
        k = '-'+ prefix +'_'+ key+'-'
        if key == 'TPC':
            top_row.append(sg.Text(factors[key], size = (7,1), font = ('Bold', 9), justification = 'left'))
            top_row.append(sg.InputText(key = k, size = (7,1), enable_events = True, readonly = True))
        else:
            top_row.append(sg.Text(factors[key], size = (7,1), font = ('Bold', 9), justification = 'left'))
            top_row.append(sg.InputText(key = k, size = (7,1), enable_events = True))

    block = []
    nitems = [str(n) for n in range(1, nM+1)]
    nitems.append('AVE')
    nitems.append('STD')

    # create a dictionary
    s = (5, 1)
    dict = {}
    for n in nitems:
        if n not in ['AVE','STD']:
            dict.update({prefix+'R'+n: [[sg.Text(prefix+'R'+n, size = s)]]})
        else:
            dict.update({prefix+n: [[sg.Text(prefix+n, size =s )]]})

    KEYS = list(dict.keys())

    # creates coloumns for the block
    ens = (7, 1)
    energy = [[sg.Text('En(MeV)', size = ens)]]

    for en in cg.pro_en:
        energy.append([sg.Text(en, size = ens)])

    for k in KEYS:
        for en in cg.pro_en:
            sk = '-' + k + '_' + en + '-'
            # "do not edit" the AVE and STD cells
            if 'AVE' in sk or 'STD' in sk:
                dict[k].append([sg.InputText(key = sk, size =s, enable_events=True, readonly = True)])
            else:
                dict[k].append([sg.InputText(key = sk, size =s, enable_events=True)])

    return energy, top_row, dict

def make_GUI(theme):
    """ make a gui for data-entering

    """
    # define the theme
    sg.theme('DefaultNoMoreNagging')

    # chambers
    sschambers = cg.sschambers
    fchambers = cg.fchambers

    #electrometer
    electrometers = cg.electrometers

    # # proton energy

    #operators
    operators = db.fetch_db(cg.DATABASE_DIR, 'Operators', 'Initials', PWD=cg.PWD)
    if operators == False:
        sg.popup_yes_no("Unable to fetch operators from database. \n Operator list may not be up to date.", title = "YesNo")
        operators = cg.operators

    print(operators)

    # electrometer range
    # ele_ranges = cg.ele_range

    # NDW calibration factor
    cal_factor = db.fetch_ndw(cg.DATABASE_DIR, table_name='Calibration', col='CalFactor', col_1='Equipment' ,chno='%_3126_%', col_2 = 'Cal Date',  PWD=cg.PWD)
    if cal_factor == False:
        sg.popup_yes_no("Unable to fetch NDW from database. \n ", title = "YesNo")
        ndw_fetch_msg = 'Unable to fetch NDW factor from database. PLEASE check the chamber specific NDW factor on iPASSPORT.'
    else:
        ndw_fetch_msg = 'NDW factor sucessfully fetched from database.'


    # # GUI

    # for column 1
    current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    date = [sg.Text('Date/ time:', size = (10, 1)), \
            sg.InputText(key='-DATETIME-', default_text = current_datetime, size = (17,1), enable_events=True)]
    datetime_button = [sg.Text('', size = (10, 1)), sg.CalendarButton(button_text = 'DATE + TIME', target = '-DATETIME-',close_when_date_chosen = True, format = "%Y-%m-%d %H:%M:%S", size = (17, 1), font = ('MS Sans Serif', 5, 'bold'), location = (0,0))]
    person_1 = [sg.Text('Operator 1: ', size = (10,1)), sg.Combo(values= operators, key = '-PERSON1-', size = (10,1), enable_events=True)]
    person_2 = [sg.Text('Operator 2: ',  size = (10,1)), sg.Combo(values= operators, key = '-PERSON2-',  size = (10,1), enable_events=True)]


    # for column 2

    gantries = [sg.Text('Gantry: ',  size = (10,1)), sg.Combo(values= cg.gantries, key = '-GANTRY-',  size = (10,1))]
    gantry_angles = [sg.Text('Gantry angle: ',  size = (10,1)), sg.Combo(values = cg.gantry_angles, key = '-GA-', default_value = '0', size = (10,1))]
    material = [sg.Text('Material: ', size = (10,1)), sg.Combo(values= cg.material, key = '-MATERIAL-', size = (10,1), enable_events=True)]
    humidity =  [sg.Text('Humidity (%): ',  size = (10,1)), sg.InputText(key = '-HUMIDITY-',  size = (10,1))]

    # for column 3 (secondary standard)
    ssch = [sg.Text('Chambers (secondary standard): ', size = (24,1)), sg.Combo(values= sschambers, key = '-SSCH-', size = (7,1), enable_events=True)]
    ss_electrometers = [sg.Text('Electrometers (ss): ', size = (24,1)), sg.Combo(values= electrometers,  key = '-SS_ELE-', size = (7,1))]
    ss_ele_range = [sg.Text('Electrometer range (ss): ', size = (24,1)), sg.Combo(values= cg.ele_ranges,  key = '-SS_ELE_RANGE-', default_value = "Medium", size = (7,1))]
    ss_ele_voltage = [sg.Text('Electrometer voltage (ss,V): ', size = (24,1)), sg.InputText(key = '-SS_ELE_VOLT-', default_text = '-200', size = (7,1))]

    # for column 4 (field)
    fch = [sg.Text('Chambers (Field): ', size = (24,1)), sg.Combo(values= fchambers,  key = '-FCH-', size = (7,1))]
    f_electrometers = [sg.Text('Electrometers (f): ', size = (24,1)), sg.Combo(values= electrometers,  key = '-F_ELE-', size = (7,1))]
    f_ele_range = [sg.Text('Electrometer range (f): ', size = (24,1)), sg.Combo(values= cg.ele_ranges,  key = '-F_ELE_RANGE-', default_value = "Medium", size = (7,1))]
    f_ele_voltage = [sg.Text('Electrometer voltage (f, V): ', size = (24,1)), sg.InputText(key = '-F_ELE_VOLT-', default_text = '-200', size = (7,1))]

    # add comments
    comment =  [sg.Text('Comment:', size = (10, 1))]
    comment_input = [sg.Multiline(key = '-COMMENT-', size = (70,30), expand_x=True)]
    comments = [comment, comment_input]

    # meausrement details
    col_1 = [ date, datetime_button, person_1, person_2]
    col_2 = [ gantries, gantry_angles, material, humidity]
    col_3 = [ ssch, ss_electrometers, ss_ele_range, ss_ele_voltage]
    col_4 = [ fch, f_electrometers, f_ele_range, f_ele_voltage]



    # NDW factor
    # add ndw text to the GUI. Flag it as red if fetching NDW from database is not sucessful.
    # set InputText to state = 'disabled' to freeze the cell (no changes )
    if cal_factor == False:
        ndw_text = [sg.Text(ndw_fetch_msg, font = ('MS Sans Serif', 5, 'bold'), text_color='red')]
        ndw = [sg.Text('ssNDW: ', size=(10,1)), sg.InputText(key = '-NDW-',  size = (10,1), readonly = True)]
    else:
        ndw_text = [sg.Text(ndw_fetch_msg, font = ('MS Sans Serif', 5, 'bold'), text_color='blue')]
        ndw = [sg.Text('ssNDW: ', size=(10,1)), sg.InputText(key = '-NDW-', default_text = str(cal_factor[0]), size = (10,1), readonly = True)]


    # information layout
    layout = [
            [sg.Frame('Measurement details: ', [[sg.Column(col_1, justification ='left'), sg.Column(col_2, justification ='left'), sg.Column(col_3, justification ='left'), sg.Column(col_4, justification ='left'), sg.Column(comments, justification = 'left')]], size = (1700, 150))],
            [sg.Frame('ss NDW calibration factor', [ndw_text, ndw], size = (1700, 80))]
            ]

    ## data entry
    parameters = {'ss':5, 'f':5, 'ssr':3}
    s = (5, 1)

    frames = []
    for key, val in parameters.items():
        # put the first to fifth readings + ave + std into coluns
        energy, top_row, dict = make_blocks(key, cg.pro_en, val, (5, 1))

        # make blocks for ss, field and ssr measurement
        mea_cols = [sg.Column(energy, justification = 'left')]
        for k in dict.keys():
            c = dict[k]
            mea_cols.append(sg.Column(c, justification = 'left'))

        # make TPC row
        tpc_frame = [sg.Frame('TPC', [top_row], size = (530, 50))]
        # make frame for ss, field and ssr measurements

        # define the gui frame size based on the reading
        if key == 'ssr':
            frames.append(sg.Frame(key +'_measurement', [tpc_frame, mea_cols], size = (430, 300)))
        else:
            frames.append(sg.Frame(key +'_measurement', [tpc_frame, mea_cols], size = (550, 300)))

    # make a f_ndw colume to auto calculate F_NDW

    # re-create the energy column for the ndw frame as same element cannot be use twice in the layout
    ens = [[sg.Text('En(MeV)', size = (7,1))]]
    for e in cg.pro_en:
        ens.append([sg.Text(e, size = (5, 1))])

    ndw_frame = [sg.Frame('NDW', [[sg.Text('unit: Gy/nC', font = ('MS Sans Serif', 6, 'bold'))]], size = (150, 50))] # make the frame same size as the TPC to keep formal

    ndws = [[sg.Text('NDW',  font = ('MS Sans Serif', 4, 'bold'))]]

    for en in cg.pro_en:
        k = '-f_ndw' + '_' + en + '-'
        ndws.append([sg.InputText(key = k, size = s, enable_events=True, readonly = True)])

    ndw_block = [sg.Column(ens, justification = 'left'), sg.Column(ndws, justification = 'left')]
    fndw_frame = sg.Frame('Results', [ndw_frame, ndw_block], size = (150, 300))

    # add ndw columns to the measurement blocks (ss + f + ssr measurements)
    frames.append(fndw_frame)
    layout.append(frames)

    # report saving location frame
    loc = [sg.Text('Report location:', size = (24, 1))]
    browse_loc = [sg.InputText(key = '-RESULT_LOC-'), sg.FolderBrowse()]
    loc_frame = [sg.Frame('Location', [loc, browse_loc], size = (1700, 100))]

    # append the location
    layout.append(loc_frame)

    # # add measurement blocks into the GUI
    # # Buttons
    button_exit = [sg.Button('Exit')]
    button_submit = [sg.Button('Submit')]
    button_check = [sg.Button('Check Data')]


    layout.append([button_check, button_submit + button_exit])

    window =sg.Window('Chamber intercomparison:', layout)
    # window = sg.Window('test', layout1)


    while True:
        event, values = window.read()
        print(f'event: {event}')
        print(f'values: {values}')

        if event == sg.WINDOW_CLOSED or event == 'Exit' or event == 'Submit':
            window.close()
            break

        # updating the GUI according to GUI input

        # if -DATETIME- is triggered, ensure it is in "%Y-%m-%d %H:%M:%S"
        if event == '-DATETIME-':
            try:
                datet = datetime.strptime(values['-DATETIME-'], '%Y-%m-%d %H:%M:%S')
            except:
                sg.popup_ok('Your datetime format does not match YYYY-MM-DD hh:mm:ss. PLease re-entre the datetime.')

    # if -MATERIAL- is 'water', set the -SSCH- to '3126' and update the NDW
        if event == '-MATERIAL-':
            if values['-MATERIAL-'] == 'water':
                window['-SSCH-'].update('3126')
                window['-NDW-'].update(str(cg.ndw['3126']))

    # if op1 is empty and op2 is not
        if event =='-PERSON2-':
            try:
                if not values['-PERSON1-']:
                    sg.popup_ok('Please fill operator 1 first. ')

            except:
                print(f'Fail to detect operator 2.')


    # if -SSCH- is '3132', set the -MATERIAL- to 'solid water (RW3)'
        if event == '-SSCH-':
            if values['-SSCH-'] == '3132':
                window['-MATERIAL-'].update('solid water (RW3)')
                window['-NDW-'].update(str(cg.ndw['3132']))
            elif values['-SSCH-'] == '3126':
                window['-NDW-'].update(str(cg.ndw['3126']))

        if 'PRESSURE' in event:
            try:
                p = event.split('_')[0][1:]

                # test whether the entries are string
                ts = '-' + p + '_' + 'TEMP-'
                ps = '-' + p + '_' + 'PRESSURE-'
                tpcs = '-' + p + '_' + 'TPC-'

                # calculate TPC
                # check temperature and pressure is a float
                check_temp = is_float(values[ts])
                check_pressure = is_float(values[ps])

                if check_temp == False or check_pressure == False:
                    sg.popup_ok('Your temperature/ pressure entry is not a float. Please correct it!')

                if check_temp == True and check_pressure ==  True:
                    tpc = calc_tpc(float(values[ts]), float(values[ps]))
                    window[tpcs].update(str(tpc))
            except:
                print(f'fail to update -TPC-')

        # automatically update AVE and STD
        if bool(re.search('R[123456]', event)) == True:
            try:
                # check all reading are float
                check_meas = is_float(values[event])

                if check_meas == False and values[event] != "":
                    sg.popup_ok(f'Your {event} entry is not a float. Please correct it!')

                # calculate the average and std of the measured values
                # meanwhile, check the number of measurements per energy
                if check_meas == True:
                    nM, en = event.split('_') # get the no of measurements
                    nM = nM[-1]
                    en = en[:-1]
                    prefix = event.split('R')[0][1:]

                    if  int(nM)>2 or int(nM) ==2: # calculate the AVE when nM >=2
                        items = range(1, int(nM)+1)
                        nitems = len(items)
                        nC = []
                        for i in items:
                            key = '-' + prefix + 'R' + str(i)+ '_' + en + '-'
                            nC.append(float(values[key]))

                        ave = sum(nC)/ len(nC) # average nC measured
                        ave = round(ave, 3)

                        k = '-' + prefix + 'AVE'+ '_' + en + '-'
                        window[k].update(ave)

                    if int(nM) >3 or int(nM)==3: #student t-test with n-1 degrees of freedom, n>3 to calculate standard devivation
                        k_std =  '-' + prefix + 'STD'+ '_' + en + '-'
                        std = calc_sample_std(nC)
                        window[k_std].update(std)

            except:
                print(f'fail to update the -AVE- and -STD-')


        # # check operator input 5 for ss, 5 for f and 3 for ssr
        # if  event == 'Check Data': # last entry
        #
        #     # check ndw measured
        #     try:
        #         ssChamber = Chamber('ss', values)
        #         fChamber = Chamber('f', values)
        #         ssrChamber = Chamber('ssr', values)
        #
        #         ndw, ndw_outcome = calc_ndw(ssChamber, fChamber, ssrChamber)
        #
        #         print(f'ndw:{ndw}')
        #         print(f'ndw_outcome: {ndw_outcome}')
        #
        #         if ndw_outcome[0] == True:
        #             sg.popup_ok(f'The average ndw from {ndw_outcome[1:]} seems not to be within 2 std of the ndw mean from all other energies. Could you check your measured number/ remeasure those values? ')
        #     except:
        #         print(f'fail to calculate NDW')

        if bool(re.search('-ssrR3_', event)) == True:
            try:
                # get energy
                en = event.split('_')[1][:-1]

                parameters = {'ss':5, 'f':5, 'ssr':3}
                ss_tot = []
                f = []

                for k in list(parameters.keys()):
                    RoM = range(1, parameters[k]+1) # range of measurement
                    for n in RoM:
                        key = '-' + k + 'R' + str(n) + '_' + en + '-'
                        if values[key] != "": # if the entry is not empty
                            # calculate TPC corrected nR
                            key_tpc = '-' + k + '_TPC-'
                            tpc = float(values[key_tpc]) # get tpc
                            nR_tpc_corr = tpc*float(values[key]) # corrected ready with TPC

                            if k == 'ss' or k == 'ssr':
                                ss_tot.append(nR_tpc_corr)
                            elif k == 'f':
                                f.append(nR_tpc_corr)

                print(f'ss_tot: {ss_tot}')
                print(f'f: {f}')
                print(f'ssr energy: {en}')

                # calculate the average
                ss_ave = round(sum(ss_tot)/len(ss_tot), 5)
                f_ave = round(sum(f)/len(f), 5)

                print(f'ss_ave:{ss_ave} , f_ave:{f_ave}')

                f_ndw = (float(values['-NDW-'])*1e-9)*ss_ave/f_ave

                print(f'f_ndw: {f_ndw}')

                key_fndw = '-f_ndw' + '_' + en + '-'
                window[key_fndw].update(str(f_ndw))







            except:
                print(f'fail to calculate ndw')
        # window.close()

    return event, values, ndw_fetch_msg, window

class Chamber:
    def __init__(self, prefix, values):
        self.prefix = prefix
        self.temp = float(values['-' + self.prefix +'_TEMP-'])
        self.pressure = float(values['-' + self.prefix +'_PRESSURE-'])
        self.tpc = float(values['-' + self.prefix +'_TPC-'])

        if prefix == 'f':
            self.chamber_no = values['-' + self.prefix.upper()+ 'CH-' ]
            self.electrometer = values['-' + self.prefix.upper() + '_ELE-']
            self.ele_range = values['-' + self.prefix.upper() + '_ELE_RANGE-']
            self.voltage = values['-' + self.prefix.upper() + '_ELE_VOLT-']

        else:
            self.chamber_no = values['-SSCH-' ]
            self.electrometer = values['-SS_ELE-']
            self.ele_range = values['-SS_ELE_RANGE-']
            self.voltage = values['-SS_ELE_VOLT-']
            self.ssndw = float(values['-NDW-'])


        if prefix == 'ssr':
            nM = range(1, 4)
        else:
            nM = range(1, 6)

        nR_dict = {}
        for en in cg.pro_en:
            ls = []
            for n in nM:
                k = '-' + self.prefix + 'R' + str(n) + '_' + en + '-'
                v = values[k]
                ls.append(float(v))

            nR_dict.update({en: ls})

        self.nRs = nR_dict

def calc_ave_std(dict, tpc):
    ''' calculate the average and std for each proton energy
    the ave_nR is corrected for TPC
    '''
    d_ave = {}
    d_std = {}

    for en in cg.pro_en:
        a = tpc*sum(dict[en])/len(dict[en])
        d_ave.update({en: a})

        s = calc_sample_std(dict[en])
        d_std.update({en:s})

    return d_ave, d_std

def calc_ndw(ss, f, ssr):
    ''' ss, f and ssr : objects Chamber
        we applied tpc correction on the nR from ss and ssr chamber.
        we calculate the ave, std from the combined nR (sst_nR = ss + ssr)
        if ndw is > pm 2 std, flag energies
    '''

    # merge the ss results. ss_tot = ss + ssr
    ss_tot = {} # contain all nR data from ss chamber
    sst_ave = {} # store the average nR per energy data from ss_tot
    sst_std = {} # store the std nR per energy data from ss_tot

    for en in cg.pro_en:
        l = []
        for val in ss.nRs[en]:
            cnR = val*ss.tpc # tpc corrected nR
            l.append(cnR)

        for v in ssr.nRs[en]:
            c_nR = val*ss.tpc # tpc corrected nR
            l.append(c_nR)

        ss_tot.update({en:l})

        ave = sum(l)/len(l)
        sst_ave.update({en:ave})

        std = calc_sample_std(l)
        sst_std.update({en:std})

    # calculate average TPC corrected nR from field chamber
    f_ave, f_std = calc_ave_std(f.nRs, f.tpc)

    print(f'f_ave: {f_ave}')
    print(f'f_std: {f_std}')

    # calculate ndw
    ndw = {}
    for en in cg.pro_en:
        n = (ss.ssndw)*(sst_ave[en]/f_ave[en])*1e-9
        n = round(n, 5)
        ndw.update({en:n})

    print(f'fn.ndw: {ndw}')

    # check all values are within 2 std
    # output the energy (ies) that does not lie within 2 std
    ndw_std = calc_sample_std(list(ndw.values()))

    ndws = list(ndw.values())
    ave_ndw = sum(ndws)/len(ndws)

    print(f'ndws: {ndws}')
    print(f'ave_ndw: {ave_ndw}')
    print(f'ndw_std:{ndw_std}')

    tol = 2*ndw_std
    print(f'tol: {tol}')
    print(f'ave_ndw + tol :{ave_ndw + tol}')
    rmea_en = []
    for en in cg.pro_en:
        if ndw[en] > ave_ndw + tol or ndw[en] < ave_ndw - tol:
            rmea_en.append(en)

    ndw_outcome = []
    if rmea_en:
        ndw_outcome.append(True)
        ndw_outcome.extend(rmea_en)
    else:
        ndw_outcome.append(False)







    #
    # print(f'sst_ave: {sst_ave}')
    # print(f'f_ave: {f_ave}')
    # print(f'ndw: {ndw}')

    # calculate the average nR from ss_tot

    # sst_ave, sst_std = calc_ave_std()
    ## assign those things to a variable to avoid update the object
    # ss_ave, ss_std = calc_ave_std(ss.nRs, ss.tpc)
    # f_ave, f_std = calc_ave_std(f.nRs, f.tpc)
    # ssr_ave, ssr_std = calc_ave_std(ssr.nRs, ssr.tpc)
    #
    # # considering all ss measurement for ndw calculation
    # ndw = {}
    # for e in cg.pro_en:
    #     # calculate the average nR from ss + ssr
    #     v = (ss_ave[e] + ssr_ave[e])/2
    #
    #     fndw = (v/f_ave[e])*(ss.ssndw *1e-9)
    #     ndw.update({e: fndw})

    return ndw, ndw_outcome
