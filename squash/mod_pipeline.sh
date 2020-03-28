#!/bin/bash
#
#SBATCH --job-name=job_doc2qa
#SBATCH -o /mnt/nfs/work1/miyyer/kalpesh/projects/squash-generation/logs/log_doc2qa.txt
#SBATCH --time=24:00:00
#SBATCH --partition=1080ti-long
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=12GB
#SBATCH --open-mode append
#SBATCH -d singleton

echo "Run $var ..."
echo 'Choosing instance from QuAC dev set ...'
#KEY=$(python3 squash/populate_input.py)
KEY='quac_475'
echo $KEY

echo 'Extracting answers ...'
python3 squash/extract_answers.py --key $KEY

echo 'Generating questions ...'
python3 question-generation/mod_interact.py --key $KEY

echo 'Running QA module ...'
python3 question-answering/mod_run_squad.py 

echo 'Combining Q and A ...'
python3 squash/combine_qa.py --key $KEY

echo 'Filtering bad Q/As ...'
python3 squash/filter.py --key $KEY
