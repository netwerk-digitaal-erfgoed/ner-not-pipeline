from python_graphql_client import GraphqlClient
import spacy
import json
import sys
from spacy.matcher import Matcher

if len(sys.argv) == 1:
  print("Please give filename of textfile to process...")
  sys.exit()
  
filename = sys.argv[1]
configFile = open('config.json')
config=json.load(configFile)

with open(filename) as f:
    text = f.read()

# Specify the Network-of-Terms GraphQL API
client = GraphqlClient(endpoint="https://termennetwerk-api.netwerkdigitaalerfgoed.nl/graphql")

def queryTN(sources,searchTerm):

    # Prepare the search query
    query = """
      query tn($sources: [ID]!, $searchTerm: String!) {
        terms( sources: $sources, query: $searchTerm ) {
          result {
            __typename
            ... on Terms {
              terms { uri prefLabel altLabel hiddenLabel scopeNote seeAlso }
            }
            ... on Error {
              message
            }
          }
        }
      }
    """

    # Perform a synchronous request for simplicity
    return client.execute(query=query, variables= {"sources": sources, "searchTerm": searchTerm })

def matchLabel(labels,searchLabel):
  for label in labels:
    if label.strip().lower() == searchLabel:
      return label
  return False

def Refine(ner,nerType):

  # only proces nerTypes that are defined in the config file
  if not (nerType in config):
    return False

  # use source selection from the config.json
  sourceList=config[nerType]

  # perform Network of Terms request for this NER
  data=queryTN(sourceList,ner)

  # select the resultLists per source
  resultList = data['data']['terms']
  for results in resultList:
    if(results['result']['__typename']=="Terms"):
      terms=results['result']['terms']
      for term in terms:
        found=matchLabel(term['prefLabel'],ner)
        if(found):
          return term
        found=matchLabel(term['altLabel'],ner)
        if(found):
          return term
  return False

def processKeywords():
  token_details = []
  print("Processing keywords: ",end="")
  for token in doc:
    if(token.pos_=="NOUN"):
      if not token.text in termList:
        print(".",end="",flush=True)
        termFound=Refine(token.text,"CONCEPT")
        if(termFound):
        
          #print("TOKEN: Found matching URI:",termFound['uri'],"with prefLabel",termFound['prefLabel'],"for",token.text)
          termList[token.text]=termFound
  print("\nKeywords processing finshed!")

def processNERs():
  ner_details = []
  for ent in doc.ents:
    row=(ent.text, ent.label_,spacy.explain(ent.label_))
    if not (row in ner_details):
      ner_details.append(row)

  print("Processing named entities: ",end="")
  for row in ner_details:
    ner=row[0].strip().lower()
    nerType=row[1]
    if not ner in termList:
      print(".",end="",flush=True)
      termFound=Refine(ner,nerType)
      if(termFound):
        termList[ner]=termFound

        #print("NER: Found matching URI:",termFound['uri'],"with prefLabel",termFound['prefLabel'],"for",ner,)
  print("\nNER processing finished!")

def writeCSV():
  outFile=filename.rsplit('.',1)[0] + '.csv'
  with open(outFile,"w") as fileHandle:
    for term in termList:
      print(
        term +";"+
        termList[term]['uri'] +";"+ 
        ', '.join(termList[term]['prefLabel']) +";"+
        ', '.join(termList[term]['altLabel']) +";"+
        ', '.join(termList[term]['scopeNote']),
        file=fileHandle
      )
  print("Results written to",outFile)

# load a Dutch language model
nlp = spacy.load("nl_core_news_lg")

# process the text read from the specified input file
doc = nlp(text)

# initialize resultlist
termList = {}

# find relevant concepts URIs based on the nouns in the text
processKeywords()

# find relevant URIs for locations and persons based
# on the namend entities in the text
processNERs()

# write resultlist out as CSV file
writeCSV()