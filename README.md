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

We are using the Spacy module for doing the Named Entity Recognition (NER). And because we are analyzing Dutch texts we need to download a Dutch model, in this case the `nl_core_news_lg` model:
```
$ python -m spacy download nl_core_news_lg
```
It will take a short while to download the almost 600MB sized model.

Start the program with:
```
$ python3 ner-not.py some.txt
```

Change the plain text in the `some.txt` file to try out different results for the pipeline.

The pipeline uses the Spacy NER functionality to extract different type of named entities. The extracted entities are fed to the Network of Terms (NoT) to find matching terms. The current program lists the found entities and their type. The reconcilation with the Network of Terms is configured per type. The `config.json` file connects the NER type to the relevant source to query for the Network of Terms.

Bases on the configuration all the NoT sources are queried. The results are processed in the order defined in the config file. As soon as one of the found pref- or altLabels has an exact match with the named entity the URI of this term is return and the processing of the result stops. 

