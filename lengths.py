import json
from multiprocessing import Pool
from Bio.PDB import PDBParser
import pandas as pd
import pathlib
import random
import string
import os


pdbparser = PDBParser()

def file_op(file_path):
    filename = pathlib.Path(file_path).stem
    random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    struc = pdbparser.get_structure(random_id, file_path)
    length = len([i for i in struc.get_residues()])
    return filename, file_path, length

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("dir")

    args = parser.parse_args()

    files = os.listdir(args.dir)
    files = (os.path.join(args.dir, i) for i in files)

    with Pool() as p:
        results = p.map(file_op, files)

    result = pd.DataFrame(results, columns=["name", "path", "length"])
    result.to_csv("lengths.csv")

