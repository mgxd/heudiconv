#!/bin/bash

set -eu

VER=$(grep -Po '(?<=^__version__ = ).*' ../heudiconv/info.py | sed 's/"//g')

image="kaczmarj/neurodocker:0.4.3"

docker run --rm $image generate docker -b neurodebian:stretch -p apt \
    --dcm2niix version=v1.0.20181125 method=source \
    --install git gcc pigz liblzma-dev libc-dev git-annex-standalone netbase \
    --copy . /src/heudiconv \
    --miniconda use_env=base conda_install="python=3.6 traits>=4.6.0 scipy numpy nomkl pandas" \
      pip_install="/src/heudiconv[all]" \
      pip_opts="--editable" \
    --entrypoint "heudiconv" \
> ../Dockerfile
