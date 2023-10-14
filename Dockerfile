FROM continuumio/miniconda3
WORKDIR /app
COPY environment.yml .
RUN conda env create -f environment.yml
COPY . .
EXPOSE 5000
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "auto-trading", "waitress-serve", "--port=5000", "--call", "app:get_app"]