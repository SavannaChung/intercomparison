# operators
operators = ['AB', 'AG', 'AGr', 'AK',  'AT', 'AW', 'CB', 'CG', '-KC-', 'KLM', 'PI', 'SC', 'SG', 'TNC', 'VN', 'QK' ]

# gantries
gantries = ['Gantry 1', 'Gantry 2', 'Gantry 3', 'Gantry 4']

gantry_angles = ['0', '90', '180', '270']

# secondary standard ssChamber.
# 3126: water/RW3
# 3132: RW3 only
sschambers = ["3126", "3132"]

# field chamber
fchambers = ["3128", "3131", "3132", "3735", "3736"]

# electrometer
electrometers = ["92579", "92580", "92581"]
ele_ranges = ["Medium", "High", "Low"]

# material
material = ['water', 'solid water (RW3)']

# NDW
# 3126: last calib date = 2023-08-24
# 3132: last calib date = 2021-05-13
ss_ndws = {"3126": 84700000, "3132": 83600000}

# 3128: last calib : 2023-07-18
#3131: last calib: 2023-10-24
f_ndws = {"3128": 83590000, "3131": 83300000, "3132": 83600000, "3735": 0, "3736": 0}

# proton energiesdir
pro_en = ['240', '210', '180', '170', '160', '110', '70']

# # Real proton database. back end.
DATABASE_DIR = r"\\9.40.120.20\\rtassetBE\AssetsDatabase_be.accdb"

# restore to May-2023 working now. cannot connect to database after adding a sheet
# DATABASE_DIR = r"O:\protons\Work in Progress\KC\Access\copies\AssetsDatabaseInProgressSAVANNA.accdb"
# DATABASE_DIR = r"O:\protons\Work in Progress\KC\Access\copies\AssetsDatabaseSAVANNA_be.accdb"

# Add "Roos" table
# DATABASE_DIR = r"O:\protons\Work in Progress\KC\Access\modified_by_KC\AssetsDatabaseSAVANNA_be.accdb"

# round 1 - working
# DATABASE_DIR = r"O:\protons\Work in Progress\KC\Access\modified_by_KC_round1\AssetsDatabaseSAVANNA_be.accdb"
# not working
# DATABASE_DIR = r"C:\Users\KAWCHUNG\OneDrive - NHS\database_assess\AssetsDatabaseSAVANNA_be.accdb"
# DATABASE_DIR = r"C:\Users\KAWCHUNG\Desktop\AssetsDatabaseInProgressSAVANNA.accdb"
#
# PWD = "Pr0ton5%"
PWD = "JoNiSi"
