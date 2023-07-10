#!/bin/bash
#SBATCH --partition=main                      # Ask for main job
#SBATCH --cpus-per-task=4                     # Ask for 4 CPUs
#SBATCH --gres=gpu:1                          # Ask for 1 GPU
#SBATCH --mem=4G                              # Ask for 4 GB of RAM


# 1. Load the required modules
module load anaconda/3

# 2. Load your environment
conda activate milamoth_ai

# 4. Launch your script
python 02-calculate_taxa_statistics.py \
--species_list /home/mila/a/aditya.jain/mothAI/species_lists/Barro-Colorado-Island_Moth-List_11January2023.csv \
--write_dir /home/mila/a/aditya.jain/mothAI/gbif_species_trainer/model_training/data/ \
--numeric_labels_filename panama_numeric_labels \
--taxon_hierarchy_filename panama_taxon_hierarchy \
--training_points_filename panama_count_training_points \
--train_split_file /home/mila/a/aditya.jain/mothAI/gbif_species_trainer/model_training/data/01-panama-train-split.csv


