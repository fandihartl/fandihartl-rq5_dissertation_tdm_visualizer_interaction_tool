import pandas as pd
from py2neo import Graph
from neomodel import db, config, StructuredNode, RelationshipTo, RelationshipFrom
import os
import os.path

import sys




# set the path to the required module
sys.path.append('../TDebituM-master/TDebituM-master')

# import configuration parameters
from configuration import *



# select the DATABASE in configuration.py
try:
    print(f"\n-> The backend {DATABASE} will be overwritten")
    confirmation = str(input("\tDo you want to continue? (y/n) ")) 
    if confirmation == "y" or confirmation == "yes":
        # graph = Graph(scheme=NEO4J_SCHEME, host=NEO4J_HOST, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))    #py2neo ended, migration to neomodel 2025
        config.DATABASE_URL = "neo4j+s://neo4j:XqcmVXM8QAKKbS1jGKMpayVqMWIVn2tQHEDtexyqlE8@689dca76.databases.neo4j.io"  #new format from neomodel 2025
    else:
        print("The connection to the database was not established!\n" + 
                "Aborting!")
        sys.exit(1)
    
except Exception:
    print(sys.exc_info()[1])
    print("No neo4j database connection could be established! " + 
            "Check py2neo parameters in configuration.py\n" +
            "Aborting!")
    sys.exit(1)

# TODO: make a backup copy before deleting it
#clear database before creating it

#path = os.getcwd()

#df = pd.read_excel(f"{path}\Backend\TD_datasource_71.xlsx", sheet_name="Tabelle1") #Database stored in same directory #comment due to data source problems
#df = pd.read_excel("C:\\Users\\xfand\\OneDrive\\Desktop\\TD_datasource_71.xlsx", sheet_name="Tabelle1") #local path
df = pd.read_excel("C:\\Users\\xfand\\OneDrive\\Desktop\\TD_datasource_80_n.xlsx", sheet_name="M4x4")

for i in range(len(df)):
    row = df.iloc[i]

    Personnumber=str(row["#Interview"])
    IncidentNumber=str(row["#TDincident"])
    TDItem=str(row["#TDitem"])
    itemNumber=row["#TDitem"]
    causeid=str(row["#TDCause"])
   
    TDID=Personnumber+'-'+IncidentNumber+'-'+TDItem
    position=str(row["Position"])
    leading=row["Leading Position"]
    
    experience=str(row["Experience"])
    heardtd=str(row["Heard of TD"])
    company=str(row["Company Code"])
    companysize=str(row["Company Size"])
    domain=str(row["Domain"])
    Incident=row["TD incident description"]
    tdtype=row["TD Type"]
    tdsubtyp=row["TD Subtype (Li+own)"].capitalize()
    Cause=row["Cause"].capitalize()
    msideal=str(row["(missing) TD measure"]).capitalize()
    mstaken=str(row["MeasureIst"])
    currentstate=str(row["Current state"]).capitalize()
    initparty=row["Initiating party"].split(',')
    affparty=row["Disciplines Involved in TD Case"].split(',')
    plc=row["PLC"]
    
#add person
    
    add_person="MERGE (company:Company {name:'"+company+"'}) ON CREATE SET company.companysize = '"+companysize+"' MERGE (domain:Domain {name:'"+domain+"'}) MERGE (company)-[:IS_IN]->(domain) MERGE (p:Person {name: '"+Personnumber+"'}) ON CREATE SET p.heardOfTD= false,p.experience='"+experience+"' MERGE (p)-[:WORKS_AT {POSITION:'"+position+"',leadingPosition:'"+leading+"'}]->(company)"
    
    query= add_person
#add person-report->incident
    add_incident='merge (incident:TDIncident {name:"'+Incident+'"}) MERGE (p)-[:REPORTED]->(incident)'
    query=query+add_incident

# add td incident->td item
    add_tditem =" merge (item:TDItem {ID:'"+TDID+"'}) merge(incident)<-[:IS_PART_OF]-(item)"
    query=query+add_tditem

# add cause
    add_cause =' merge (cause:Cause {name:"'+Cause+'"}) merge(item)-[:HAS_CAUSE {CAUSE_ID:"'+causeid+'"}]->(cause)'
    query=query+add_cause

# add measure ideal
    add_msideal ='merge (msideal :MeasureIdeal {name:"'+msideal+'"}) merge(item)-[:REQUIRES]->(msideal)'
    query=query+add_msideal
# add measure taken
    add_mstaken ='merge (mstaken :MeasureTaken {name:"'+mstaken+'"}) merge(item)<-[:SOLVED]-(mstaken)'
    query=query+add_mstaken
# add current state
    add_currentstate="merge (currentstate:CurrentState {name:'"+currentstate+"'}) merge (currentstate)<-[:RESULTED_IN]-(mstaken)  merge (currentstate)<-[:IS_NOW_IN]-(item) "
    query=query+add_currentstate
# add td subtyp
    add_subtyp =" merge (subtyp :TDSubtype {name:'"+tdsubtyp+"'}) merge(item)-[:BELONGS_TO]->(subtyp)"
    query=query+add_subtyp
# add td typ
    add_typ =" merge (typ :TDType {name:'"+tdtype+"'}) merge(subtyp)-[:SUBCLASS_OF]->(typ)"
    query=query+add_typ

    print(f"Row {i} of {len(df)} has been imported!")
    db.cypher_query(query)


# ------------affected party----------------next cause------------#
# add relation between td items (item lead to next item)
    if i==0:
        OldIncidentNumber="0"
        OlditemNumber= 0
    if itemNumber ==1:
        pass
    elif IncidentNumber==OldIncidentNumber and itemNumber == OlditemNumber+1:
        add_item_relation=" match (item:TDItem {ID:'"+TDID+"'}), (olditem:TDItem {ID:'"+OldTDID+"'}) merge (olditem)-[:LEAD_TO]->(item)"
        db.cypher_query(add_item_relation)
    elif IncidentNumber==OldIncidentNumber and itemNumber == OlditemNumber:
        pass
    else:
        print("wrong order of item in line", i+1 )

    OldIncidentNumber=IncidentNumber
    OlditemNumber= itemNumber
    OldTDID=TDID

# add tditem-affect-party 
    for party in affparty:
        party=party.strip()
        add_affparty="merge (item:TDItem {ID:'"+TDID+"'}) merge ("+party[0:7]+":Party {name:'"+party+"'})  merge (item)-[:AFFECTS]->("+party[0:7]+")"
        db.cypher_query(add_affparty)
# add tditem-initiate-party 
    for party in initparty:
        party=party.strip()
        add_initparty="match (item:TDItem {ID:'"+TDID+"'})  merge ("+party[0:7]+":Party {name:'"+party+"'})   merge (item)<-[:INITIATES]-("+party[0:7]+")"
        db.cypher_query(add_initparty)
