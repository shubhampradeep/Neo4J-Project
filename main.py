from flask import Flask, jsonify,render_template,request
from neo4j import GraphDatabase, basic_auth


app = Flask(__name__)

driver = GraphDatabase.driver("bolt://3.236.36.139:7687", auth=basic_auth("neo4j", "vacuums-copies-plug"))
session = driver.session()
question_list = ["What are the names of all Air-Air missiles?"
    ,"Which missiles are manufactured by both DRDO and BEL ?"
    ,"Which Manufacture manufactures both Air-Air and Surface-Surface missile?"
    ,"Which Manufacture manufactures both Defense and Cruise missile?"
    ,"Which missile have an operating range between 100 and 200 km?"
    ,"Which missiles are manufactured in both India and Russia?"
    ,"Which missiles are manufactured in India?"
    ,"Which missile has the highest operating range?"
    ,"What are the top 10 missiles that have the highest operating range?"
     ,"Which missiles have range above 3000km?"
      ,"Which launch platforms uses missiles manufactured by DRDO?"
       ,"Submarine Missiles are used in which launch platforms?"
         ,"Astra missile is used in which launch platform?"
                 ,"Akash is manufactured by which manufacturer and what is the location of the manufacturer?"
                 ,"Which missiles are used in HAL Light Combat Helicopter?"
                 ,"Which short range air-air missiles are manufactured by DRDO ?"
                 ,"What are the top 10 short range missiles in india ?"]

cypher_list = ["match (n:M)-[r:Type]->(n1:MType {name:'Air-Air Missile'}) return n"
    ,"match (n:MANUFACTURER{name:'Bharat Electronics Limited'})-[r:MANUFACTURES ]->(n1:M),(m:MANUFACTURER {name:'Defence Research and Development Organisation'})-[r1:MANUFACTURES]->(n1) return n1"
    ,"MATCH (m:MANUFACTURER)-[r1:MANUFACTURES]->(n:M)-[r2:Type]->(n1:MType {name:'Air-Air Missile'} ),(m)-[r3:MANUFACTURES]->(n2:M)-[r4:Type]->(n3:MType {name:'Surface-Surface Missile'}) return distinct m"
    ,"MATCH (m:MANUFACTURER)-[r1:MANUFACTURES]->(n:M)-[r2:Type]->(n1:MType {name:'Defence Missile'}),(m)-[r3:MANUFACTURES]->(n2:M)-[r4:Type]->(n3:MType {name:'Cruise Missile'}) return distinct m"
    ,"match (n:M) where n.maxr<=200 and n.minr>=100 return distinct n"
    ,"MATCH(n:M)<-[:MANUFACTURES {origin:'INDIA'}]-(n1:MANUFACTURER),(n2:MANUFACTURER)-[:MANUFACTURES {origin:'RUSSIA'}]->(n) return distinct n"
    ,"MATCH (n:M)<-[:MANUFACTURES {origin:'INDIA'}]-(n1:MANUFACTURER) return distinct n"
     ,"MATCH (n:M)RETURN n ORDER BY (n.maxr-n.minr) DESC LIMIT 1"
     ,"MATCH (n:M)RETURN n ORDER BY (n.maxr-n.minr) DESC LIMIT 10"
      ,"match (n:M) where n.minr>=3000 return n"
       ,"MATCH (n:MANUFACTURER {name:'Defence Research and Development Organisation'})-[:MANUFACTURES]->(:M)-[:LAUNCH_PLATFORM]->(n1:CRAFT) return distinct n1"
               ,"MATCH (n:M)-[:Type]->(:MType {name:'Submarine Missile'}), (n)-[:LAUNCH_PLATFORM]->(n1:CRAFT) return distinct n1"
               ,"MATCH (n:M {name:'ASTRA'})-[:LAUNCH_PLATFORM]->(n1:CRAFT) return n1"
               ,"MATCH (n:MANUFACTURER)-[r:MANUFACTURES]->(n1:M {name:'Akash'}) return distinct n,r"
               ,"MATCH (n:CRAFT {Craftname:'HAL Light Combat Helicopter'})<-[:LAUNCH_PLATFORM]-(n1:M) return distinct n1"
               ,"match (n:MANUFACTURER {name:'Defence Research and Development Organisation'})-[:MANUFACTURES]->(n1:M)-[:Type]->(n2:MType {name:'Air-Air Missile'} ) where n1.maxr<=500 return n1"
               ,"match (n:M) return n order by n.minr  ASC LIMIT 10"]


cypher_list_graph = ["match (n:M)-[r:Type]->(n1:MType {name:'Air-Air Missile'}) return n,r,n1"
    ,"match (n:MANUFACTURER{name:'Bharat Electronics Limited'})-[r:MANUFACTURES ]->(n1:M),(m:MANUFACTURER {name:'Defence Research and Development Organisation'})-[r1:MANUFACTURES]->(n1) return n1,n,r,m,r1"
    ,"MATCH (m:MANUFACTURER)-[r1:MANUFACTURES]->(n:M)-[r2:Type]->(n1:MType {name:'Air-Air Missile'} ),(m)-[r3:MANUFACTURES]->(n2:M)-[r4:Type]->(n3:MType {name:'Surface-Surface Missile'}) return distinct m,r1,r2,r3,r4,n,n1,n2,n3"
    ,"MATCH (m:MANUFACTURER)-[r1:MANUFACTURES]->(n:M)-[r2:Type]->(n1:MType {name:'Defence Missile'}),(m)-[r3:MANUFACTURES]->(n2:M)-[r4:Type]->(n3:MType {name:'Cruise Missile'}) return distinct m,r1,r2,r3,r4,n,n1,n2,n3"
    ,"match (n:M) where n.maxr<=200 and n.minr>=100 return distinct n"
    ,"MATCH(n:M)<-[r1:MANUFACTURES {origin:'INDIA'}]-(n1:MANUFACTURER),(n2:MANUFACTURER)-[r2:MANUFACTURES {origin:'RUSSIA'}]->(n) return distinct n,n1,n2,r1,r2"
    ,"MATCH (n:M)<-[r1:MANUFACTURES {origin:'INDIA'}]-(n1:MANUFACTURER) return distinct n,n1,r1"
     ,"MATCH (n:M)RETURN n ORDER BY (n.maxr-n.minr) DESC LIMIT 1"
     ,"MATCH (n:M)RETURN n ORDER BY (n.maxr-n.minr) DESC LIMIT 10"
      ,"match (n:M) where n.minr>=3000 return n"
       ,"MATCH (n:MANUFACTURER {name:'Defence Research and Development Organisation'})-[r1:MANUFACTURES]->(n2:M)-[r2:LAUNCH_PLATFORM]->(n1:CRAFT) return distinct n1,n2,n,r1,r2"
               ,"MATCH (n:M)-[r1:Type]->(n2:MType {name:'Submarine Missile'}), (n)-[r2:LAUNCH_PLATFORM]->(n1:CRAFT) return distinct n1,n,n2,r1,r2"
               ,"MATCH (n:M {name:'ASTRA'})-[r1:LAUNCH_PLATFORM]->(n1:CRAFT) return n1,n,r1"
               ,"MATCH (n:MANUFACTURER)-[r:MANUFACTURES]->(n1:M {name:'Akash'}) return distinct n,r,n1"
               ,"MATCH (n:CRAFT {Craftname:'HAL Light Combat Helicopter'})<-[r1:LAUNCH_PLATFORM]-(n1:M) return distinct n1,n,r1"
                ,"match (n:MANUFACTURER {name:'Defence Research and Development Organisation'})-[r1:MANUFACTURES]->(n1:M)-[r2:Type]->(n2:MType {name:'Air-Air Missile'} ) where n1.maxr<=500 return n,n1,n2,r1,r2"
                     ,"match (n:M) return n order by n.minr  ASC LIMIT 10"]


qw = 0
question_selected = ""
# @app.route('/')
# def Index():
#     q1 = question_list[0]
#     q2 = question_list[1]
#     q3 = question_list[2]
#     q4 = question_list[3]
#     q5 = question_list[4]
#     q6 = question_list[5]
#     q7 = question_list[6]
#     q8 = question_list[7]
#     q9 = question_list[8]
#     q10 = question_list[9]
#     q11 = question_list[10]
#     q12 = question_list[11]
#     q13 = question_list[12]
#     q14 = question_list[13]
#     q15 = question_list[14]
#     return render_template("index.html",q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,q9=q9,q10=q10,q11=q11,q12=q12,q13=q13,q14=q14,q15=q15)
#

@app.route('/query', methods=['GET'])
def checker():
    global qw

    cquery={}
    cquery['query'] = cypher_list_graph[qw]
    print(cypher_list[qw])
    return jsonify(cquery)


@app.route('/')
def home():
    global question_selected
    return render_template("index1.html", qlist = question_list,qselected=question_selected)



@app.route('/', methods=['POST'])
def Demo_page():

    temp = request.form['choice']
    global question_selected
    question_selected = temp
    i = question_list.index(temp)

    global qw
    qw = i

    cypher_query = cypher_list[i]
    results = session.run(cypher_query)
    Craft_name = []
    missile_maxr = []
    missile_minr = []
    manufacter_origin = []
    names = []

    for row in (results):

            if(row[0]['name']):
                names.append(row[0]['name'])
            if(row[0]['maxr']):
                missile_maxr.append(row[0]['maxr'])
                missile_minr.append(row[0]['minr'])
            if(row[1]):
                manufacter_origin.append(row[1]['origin'])
            if(row[0]['Craftname']):
                Craft_name.append(row[0]['Craftname'])

    if'table' in request.form:
         return render_template("demo_page.html", qlist = question_list, qselected=question_selected, Craft_name=Craft_name,manufacter_origin = manufacter_origin,names=names,missile_maxr=missile_maxr,missile_minr=missile_minr)
    elif 'Graph' in request.form:
         return render_template("graph.html", qlist = question_list,qselected=question_selected)


if __name__=="__main__":
    app.run(debug=True)