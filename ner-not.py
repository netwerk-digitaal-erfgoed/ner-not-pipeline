from python_graphql_client import GraphqlClient
import spacy
import json

configFile = open('config.json')
config=json.load(configFile)

with open('some.txt') as f:
    text = f.read()

# Specify the Network-of-Terms GraphQL API
client = GraphqlClient(endpoint="https://termennetwerk-api.netwerkdigitaalerfgoed.nl/graphql")

def queryTN(sources,searchTerm):

    #print("Query NoT with",searchTerm,"and",sources)
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
  #print("Find exact match in results for",searchLabel,"...")
  for label in labels:
    #print("Test",label,"...")
    if label.strip().lower() == searchLabel:
      return label
  return False

def Refine(ner,nerType):

  if not (nerType in config):
    print(row[1],"not in configfile")
    return False

  # use source selection from the config.json
  sourceList=config[nerType]
  #print("using the followin sources",sourceList)

  # perform Network of Terms request for this NER
  data=queryTN(sourceList,ner)

  # select the resultLists per source
  resultList = data['data']['terms']
  for results in resultList:
     
    # select list of terms from the resultset
    terms=results['result']['terms']
    for term in terms:
    #print("Process term",term)
    #print("Find matching prefLabel...")
      found=matchLabel(term['prefLabel'],ner)
      if(found):
        #print("Found",found,"in prefLabel for",term['uri'])
        return term['uri']
      #print("Find matching altLabel...")
      found=matchLabel(term['altLabel'],ner)
      if(found):
        #print("Found",found,"in altLabel for",term['uri'])
        return term['uri']
      
  return False


nlp = spacy.load("nl_core_news_lg")
#doc = nlp('Haarlem behoort tot de middelgrote steden in de Randstad. Tot de gemeente Haarlem behoren de stad Haarlem en het westelijke deel van het dorp Spaarndam. Haarlem telt 165.650 inwoners[1] en is daarmee na Amsterdam de grootste stad van Noord-Holland en de dertiende gemeente van Nederland. De grootstedelijke agglomeratie Haarlem (Haarlem, Heemstede, Bloemendaal en Zandvoort) telt ongeveer 235.000 inwoners,[1] en het stadsgewest Haarlem (Zuid-Kennemerland en IJmond) ruim 385.000 inwoners.[1] Haarlem wordt voor het eerst genoemd in een document uit de 10e eeuw. In 1245 kreeg het stadsrechten van Willem II van Holland. Aan het eind van de middeleeuwen was Haarlem een van de belangrijkste steden van Holland geworden. In de Vroegmoderne Tijd ontwikkelde de stad zich op industrieel gebied als textielstad en op cultureel gebied als schildersstad. ')
doc = nlp(text)

ner_details = []
for ent in doc.ents:
  row=(ent.text, ent.label_,spacy.explain(ent.label_))
  print(row)
  if not (row in ner_details):
    ner_details.append(row)

for row in ner_details:
  ner=row[0].strip().lower()
  nerType=row[1]
  #print("start refinement with",ner,"with type",nerType)

  URI=Refine(ner,nerType)
  if(URI):
    print("Found matching URI:",URI,"for \"",ner,"\"")
  else:
    print("No matching URI found for \"",ner,"\"")


    