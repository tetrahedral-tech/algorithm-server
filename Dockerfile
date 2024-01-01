FROM continuumio/miniconda3
WORKDIR /app:get_app
COPY environment.yml .
RUN conda env create -f environment.yml

COPY . .
WORKDIR /app/src
EXPOSE 80
CMD ["conda", "run", "--no-capture-output", "-n", "auto-trading", "waitress-serve", "--port=80", "--call", "app:get_app"]
