# Uncovering Geographical Disparities in Generated Stories and Travel Recommendations

The repository would contain the code for the following paper: 

> Richer Output for Richer Countries: Uncovering Geographical Disparities in Generated Stories and Travel Recommendations
> by Kirti Bhagat, Kinshuk Vasisht, Danish Pruthi. 
> Findings of North American Chapter of the ACL (NAACL 2025)
> [Paper Link](https://arxiv.org/abs/2411.07320)

We examine large language models for two common scenarios that require geographical knowledge (a) travel recommendations and (b) geo-anchored story generation.

## Setup Environment
1. Create a conda environment and install dependencies:
```
conda create -n geo-disparities
conda activate geo-disparities
pip install -r requirements.txt
```

2. Download the list of all cities with a population > 1000 through geonames: [link](https://download.geonames.org/export/dump/cities1000.zip)

## Prompt Creation
Script to sample locations and create prompts can be found at `src/generate_prompt_for_task.py`. Provide file path to the geonames dataset downloaded in the previous step as input. You should also provide the task name (story_generation or travel_recommendation) for which you want to prompts to be created.

Example:
```
python src/generate_prompt_for_task.py --input_file path/to/dataset.csv --task story_generation
```

Running the above would generate a file `generated_prompts.csv` with additional columns of `task` and `prompt`. For proper usage instructions  kindly refer to the `--help` option:
```
python src/generate_prompt_for_task.py --help
```

## Evaluation
We evaluate responses from models on three attributes, namely uniqueness, informativeness and emotions (for stories generated) which can be calculated using the following scripts:
1. Uniqueness: `src/measure_uniqueness.py` 
2. Informativeness: `src/measure_informativeness.py`
3. Emotion: `src/extract_emotions.py`

The input file should contain the `response` column for which the attribute needs to be calculated. For proper usage instructions  kindly refer to the `--help` option.
Running the evaluation scripts will modify the input csv file by adding a column for the attribute value measured.