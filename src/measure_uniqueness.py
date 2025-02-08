import argparse
import os
import pandas as pd

from nltk.corpus import stopwords
s = set(stopwords.words("english"))

def get_uniqueness_score(document_frequency, response_filtered):
    word_count = 0
    score = 0
    for i in response_filtered:
        if i in document_frequency:
            word_count += 1
            score += 1 / document_frequency[i]
    return score / word_count

def calculate_uniqueness(df, document_frequency, response_column):
    total_responses = df.shape[0]
    for index, row in df.iterrows():
        response = row[response_column]
        response = response.lower()
        response_filtered = filter(lambda w: not w in s, response.split())
        score = get_uniqueness_score(document_frequency, response_filtered)
        df.loc[index, "Uniqueness_score"] = score * total_responses

def calculate_document_frequency(df, response_column):
    document_frequency = {}
    for index, row in df.iterrows():
        response = row[response_column]
        response = response.lower()
        response_filtered = set(filter(lambda w: not w in s, response.split()))
        for i in response_filtered:
            if i in document_frequency:
                document_frequency[i] += 1
            else:
                document_frequency[i] = 1
    return document_frequency

def main():
    parser = argparse.ArgumentParser(
        description="Enter details to calculate uniqueness score for each response."
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
        df = pd.read_csv(args.input_file, sep=";")

        if args.response_column not in list(df.columns):
            raise ValueError(
                f"{args.response_column} column is not present in the input file.")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        response_column = args.response_column

        print("Calculating document_frequency ...")
        document_frequency = calculate_document_frequency(df, response_column)

        print("Calculating score ...")
        calculate_uniqueness(df, document_frequency, response_column)

        if args.bool_new_file:
            file = f"{args.input_file}_uniqueness_score.csv"
        else:
            file = f"{args.input_file}"

        df.to_csv(file, index=False, sep=";")
        print(f"Uniqueness score calculated and saved at {file}")

    except FileNotFoundError as e:
        print(f"Error: File {args.input_file} not found.")
    except ValueError as err:
        print(err)


if __name__ == "__main__":
    main()
