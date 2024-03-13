import json
from copy import deepcopy
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from epics import PV

_K500_BPMS = ["DT11", "DT12", "DT13"]
_VEPP3_BPMS = ["1P7"]
_KNOBS = {"K500": {"Xe_pos": "CHAN:BPM_NAME:Xu-I",
                   "Ye_pos": "CHAN:BPM_NAME:Yu-I",
                   "Ie_pos": "CHAN:BPM_NAME:Iu-I"},
          "VEPP3": {"Xe_pos": "VEPP3:BPM_NAME:X-I",
                    "Ye_pos": "VEPP3:BPM_NAME:Y-I",
                    "Ie_pos": "VEPP3:BPM_NAME:I-I"},
          }


class Data(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    time: List[str] = []
    y: List[float] = []
    x: List[float] = []
    i: List[float] = []
    best_shot_num: int = None


class PickupPVs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    x: PV
    y: PV
    i: PV


class BeamStats:
    bpms: List[str]
    history: Dict[str, Data]
    best_shot_num: int
    pvs: Dict[str, PickupPVs]
    bpm_for_callback: str

    def __init__(self):
        self.bpms = _K500_BPMS + _VEPP3_BPMS
        self.history = {bpm: Data() for bpm in self.bpms}
        self.best_shot_num = 0
        self.pvs = {}
        self.bpm_for_callback = _K500_BPMS[-1]

    def connect(self):
        for bpm in self.bpms:
            if bpm in _K500_BPMS:
                facility = "K500"
            elif bpm in _VEPP3_BPMS:
                facility = "VEPP3"
            else:
                raise ValueError(f"Unknown BPM: {bpm}")
            x = PV(_KNOBS[facility]["Xe_pos"].replace("BPM_NAME", bpm))
            y = PV(_KNOBS[facility]["Ye_pos"].replace("BPM_NAME", bpm))
            i = PV(_KNOBS[facility]["Ie_pos"].replace("BPM_NAME", bpm))
            x.connect()
            y.connect()
            i.connect()
            self.pvs[bpm] = PickupPVs(x=x, y=y, i=i)

        self.pvs[self.bpm_for_callback].x.add_callback(self.get_bpm_data)

    def disconnect(self):
        self.pvs[self.bpm_for_callback].x.clear_callbacks()

    def get_bpm_data(self, pvname=None, value=None, char_value=None, **kw):
        time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        for bpm in self.bpms:
            self.history[bpm].x.append(self.pvs[bpm].x.value)
            self.history[bpm].y.append(self.pvs[bpm].y.value)
            self.history[bpm].i.append(self.pvs[bpm].i.value)
            self.history[bpm].time.append(time)
            if bpm == "1P7":
                self._filter_bpm_data(bpm)
            self.find_best_passing(bpm)

    def find_best_passing(self, bpm: str):
        max_current = max(self.history[bpm].i)
        max_current_id = self.history[bpm].i.index(max_current)
        self.history[bpm].best_shot_num = max_current_id

    def _filter_bpm_data(self, bpm: str):
        if len(self.history[bpm].i) == 1:
            self._last_current_val = self.history[bpm].i[0]
            self.history[bpm].i[0] = 0
        else:
            delta = self.history[bpm].i[-1] - self._last_current_val
            self._last_current_val = self.history[bpm].i[-1]
            self.history[bpm].i[-1] = delta if delta > 0 else 0

    def save_data(self, comment: str, auto_save: bool = False):
        history = deepcopy(self.history)
        for bpm in self.bpms:
            history[bpm] = history[bpm].model_dump(mode="json")

        time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        Path("log/").mkdir(exist_ok=True)

        with open(f'log/{time}_passing{comment}.json', 'w') as f:
            json.dump(history, f, indent=2)
