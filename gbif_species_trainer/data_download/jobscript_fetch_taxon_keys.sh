#!/bin/bash
#SBATCH --partition=long-cpu                # Ask for long job
#SBATCH --cpus-per-task=1                     # Ask for 2 CPUs
#SBATCH --mem=4G                              # Ask for 4 GB of RAM

# 1. Load the required modules
module load anaconda/3

# 2. Load your environment
conda activate milamoth_ai

# 3. Launch your script
python 01-fetch_taxon_keys.py \
--species_filepath /home/mila/a/aditya.jain/mothAI/species_lists/Moths_of_Barro_Colorado_Island_1673275447.csv \
--column_name ScientificName \
--output_filepath /home/mila/a/aditya.jain/mothAI/species_lists/Barro-Colorado-Island_Moth-List_25Apr2023.csv \
--place panama_11Jan2023