import standard_benchmark_converter
import argparse
import os

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario_dir", type=dir_path, help="directory containing .scen files Scenario directory")
    parser.add_argument("map_dir", type=dir_path, help="directory contianing .map files Map directory")
    parser.add_argument("output_prefix", type=str, help=".yaml Output file prefix")
    return parser.parse_args()

def run_benchmark_converter_for_all(
        map_path: str,
        map_files: list[str], 
        scenario_path: str,
        scenario_files: list[str], 
        output_prefix: str
        ):
    
    for map_file, scenario_file in zip(map_files, scenario_files):
        if map_file.startswith(scenario_file.split("_")[0]):
            print(f"Matching map and scenario files: {map_file} and {scenario_file}")
            standard_benchmark_converter.main(
                scenario=os.path.join(scenario_path, scenario_file),
                map=os.path.join(map_path, map_file),
                output_prefix=output_prefix + "_" + map_file.split(".")[0] + "_" + scenario_file.split(".")[0]
            )

def get_files_extension(path: str, ext: str) -> list[str]:
    return [f for f in os.listdir(path) if f.endswith(ext)]

def main(scenario_path: str, map_path: str, output_prefix: str):
    scenario_files = get_files_extension(scenario_path, ".scen")
    if len(scenario_files) == 0:
        print("No scenario files found in the directory!")
        exit(-1)
    
    map_files = get_files_extension(map_path, ".map")
    if len(map_files) == 0:
        print("No map files found in the directory!")
        exit(-1)

    run_benchmark_converter_for_all(map_path, map_files, scenario_path, scenario_files, output_prefix) 

if __name__ == "__main__":
    args = setup_args()
    main(args.scenario_dir, args.map_dir, args.output_prefix)