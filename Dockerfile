FROM continuumio/miniconda3

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
#RUN conda create -n DrIP python
#ENV PATH /opt/conda/envs/DrIP/bin:$PATH
#RUN /bin/bash -c "source activate DrIP"

RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH

#RUN conda env update --name DrIP --file environment.yml

WORKDIR /application

CMD python run.py