FROM continuumio/miniconda3

RUN conda create -n DrIP python=3.6
ENV PATH /opt/conda/envs/DrIP/bin:$PATH
RUN /bin/bash -c "source activate DrIP"

RUN conda env update --name DrIP --prefix ./env --file environment.yml --prune