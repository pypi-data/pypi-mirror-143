# fastai_prims

This repository contains a primitive that makes use of the [fastai library](https://www.fast.ai/). Hosted on PyPi [here](https://pypi.org/project/fastai-prims/).

Step 1: Run `docker pull registry.gitlab.com/datadrivendiscovery/images/primitives:ubuntu-bionic-python38-master`

Step 2: Run `docker image ls` and take note of the id for the ubuntu-bionic-python38-master image 

Step 3: Run `docker run -t -i -v <path to datasets folder on local machine>:/mnt/datasets <id of image> /bin/bash`
        Make sure to substitute the path to your datasets folder ([ex. D3M Datasets](https://datasets.datadrivendiscovery.org/d3m/datasets)) and the id of your docker image.
        ** FOR GPU support, add the `--gpus=all` flag: `docker run -t -i --gpus=all -v <path to datasets folder on local machine>:/mnt/datasets <id of image> /bin/bash`

The above command should have launched you into the Docker container.

** All steps below will be run within the Docker container **

Step 4: Run `mkdir /static`

Before running the next step, see the **NOTE below if you are a developer on this primitive.

Step 5: Run `python3 -m d3m primitive download -p d3m.primitives.classification.Convolutional_neural_network.Fastai -o /static`

Step 6: Run `git clone https://gitlab.com/datadrivendiscovery/primitives.git` in home directory

Step 7: To execute the pipeline, from home directory run the command below, substituting the path to the dataset you want

    python3 -m d3m runtime --volumes /static fit-score \
            --pipeline primitives/primitives/JPL_manual/d3m.primitives.classification.Convolutional_neural_network.Fastai/0.1.0/pipelines/pipeline.json \
            --problem /mnt/datasets/seed_datasets_current/<dataset name here>/TRAIN/problem_TRAIN/problemDoc.json \
            --input /mnt/datasets/seed_datasets_current/<dataset name here>/TRAIN/dataset_TRAIN/datasetDoc.json \
            --test-input /mnt/datasets/seed_datasets_current/<dataset name here>/TEST/dataset_TEST/datasetDoc.json \
            -a /mnt/datasets/seed_datasets_current/<dataset name here>/SCORE/dataset_SCORE/datasetDoc.json
            -c <any name here>.csv;

Step 8: If desired, modify hyperparameters for the Fastai primitive in the pipeline.json file passed above

**NOTE : To install the latest version of the primitive (if changes in this repo have not yet been published to the public D3M primitives registry or PyPi), run:

1) `git clone https://gitlab.com/datadrivendiscovery/fastai_prims.git`

2) Run `pip install -e fastai_prims/`

**NOTE 2 : For GPU support, install the CUDA versions of torch manually with
`pip install torch==1.7.0+cu110 torchvision==0.8.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html`
