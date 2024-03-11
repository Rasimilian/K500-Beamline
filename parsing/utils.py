from typing import List, Tuple


class Sequence:
    def __init__(self,
                 elem_defs: List[Tuple[int, str, str, float]],
                 elem_seq: List[int],
                 seq_str: str):
        self.elem_defs = elem_defs
        self.elem_seq = elem_seq
        self.seq_str = seq_str


def ring_to_madx(file: str, save: bool = False, file_to_save: str = None, verbose: bool = False) -> Sequence:
    """
    Convert structure in the RING format to the MAD-X format.
    """
    with open(f"{file}", "r") as f:
        text = f.readlines()

    for idx, line in enumerate(text):
        if "[End OF STR" in line:
            start_elem = idx + 2
        if "[  end of elm" in line:
            end_elem = idx
        if "Energy of injection" in line:
            HR = float(line.split("=")[1].split()[0])
        if "STRUCTURE " in line:
            start_seq = idx + 1
        if "[End OF STR" in line:
            end_seq = idx

    seq: List[int] = []
    for idx, line in enumerate(text[start_seq:end_seq]):
        ll = line.split()
        if "[" in line:
            ll = [int(i) for i in ll[:-1]]
        else:
            ll = [int(i) for i in ll]
        seq += ll

    elem_def: List[Tuple[int, str, str, float]] = []
    edge_count = 0
    quad_cnt = 0
    for idx, line in enumerate(text[start_elem:end_elem]):
        ll = line.split()
        if "S" not in ll:
            continue
        else:
            num = int(ll[0])
        if "S" in ll:
            index_val_len = ll.index("S") + 1
            length = round(float(ll[index_val_len]) / 100, 6)
            if "G" in ll and "H" in ll:
                index_val_grad = ll.index("G") + 1
                index_val_field = ll.index("H") + 1
                name = line.split("[")[1].split()[0]
                angle = round(float(ll[index_val_field]) * length / HR * 1e2, 6)
                k1 = round(float(ll[index_val_grad]) / HR * 1e4, 6)
                elem = f"el.{name}: sbend,l= {length}, angle= {angle}, k1= {k1};\n"
            elif "G" in ll and "edge" not in line:
                index_val_grad = ll.index("G") + 1
                if "[" in line:
                    name = line.split("[")[1].split()[0]
                else:
                    quad_cnt += 1
                    name = f"quad_{quad_cnt}"
                k1 = round(float(ll[index_val_grad]) / HR * 1e4, 6)
                elem = f"el.{name}: quadrupole,l= {length}, k1= {k1};\n"
            elif "HZ" in ll:
                index_val_field = ll.index("HZ") + 1
                name = line.split("[")[1].split()[0]
                angle = round(float(ll[index_val_field]) * length / HR * 1e2, 6)
                elem = f"el.{name}: sbend,l= {length}, angle= {angle};\n"
            elif "H" in ll:
                index_val_field = ll.index("H") + 1
                name = line.split("[")[1].split()[0]
                angle = round(float(ll[index_val_field]) * length / HR * 1e2, 6)
                elem = f"el.{name}: sbend,l= {length}, angle= {angle};\n"
            elif "HX" in ll:
                index_val_field = ll.index("HX") + 1
                name = line.split("[")[1].split()[0]
                angle = round(float(ll[index_val_field]) * length / HR * 1e2, 6)
                elem = f"el.{name}: sbend,l= {length}, angle= {angle}, tilt= pi/2;\n"
            elif "edge" in line:
                edge_count += 1
                index_val_grad = ll.index("G") + 1
                name = f"edge_{edge_count}"
                k1 = round(float(ll[index_val_grad]) / HR * 1e4, 6)
                elem = f"el.{name}: quadrupole,l= {length}, k1= {k1};\n"
            else:
                elem = "drift"
                elem_def.append((num, "", elem, length))
                continue
            elem_def.append((num, elem, f"el.{name}", length))

    structure = "".join([i[1] for i in elem_def]) + "k500: sequence, l = total_length;\n"
    pos = 0
    for idx in seq:
        for (num, elem, name, length) in elem_def:
            if idx == num:
                if name != "drift":
                    loc = f"{name}, at = {round(pos + length / 2, 6)};\n"
                    pos += length
                    structure += loc
                else:
                    pos += length

    structure = structure.replace("total_length", str(round(pos, 6))) + "endsequence;"

    if verbose:
        print(structure)

    if save:
        with open(file_to_save, "w") as f:
            f.write(structure)

    sequence = Sequence(elem_defs=elem_def,
                        elem_seq=seq,
                        seq_str=structure)

    return sequence
