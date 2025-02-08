import argparse
import pandas as pd
import os
import asyncio
from tqdm import tqdm
import utils

assistant_prompt ='''Help me identify which of the following emotions: Joy, Hardships, Fear, Sadness, Serenity;
are recognized within the story given in the prompt. Only output the names of the emotions found in the prompt.'''

config = {
    'model_name': "gpt-4",
    'max_tokens': 50,
    'temperature': 0.7,
    'request_timeout': 60,
}

async def extract_emotions(df, response_column, model_config, file):
    for index, row in tqdm(df.iterrows()):
        gpt4_response = await utils.get_gpt4_response(model_config, assistant_prompt, row[response_column])
        df.loc[index, 'Emotions'] = gpt4_response
        df.to_csv(file, index=False, sep=";")

def main():
    parser = argparse.ArgumentParser(
        description="Enter details to extract emotions from each response."
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Path of the data file, should be in .csv format with seperator as ';', with atleast one field representing response from model.",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--response_column",
        help="Column which denotes the model response in the input file",
        default="Response",
    )
    parser.add_argument(
        "-b",
        "--bool_new_file",
        type=bool,
        help="If results should be put in a new file",
        default=False,
    )
    args = parser.parse_args()

    try:
        print(f"Reading the input dataset {args.input_file}")
        df = pd.read_csv(
            args.input_file,
            sep=";",
        )

        if args.response_column not in list(df.columns):
            raise ValueError(
                f"{args.response_column} column is not present in the input file.")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        response_column = args.response_column
        if args.bool_new_file:
            file = f"{args.input_file}_emotions.csv"
        else:
            file = f"{args.input_file}"

        print("Extracting emotions ...")

        asyncio.run(extract_emotions(df, response_column, config, file))
        df.to_csv(file, index=False, sep=";")

    except FileNotFoundError as e:
        print(f"Error: File {args.input_file} not found.")
    except ValueError as err:
        print(err)


if __name__ == "__main__":
    main()
