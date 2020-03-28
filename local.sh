BUCKET=ds-playground

python3 dataflow_main.py \
  --job_name squash-robin \
  --project podiq-265304 \
  --setup_file ./setup.py \
  --staging_location gs://$BUCKET/squash-robin/staging \
  --temp_location gs://$BUCKET/squash-robin/temp \
  --coordinate_output gs://$BUCKET/squash-robin/out \
  --extra_package pytorch-bert-pretrained.tar.gz
  #--grid_size 2
  #--runner DataflowRunner \
  #--requirements_file requirements.txt
