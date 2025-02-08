import argparse
import en_core_web_trf
import os
import pandas as pd
import spacy
from tqdm import tqdm

from spacy.language import Language

SPACY_MODEL = 'en_core_web_trf'
NLP = spacy.load(SPACY_MODEL, disable = ['tagger', 'parser', 'attribute_ruler', 'lemmatizer'])
print(NLP.pipe_names)

def extract_spatial_entities(text):
    doc = NLP(text)
    doc.ents = [ent for ent in doc.ents if ent.label_ == 'LOC' or ent.label_ == 'FAC' or ent.label_ == 'GPE']
    return doc
 
def count_geo_entities(df, response_column):
    for index, row in tqdm(df.iterrows(),total=df.shape[0]):
        location_name = row['Name']
        country_name = row['Country']
        reponse = row[response_column]
        entities = extract_spatial_entities(reponse.replace("||||","\n")).ents
        entities = [p.text.strip(" ").strip("the").strip(" ") for p in entities]
        entity_set = set(entities)
        if(location_name in entity_set):
            entity_set.remove(location_name)
        if(country_name in entity_set):
            entity_set.remove(country_name)
        df.loc[index, "Informativeness"] = len(set(entity_set))
       
def main():
    parser = argparse.ArgumentParser(
        description="Enter details to calculate Informativeness (Count of geo-entities) for each response."
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

        print("Calculating geo entities ...")
        count_geo_entities(df, response_column)

        if args.bool_new_file:
            file = f"{args.input_file}_informativeness_score.csv"
        else:
            file = f"{args.input_file}"

        df.to_csv(file, index=False, sep=";")
        print(f"Informativeness score calculated and saved at {file}")

    except FileNotFoundError as e:
        print(f"Error: File {args.input_file} not found.")
    except ValueError as err:
        print(err)


if __name__ == "__main__":
    main()
