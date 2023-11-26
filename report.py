import json
# import datetime
import pandas as pd
import os

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, TableStyle, Table, PageBreak, Frame
from  reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm

from reportlab.lib import utils

width, height = letter


def write_report(values):
    ''' prepare the report '''


    # date/ time
    datetime = values['-DATETIME-']

    # operators
    op1 = values['-PERSON1-']
    op2 = values['-PERSON2-']

    # gantry angle
    gantry_angle = values['-GA-']

    report_name = 'IC_G%s_GA%s_%s.pdf' % (values['-GANTRY-'], values['-GA-'], d)

    # values = {'-DATETIME-': '2023-11-24 16:27:30', 'DATE + TIME': '', '-PERSON1-': 'KC', '-PERSON2-': '', '-GANTRY-': '4', '-GA-': '0', '-MATERIAL-': 'solid water (RW3)', '-HUMIDITY-': '50.2', '-SSCH-': '3126', '-SS_ELE-': '92581', '-SS_ELE_RANGE-': 'Medium', '-SS_ELE_VOLT-': '-200', '-FCH-': '3131', '-F_ELE-': '92579', '-F_ELE_RANGE-': 'Medium', '-F_ELE_VOLT-': '-200', '-COMMENT-': '', '-NDW-': '84800000', '-ss_TEMP-': '22.8', '-ss_PRESSURE-': '987.9', '-ss_TPC-': '1.0355', '-ssR1_240-': '6.392', '-ssR1_210-': '6.328', '-ssR1_180-': '6.309', '-ssR1_170-': '6.316', '-ssR1_160-': '6.345', '-ssR1_110-': '6.631', '-ssR1_70-': '8.138', '-ssR2_240-': '6.366', '-ssR2_210-': '6.346', '-ssR2_180-': '6.332', '-ssR2_170-': '6.34', '-ssR2_160-': '6.336', '-ssR2_110-': '6.654', '-ssR2_70-': '8.146', '-ssR3_240-': '6.391', '-ssR3_210-': '6.338', '-ssR3_180-': '6.331', '-ssR3_170-': '6.324', '-ssR3_160-': '6.341', '-ssR3_110-': '6.634', '-ssR3_70-': '8.157', '-ssR4_240-': '6.395', '-ssR4_210-': '6.358', '-ssR4_180-': '6.35', '-ssR4_170-': '6.35', '-ssR4_160-': '6.341', '-ssR4_110-': '6.695', '-ssR4_70-': '8.172', '-ssR5_240-': '6.4', '-ssR5_210-': '6.375', '-ssR5_180-': '6.338', '-ssR5_170-': '6.337', '-ssR5_160-': '6.343', '-ssR5_110-': '6.634', '-ssR5_70-': '8.139', '-ssAVE_240-': '6.389', '-ssAVE_210-': '6.349', '-ssAVE_180-': '6.332', '-ssAVE_170-': '6.333', '-ssAVE_160-': '6.341', '-ssAVE_110-': '6.65', '-ssAVE_70-': '8.15', '-ssSTD_240-': '0.01322', '-ssSTD_210-': '0.01822', '-ssSTD_180-': '0.01492', '-ssSTD_170-': '0.01345', '-ssSTD_160-': '0.00335', '-ssSTD_110-': '0.02699', '-ssSTD_70-': '0.01426', '-f_TEMP-': '22.8', '-f_PRESSURE-': '987.9', '-f_TPC-': '1.0355', '-fR1_240-': '6.506', '-fR1_210-': '6.488', '-fR1_180-': '6.447', '-fR1_170-': '6.473', '-fR1_160-': '6.479', '-fR1_110-': '6.771', '-fR1_70-': '8.316', '-fR2_240-': '6.504', '-fR2_210-': '6.475', '-fR2_180-': '6.45', '-fR2_170-': '6.463', '-fR2_160-': '6.472', '-fR2_110-': '6.777', '-fR2_70-': '8.325', '-fR3_240-': '6.536', '-fR3_210-': '6.521', '-fR3_180-': '6.488', '-fR3_170-': '6.462', '-fR3_160-': '6.473', '-fR3_110-': '6.801', '-fR3_70-': '8.333', '-fR4_240-': '6.531', '-fR4_210-': '6.487', '-fR4_180-': '6.477', '-fR4_170-': '6.471', '-fR4_160-': '6.493', '-fR4_110-': '6.811', '-fR4_70-': '8.355', '-fR5_240-': '6.541', '-fR5_210-': '6.481', '-fR5_180-': '6.467', '-fR5_170-': '6.487', '-fR5_160-': '6.493', '-fR5_110-': '6.808', '-fR5_70-': '8.311', '-fAVE_240-': '6.524', '-fAVE_210-': '6.49', '-fAVE_180-': '6.466', '-fAVE_170-': '6.471', '-fAVE_160-': '6.482', '-fAVE_110-': '6.794', '-fAVE_70-': '8.328', '-fSTD_240-': '0.01736', '-fSTD_210-': '0.01788', '-fSTD_180-': '0.01748', '-fSTD_170-': '0.01006', '-fSTD_160-': '0.01039', '-fSTD_110-': '0.01838', '-fSTD_70-': '0.01729', '-ssr_TEMP-': '22.9', '-ssr_PRESSURE-': '988', '-ssr_TPC-': '1.0357', '-ssrR1_240-': '6.373', '-ssrR1_210-': '6.358', '-ssrR1_180-': '6.318', '-ssrR1_170-': '6.328', '-ssrR1_160-': '6.342', '-ssrR1_110-': '6.642', '-ssrR1_70-': '8.179', '-ssrR2_240-': '6.396', '-ssrR2_210-': '6.373', '-ssrR2_180-': '6.355', '-ssrR2_170-': '6.356', '-ssrR2_160-': '6.354', '-ssrR2_110-': '6.652', '-ssrR2_70-': '8.16', '-ssrR3_240-': '6.383', '-ssrR3_210-': '6.347', '-ssrR3_180-': '6.338', '-ssrR3_170-': '6.338', '-ssrR3_160-': '6.353', '-ssrR3_110-': '6.674', '-ssrR3_70-': '8.156', '-ssrAVE_240-': '6.384', '-ssrAVE_210-': '6.359', '-ssrAVE_180-': '6.337', '-ssrAVE_170-': '6.341', '-ssrAVE_160-': '6.35', '-ssrAVE_110-': '6.656', '-ssrAVE_70-': '8.165', '-ssrSTD_240-': '0.01153', '-ssrSTD_210-': '0.01305', '-ssrSTD_180-': '0.01852', '-ssrSTD_170-': '0.01419', '-ssrSTD_160-': '0.00666', '-ssrSTD_110-': '0.01637', '-ssrSTD_70-': '0.01229', '-f_ndw_240-': '0.08303035976782297', '-f_ndw_210-': '0.0830091944274574', '-f_ndw_180-': '0.08307571534828702', '-f_ndw_170-': '0.08303589859914967', '-f_ndw_160-': '0.08300560986038667', '-f_ndw_110-': '0.08303860964892953', '-f_ndw_70-': '0.0830533853453994', '-RESULT_LOC-': 'C:/Users/KAWCHUNG/Downloads', 'Browse': 'C:/Users/KAWCHUNG/Downloads'}








    return
