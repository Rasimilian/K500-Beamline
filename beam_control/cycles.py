import argparse
from datetime import datetime
from time import sleep
from pathlib import Path
import json

import pandas as pd
from tqdm import tqdm
from epics import caget, caput

PVS = {"main_current_set": "VEPP4:COCB:H-SP",
       "main_current_read": "VEPP4:COCB:H-RB",
       "time": "VEPP4:COCB:TIME-SP",
       "apply": "VEPP4:COCB:WRITE_PVS-SP"
       }

PVS_DATA = {
    "main_current": "VEPP4:COCB:H-RB",
    "H_I": "VEPP4:CONT:H_I-RB",
    "H_UN": "VEPP4:CONT:H_UN-RB",
    "H_UK": "VEPP4:CONT:H_UK-RB",
    "H_UCAP": "VEPP4:CONT:H_UCAP-RB",
    "H_USO": "VEPP4:CONT:H_USO-RB",
    "H_BIT1": "VEPP4:CONT:H_BIT1-RB",
    "H_STARS": "VEPP4:CONT:H_****-RB",
    "H_IGND": "VEPP4:CONT:H_IGND-RB",
    "ENERGY_SET": "VEPP4:EnergySet-RB",
    "ENERGY_MEAS": "VEPP4:EnergyMeas-RB",
    "IP70_current": "VEPP4:PS70:I-I",

    "NMR_B1": "VEPP4:NMR:B1-RB",
    "NMR_Bcur1": "VEPP4:NMR:Bcur1-RB",
    "NMR_Bmeas1": "VEPP4:NMR:Bmeas1-I",
    "NMR_Bfine1": "VEPP4:NMR:Bfine1-I",
    "NMR_Bmean1": "VEPP4:NMR:Bmean1-I",
    "NMR_Bdev1": "VEPP4:NMR:Bdev1-I",
    "NMR_Bintgr1": "VEPP4:NMR:Bintegral1-I",

    "NMR3_B1": "VEPP4:NMR3:B1-RB",
    "NMR3_Bcur1": "VEPP4:NMR3:Bcur1-RB",
    "NMR3_Bmeas1": "VEPP4:NMR3:Bmeas1-I",
    "NMR3_Bfine1": "VEPP4:NMR3:Bfine1-I",
    "NMR3_Bmean1": "VEPP4:NMR3:Bmean1-I",
    "NMR3_Bdev1": "VEPP4:NMR3:Bdev1-I",
    "NMR3_Bintgr1": "VEPP4:NMR3:Bintegral1-I",

    "NMR3_B2": "VEPP4:NMR3:B2-RB",
    "NMR3_Bcur2": "VEPP4:NMR3:Bcur2-RB",
    "NMR3_Bmeas2": "VEPP4:NMR3:Bmeas2-I",
    "NMR3_Bfine2": "VEPP4:NMR3:Bfine2-I",
    "NMR3_Bmean2": "VEPP4:NMR3:Bmean2-I",
    "NMR3_Bdev2": "VEPP4:NMR3:Bdev2-I",
    "NMR3_Bintgr2": "VEPP4:NMR3:Bintegral2-I",

    "NMR3_B3": "VEPP4:NMR3:B3-RB",
    "NMR3_Bcur3": "VEPP4:NMR3:Bcur3-RB",
    "NMR3_Bmeas3": "VEPP4:NMR3:Bmeas3-I",
    "NMR3_Bfine3": "VEPP4:NMR3:Bfine3-I",
    "NMR3_Bmean3": "VEPP4:NMR3:Bmean3-I",
    "NMR3_Bdev3": "VEPP4:NMR3:Bdev3-I",
    "NMR3_Bintgr3": "VEPP4:NMR3:Bintegral3-I",

    "NMR3_B4": "VEPP4:NMR3:B4-RB",
    "NMR3_Bcur4": "VEPP4:NMR3:Bcur4-RB",
    "NMR3_Bmeas4": "VEPP4:NMR3:Bmeas4-I",
    "NMR3_Bfine4": "VEPP4:NMR3:Bfine4-I",
    "NMR3_Bmean4": "VEPP4:NMR3:Bmean4-I",
    "NMR3_Bdev4": "VEPP4:NMR3:Bdev4-I",
    "NMR3_Bintgr4": "VEPP4:NMR3:Bintegral4-I"
}

CHECKPOINTS_CURRENTS = {700: 50, 950: 30, 1200: 30, 1450: 30, 1700: 30, 1950: 30, 2196: 30,
                        2446: 30, 2696: 30, 2946: 30, 3196: 30, 3446: 30, 3696: 30, 3946: 30,
                        4196: 30, 4446: 30, 4696: 30, 4946: 30, 5196: 30, 5446: 30, 5696: 30,
                        5800: 30}  # Current: transition seconds
#CHECKPOINTS_CURRENTS = {700: 50, 3500: 50, 5800:50}

GLOBAL_CYCLE_CURRENTS = {700: 60, 5800: 50}

# CORRECTION_CYCLE_CURRENTS = {700: 60, 2000: 50, 5800: 50}

TIME_TO_WAIT = 300  # Seconds to stay at checkpoint


def turn_off_corrections():
    caput("VEPP4:COCB:SRX9-SP", 0)
    caput(PVS["time"], 1)
    caput(PVS["apply"], 1)
    sleep(2)


def get_nmr_data(element: str, data: list, current: float):
    data_per_checkpoint = {"element": element,
                           "time": str(datetime.now()),
                           "element_current_set": current}
    for param, pv in PVS_DATA.items():
        data_per_checkpoint[param] = caget(pv)

    data.append(data_per_checkpoint)

def make_field_prediction(current: float):
    """Set starting value as NMR prediction"""

    pvs =["VEPP4:NMR:B1-SP",
	  "VEPP4:NMR3:B1-SP",
          "VEPP4:NMR3:B2-SP",
          "VEPP4:NMR3:B3-SP",
          "VEPP4:NMR3:B4-SP",
          "VEPP4:NMR2:B1-SP",
          "VEPP4:NMR2:B2-SP",
          "VEPP4:NMR2:B3-SP",
          "VEPP4:NMR2:B4-SP"
]
    # Formula from v4 site
    field = 1849.8 + 0.8243 * (current - 2200)
    for pv in pvs:
        caput(pv, field)
    caput(PVS["time"], 1)
    caput(PVS["apply"], 1)
    sleep(2)


def make_cycles_main(num: int):
    """Make magnetic cycling of main field"""

    current_current = caget("VEPP4:COCB:H-RB")
    current_time = 60

    for _ in tqdm(range(num)):
        current = 5800
        time = GLOBAL_CYCLE_CURRENTS[current]
        caput(PVS["main_field"], current)
        caput(PVS["time"], time)
        caput(PVS["apply"], 1)
        sleep(time)
        sleep(15)

        current = 700
        time = GLOBAL_CYCLE_CURRENTS[current]
        caput(PVS["main_current_set"], current)
        caput(PVS["time"], time)
        caput(PVS["apply"], 1)
        sleep(time)
        sleep(15)

        caput(PVS["main_current_set"], current_current)
        caput(PVS["time"], current_time)
        caput(PVS["apply"], 1)
        sleep(current_time)
        sleep(15)


def make_cycles_correction(num: int):
    """Make magnetic cycling of SRX9"""

    print("SRX9 cycling")

    pv = "VEPP4:COCB:SRX9-RB"
    current_current = caget(pv)
    max_current = 8
    time = 5

    pv = "VEPP4:COCB:SRX9-SP"
    for _ in tqdm(range(num)):
        caput(pv, max_current)
        caput(PVS["time"], time)
        caput(PVS["apply"], 1)
        sleep(time)
        sleep(2)

        caput(pv, -max_current)
        caput(PVS["time"], 2 * time)
        caput(PVS["apply"], 1)
        sleep(2 * time)
        sleep(2)

        caput(pv, current_current)
        caput(PVS["time"], time)
        caput(PVS["apply"], 1)
        sleep(time)
        sleep(2)


def measure_nmr_main() -> list:
    """Measure Main Field"""
    print("Measruing nmr main field")

    turn_off_corrections()

    current_current = caget(PVS["main_current_read"])
    checkpoints = {key: val for key, val in CHECKPOINTS_CURRENTS.items() if key > current_current}
    checkpoints.update({key: val for key, val in CHECKPOINTS_CURRENTS.items() if key <= current_current})
    if current_current not in checkpoints:
        checkpoints.update({current_current: 30})

    data = []
    for current, time in tqdm(checkpoints.items()):
        caput(PVS["main_current_set"], current)
        caput(PVS["time"], time)
        caput(PVS["apply"], 1)
        sleep(time)
        sleep(TIME_TO_WAIT)
        make_field_prediction(current)
        get_nmr_data("H", data, current)

    checkpoints = dict(sorted(CHECKPOINTS_CURRENTS.items(), reverse=True))
    if current_current not in checkpoints:
        checkpoints.update({current_current: 30})
    for current, time in tqdm(checkpoints.items()):
        caput(PVS["main_current_set"], current)
        caput(PVS["time"], time)
        caput(PVS["apply"], 1)
        sleep(time)
        sleep(TIME_TO_WAIT)
        make_field_prediction(current)
        get_nmr_data("H", data, current)

    return data


def measure_nmr_correction() -> list:
    """Measure field of SRX9"""
    print("Measuring SRX9 field")

    current_h_field = 2000
    caput(PVS["main_current_set"], current_h_field)
    caput(PVS["time"], 30)
    caput(PVS["apply"], 1)
    sleep(30)

    pv = "VEPP4:COCB:SRX9-RB"
    current_current = caget(pv)
    data = []
    checkpoints_tmp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -7, -6, -5, -4, -3, -2, -1, 0]
    checkpoints = [i for i in checkpoints_tmp if i > current_current]
    checkpoints += [i for i in checkpoints_tmp if i <= current_current]
    if current_current not in checkpoints:
        checkpoints += [current_current]

    pv = "VEPP4:COCB:SRX9-SP"
    for current in tqdm(checkpoints):
        caput(pv, current)
        caput(PVS["time"], 1)
        caput(PVS["apply"], 1)
        sleep(2)
        make_field_prediction(current_h_field)
        sleep(80)
        get_nmr_data("SRX9", data, current)

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-cm', '--cycle_main', type=str, action='store', default=False,
                       help='Main cycle')
    parser.add_argument('-cc', '--cycle_correction', type=str, action='store', default=False,
                        help='Correction cycle')
    parser.add_argument('-mm', '--measure_main', type=str, action='store', default=False,
                        help='Measure main field')
    parser.add_argument('-mc', '--measure_correction', type=str, action='store', default=False,
                        help='Measure correction field')
    parser.add_argument('-f', '--file', type=str, action='store', default="nmr_res.json",
                        help='File to save')

    cmd_args = parser.parse_args()
   # file = Path(cmd_args.file).absolute()
    file = cmd_args.file.split(".json")[0]

    if cmd_args.cycle_main == "True":
        make_cycles_main(6)
    elif cmd_args.cycle_correction == "True":
        make_cycles_correction(6)
    else:
        print("No cycling")

    data = None
    if cmd_args.measure_main == "True":
        data = measure_nmr_main()
    elif cmd_args.measure_correction == "True":
        data = measure_nmr_correction()
    else:
        print("Nothing to measure and save")

    if data:
        data = pd.DataFrame(data)
        time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        data.to_csv(f'{time}_{file}.csv', sep='\t')

        print("Done!") 
