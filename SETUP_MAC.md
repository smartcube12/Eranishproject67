# ERAN on Mac notes (Leo)

Got ERAN running on my M4 Mac with Docker. Took a while, writing down what I had to change.

Docker: turn off "Use Rosetta for x86_64/amd64 emulation" in Settings > General. With it on, tensorflow crashes with "Illegal instruction".

    docker run -it --platform linux/amd64 --name eran -v ~/eran-project:/work ubuntu:20.04 bash

Inside the container:

    apt-get update
    apt-get install -y git wget sudo m4 build-essential autoconf libtool python3 python3-pip python3-dev
    cd /opt && git clone https://github.com/eth-sri/ERAN.git && cd ERAN
    bash ./install.sh
    source gurobi_setup_path.sh
    pip3 install -r requirements.txt

Then had to downgrade some stuff because onnx 1.8 breaks with the newer versions:

    pip3 install numpy==1.23.5 protobuf==3.20.3

Also changed line 21 in tf_verify/tensorflow_translator.py to
`from tensorflow.compat.v1 import graph_util`
(the old import doesn't exist in TF2)

Each time I go back into the container I run `source gurobi_setup_path.sh` from /opt/ERAN first.

refinepoly doesn't work yet, needs a gurobi license. The normal academic one doesn't work in docker, have to figure that out.

## first test

mnist_relu_3_50, eps 0.03, 20 images (19 classified correctly)

- deeppoly: 8/19 verified, ~10s
- deepzono: 7/19 verified, ~18s

at eps 0.005 everything verifies so you need a bigger epsilon to see differences
