''' This Project will be amazing more or less from the greek wine group

Using Ogimet to get a METAR/TAF
and check for correct METAR & TAF using DWD-Guidelines (btw use .txt-file) ??'''


import datetime as dt
from urllib import request
import urllib.request
import os

def Generate_request(icao:str,name:str,auto:bool,
        year:int,month:int,day:int,hour:int,minute:int,
        year_f:int,month_f:int,day_f:int,hour_f:int,minute_f:int
    ) -> str:
        #Set conditions...
        base_url = 'https://www.ogimet.com/display_metars2.php?'
        lang = 'en'    #Language
        tipo = 'ALL'
        ord = 'REV'
        nil = 'SI'                             # INCLUDE NIL-Messages
        fmt = 'txt'                            # File-Format from OGIMET
        send = 'send'
        #Create URL
        url = (base_url+'lang='+lang+'&lugar='+icao
               +'&tipo='+tipo+'&ord='+ord+'&nil='+nil+'&fmt='+fmt
               +'&ano='+f'{year}'+'&mes='+f'{month:02d}'+'&day='+f'{day:02d}'+'&hora='+f'{hour:02d}'
               +'&anof='+f'{year_f}'+'&mesf='+f'{month_f:02d}'+'&dayf='+f'{day_f:02d}'
               +'&horaf='f'{hour_f:02d}'+'&minf='+f'{minute_f}'+'&send='+send)

        #url_old = ('https://www.ogimet.com/display_metars2.php?lang=en&lugar=EDDw&tipo=ALL&ord=REV&nil=SI&fmt=txt'
        #       '&ano=2025&mes=04&day=15&hora=07&anof=2025&mesf=04&dayf=16&horaf=07&minf=59&send=send')

        #print(url_old)

        return url

def Get_file(url:str,icao:str,
             year:int,month:int,day:int,hour:int,minute:int,
             year_f:int,month_f:int,day_f:int,hour_f:int,minute_f:int
    ) -> str:
    ''' This Function gets the requested METAR/TAF file in the txt-format from OGIMET and download it to reduce
    unwanted requests, if you test with the same file.'''

    print("Try Connect to Ogimet.. This might take a while...")

    d_path = (icao
              + f'{year}' + '_'
              + f'{month:02d}' + '_'
              + f'{day:02d}' + '_'
              + f'{hour:02d}' + '_'
              + f'{minute:02d}' + '_'
              + f'{year_f}' + '_'
              + f'{month_f:02d}' + '_'
              + f'{day_f:02d}' + '_'
              + f'{hour_f:02d}' + '_'
              + f'{minute_f:02d}'
              + '.txt')
    print(d_path)

    if os.path.exists(d_path) == False:
        connect_to_url = request.urlopen(url)
        url_status = connect_to_url.code
        if url_status == 200:
            print('Download file')
            urllib.request.urlretrieve(url, d_path)  # This Command save the file into the folder...
            print('Download finished!')
            return d_path
        else:
            print("Source is offline or something went wrong!")
            print(url_status)
            return d_path
    else:
        print('File already exists! No Download...')
        return d_path

def Gen_Metar_from_file(path:str):
    ''' This Function will generate the METAR & TAF from the OGIMET-File and return a METAR-LIST and TAF-LIST '''

    with open(path,'r') as afile:
          for line in afile:
            if '#' in line[0]:
                print(line)



date = dt.date.today()
print(date.strftime('%a %d %b %Y %H:%M'))

url = Generate_request('EDDW','Bremen',True,
                               2025,6,7,11,0,
                               2025,6,8,9,59
                               )

path = Get_file(url,'EDDW',2025,6,7,11,0,
                               2025,6,8,9,59)

Gen_Metar_from_file(path)

# FX,FF,DD
# DD > 60° wenn ff >= 5 KT
# FF >= 5 KT
# BÖE: positive Abweichung von FF>10 KT, wenn t >= 3s
#
# Forcasted Fx oder change of windspeed of forecasted FX um >= 10 KT,
# if FF after change >= 15KT forecasted
#
# VIS-Tresholds :
# -- : >
# ++ : <=
# 0150
# 0350
# 0600
# 0800
# 1500
# 3000
# 5000
# WW:
# (+ /nothing/ -)
# MI/BC/PR/DR/BL/SH/TS/FZ
# DZ/RA/SN/SG/PL/GR/GS/UP
# BR/FG/FU/VA/DU/SA/HZ
# PO/SQ/FC/SS/DS
# TRESHOLD :
# + or nothing
# ever FZ (Freezing)
# ever TS
# SQ (ff >= 16KT increasing >= 21 KT)
# FC
# Other Weather if VIS > 5000
# CLOUDS/COVER
# SKC/NSC 0/8 or Clouds over 5000 FT
# FEW 1/8
# SCT 2/8-4/8
# BKN 5/8-7/8
# OVC 8/8
# If Cloudiness change from FEW/SCT/NSC/SKC to BKN/OVC or the other way around
# and Cloudbase (Ceiling change to treshold)
# Cloudbase (CIG):
# -- : >
# ++ : <=
# 001
# 002
# 005
# 010
# 015
# SPECIAL CASE : VV  (vertical viewrange)
# CAVOK if VIS> 9999 and NSC!

