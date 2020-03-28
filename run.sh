BUCKET=ds-playground

python3 dataflow_main.py \
  --job_name squash-robin \
  --project podiq-265304 \
  --runner DataflowRunner \
  --staging_location gs://$BUCKET/squash-robin/staging \
  --temp_location gs://$BUCKET/squash-robin/temp \
  --coordinate_output gs://$BUCKET/squash-robin/out \
  --machine-type n1-standard-4 \
  --save-main-session true
  #--setup_file ./setup.py 
  #--template_location gs://$BUCKET/squash-robin/templates/
  #--requirements_file requirements.txt
  #--extra_package pytorch-bert-pretrained.tar.gz
  #--grid_size 2
