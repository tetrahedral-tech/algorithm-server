FROM continuumio/miniconda3
WORKDIR /app
COPY environment.yml .
RUN conda env create -f environment.yml

COPY . .
EXPOSE 80
WORKDIR /app/src
ENV WSGI 1
CMD ["conda", "run", "--no-capture-output", "-n", "auto-trading", "gunicorn", "app:get_app", "--config", "config.py"]
