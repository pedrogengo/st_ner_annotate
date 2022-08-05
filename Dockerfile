FROM nikolaik/python-nodejs:python3.7-nodejs16-slim
ADD . .

RUN apt-get update && apt-get install sudo

RUN pip install -U pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN poetry run pip install -U streamlit

RUN python -m spacy download en_core_web_sm

WORKDIR /st_ner_annotate/frontend
RUN npm uninstall node-sass
RUN npm install sass
RUN npm install
RUN npm run build

EXPOSE 5000
EXPOSE 8501

ENTRYPOINT npm start & streamlit run ../__init__.py
