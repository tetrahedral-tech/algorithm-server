FROM continuumio/miniconda3
WORKDIR /app
COPY environment.yml .
RUN conda env create -f environment.yml

COPY . .
EXPOSE 80
RUN cd src/
CMD ["conda", "run", "--no-capture-output", "-n", "auto-trading", "cd", "src", "&&" "waitress-serve", "--port=80", "--call", "app:get_app"]
