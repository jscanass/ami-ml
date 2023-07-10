#!/bin/bash
#SBATCH --partition=unkillable-cpu          # Ask for long job
#SBATCH --cpus-per-task=2                   # Ask for 2 CPUs
#SBATCH --mem=4G                            # Ask for 4 GB of RAM

# 1. Load the required modules
module load anaconda/3

# 2. Load your environment
conda activate milamoth_ai

# 3. Launch your script
cp -r /home/mila/a/aditya.jain/scratch/GBIF_Data/moths_world/* /network/scratch/y/yuyan.chen/moth_world/