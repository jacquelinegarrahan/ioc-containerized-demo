FROM condaforge/miniforge3:latest

COPY environment.yml /tmp/environment.yml
COPY demo-server /demo/demo-server
COPY example_ioc.py /demo/example_ioc.py

RUN conda env update --name base --file /tmp/environment.yml && \
    rm /tmp/environment.yml && \
    pip install /demo/demo-server

CMD ["python", "/demo/example_ioc.py"]