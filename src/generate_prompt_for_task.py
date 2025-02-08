import argparse
import json
import os
import pandas as pd
import random

COLUMNS = ["Name", "Country", "Task", "Prompt"]

def create_prompts(df, task, dir_path):
    f = open(dir_path+"/prompt_template.json")
    prompt_templates = json.load(f)
    df_prompts = pd.DataFrame(columns=COLUMNS)

    for index, row in df.iterrows():
        for task_obj in prompt_templates:
            if(task_obj['task'] == task):
                for i in range(task_obj["no_of_prompt_types"]):
                    df_prompts.loc[len(df_prompts.index)] = [
                        row["Name"],
                        row["Country"],
                        task_obj["task"],
                        random.choice(task_obj["prompt_templates"][i]).format(
                            row["Name"] + ", " + row["Country"])]
                break
    return df_prompts

def main():
    parser = argparse.ArgumentParser(
        description="Enter details to sample locations from the input file and generate prompts."
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Path of the input data, should be in .csv format with atleast two fields representing location name and country.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--task",
        help="Task to create prompts for. Task should be present in prompt_template.json",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--location_column",
        help="Column which denotes the name of the location in the input file",
        default="Name",
    )
    parser.add_argument(
        "-c",
        "--country_column",
        help="Column which denotes the name of the country in the input file",
        default="Country name EN",
    )
    parser.add_argument(
        "-o",
        "--output_filename",
        help="Name for output file",
        default="generated_prompts",
    )
    parser.add_argument(
        "-n",
        "--locations_per_country",
        type=int,
        help="Number of locations to be sampled from every country",
        default=25,
    )
    parser.add_argument(
        "-s",
        "--sampling_seed",
        type=int,
        help="Seed to sample locations",
        default=100,
    )

    args = parser.parse_args()

    try:
        print(f"Reading the input dataset {args.input_file} . . . ")
        df = pd.read_csv(
            args.input_file,
            usecols=[args.location_column, args.country_column],
            sep=";",
        )

        dir_path = os.path.dirname(os.path.realpath(__file__))
        task = args.task
        df.columns.values[0] = "Name"
        df.columns.values[1] = "Country"

        df_sampled = df.groupby("Country").apply(
            lambda x: x.sample(
                args.locations_per_country,
                random_state=args.sampling_seed,
                replace=True,
            )
        )
        df_sampled.drop_duplicates(inplace=True)

        print("Creating prompts ...")
        df_prompts = create_prompts(df_sampled, task, dir_path)
        if(len(df_prompts)==0):
            raise ValueError(f"{task} not found in prompt_template.json")
        df_prompts.to_csv(
            dir_path + f"/{args.output_filename}_" + f"{task}.csv",
            index=False,
            sep=";",
        )
        print(f"Prompts created and saved at {dir_path}/{args.output_filename}_{task}.csv")

    except FileNotFoundError as e:
        print(e)
        print(f"Error: File {args.input_file} not found.")
    except ValueError as err:
        print(err)

if __name__ == "__main__":
    main()
