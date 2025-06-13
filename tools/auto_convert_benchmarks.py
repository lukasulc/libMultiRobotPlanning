import os
import glob
import subprocess
import argparse
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser(description="Auto convert MAPF benchmarks to YAML.")
    parser.add_argument("--map", type=str, required=True, help="Path to the .map file")
    parser.add_argument("--scen_dir", type=str, default="../mapf-scen-random/scen-random/", help="Directory with .scen files")
    parser.add_argument("--output_base", type=str, default="./examples/ground/", help="Base output directory")
    parser.add_argument("--count", type=int, default=400, help="Max number of agents to generate problems for")
    return parser.parse_args()

def get_prefix(filename):
    base = os.path.basename(filename)
    return os.path.splitext(base)[0]

def main(args):
    map_file = args.map
    if not os.path.isfile(map_file):
        print(f"Map file '{map_file}' not found!")
        return

    prefix = get_prefix(map_file)
    scen_pattern = os.path.join(args.scen_dir, f"{prefix}*.scen")
    scen_files = glob.glob(scen_pattern)
    if not scen_files:
        print(f"No scenario files found with prefix '{prefix}' in {args.scen_dir}")
        return

    for scen in scen_files:
        scen_base = os.path.basename(scen)
        # Remove prefix and extension, then strip any leading separator
        suffix = scen_base[len(prefix):].replace(".scen", "")
        suffix = suffix.lstrip("-_ ")
        out_dir = os.path.join(args.output_base, prefix, suffix)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        output_prefix = os.path.join(out_dir, "inputs")
        print(f"Converting: {scen} + {map_file} -> {output_prefix}_N_agents.yaml")
        subprocess.run([
            "python3",
            "libMultiRobotPlanning/example/standard_benchmark_converter.py",
            scen,
            map_file,
            output_prefix,
            "--count", str(args.count)
        ], check=True)

if __name__ == "__main__":
    main(get_args())