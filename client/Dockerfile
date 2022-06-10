FROM condaforge/miniforge3:latest

COPY environment.yml /tmp/environment.yml

RUN conda env update --name base --file /tmp/environment.yml && \
    rm /tmp/environment.yml

CMD ["/bin/bash"]