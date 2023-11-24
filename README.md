# ner-not-pipeline
NER and Network-of-Terms pipeline

Basic experiment for creating an NER pipeline in combination with querying the [NDE Netwerk of Terms](https://github.com/netwerk-digitaal-erfgoed/network-of-terms). NER code based on the Hands-On 1.2 code from the [Open HPI Knowledge Graph Course 2023](https://open.hpi.de/courses/knowledgegraphs2023).

It is recommended to use a virtual environment, create one using the following command:
```sh
$ python3 -m venv ./venv
```
Then activate the virtual evironment using:
```sh
$ source venv/bin/activate
```
This will result in a prompt starting with `(venv)`, the virtual environment is now activated.

Now install the requirend packages:
```sh
$ pip install -r requirements.txt
```
This will result in list of packages that are being installed and it should end with no errors.

We are using the Spacy module for doing the Named Entity Recognition (NER). And because we are analyzing Dutch texts we need to download a Dutch model, in this case the 'nl_core_news_lg' model:
```
$ python -m spacy download nl_core_news_lg
```
It will take a short while to download the almost 600MB sized model.
