from flask_cors import CORS,cross_origin
# cors package is needed because by default cors policy is restricted so that same site can access same backend
from flask import Flask,render_template,request,make_response,redirect

marks_app = Flask(__name__, instance_relative_config=True)
marks_app.config.from_mapping(
        SECRET_KEY='dev',
        
    )


#<----------------------------------------------------

CORS(marks_app,resources={r"/*": {"origins": "*"}},supports_credentials=True);



# for ca-------------------------------------------------------
import json
import mysql.connector

def openconnection_for_ca(**args):
    
    tablename=args.get('tablename',None);
    databasename=args.get('databasename',None);
    # adding default database as users
    try:
        if(databasename ):
            cn=mysql.connector.connect(user='shivamguys',host='yesteachermember.co0djdk6bphh.us-east-2.rds.amazonaws.com',password='HadooP_123',database=databasename,charset='utf8');
        return cn;
    except:
        print("connection error 101");
        return 101


import requests
@marks_app.route('/opensourceca/itsabhisehk/getmarks/<string:sid>',methods=['GET'])
def getdata(sid):
    conn=openconnection_for_ca(databasename='abhishekca')
    marks_data=[]
    if conn!=101:
        cursor=conn.cursor()
        try:
            cursor.execute("select * from marks where sid={}".format(sid))
            all_data=cursor.fetchall()
            
            if all_data:
                for i in all_data:
                    sid,os,ost,dbms,dbmst,automata,automatat,percentage,=i;
                    labeltag='Mark Comparison Graphs'
                    labels=['Operating System','Database Management','Automata']
                    datasets=[os,dbms,automata]

                    link="https://quickchart.io/chart?c={type:'bar',data:{labels:"+str(labels)+",datasets:[{label:'"+str(labeltag)+"', data:"+str(datasets)+", fill:false,borderColor:'blue'}]}}"
                    res=requests.get(link)
                    pie_labels=labels
                    pie_datasets=[(os/ost)*100,(dbms/dbmst)*100,(automata/automatat)*100]
                    pie_link="""https://quickchart.io/chart?bkg=white&c={ "type": "outlabeledPie", "data": { "labels":"""+str(pie_labels)+""" , "datasets": [{ "data":"""+str(pie_datasets)+"""  }] }, "options": { "plugins": { "legend": false, "outlabels": { "text": "%l -> %p", "color": "white", "stretch": 35, "font": { "resizable": true, "minSize": 12, "maxSize": 18 } } } } }"""
                    pie_res=requests.get(pie_link)
                    # print(pie_res.status_code,pie_link)
                    
                    if res.status_code==200 and pie_res.status_code==200:
                            import base64
                  

                            diurl=base64.b64encode(res.content)
                            diurl=diurl.decode('ascii')
                            diurl="data:image/png;base64,"+str(diurl)


                            pdiurl=base64.b64encode(pie_res.content)
                            pdiurl=pdiurl.decode('ascii')
                            pdiurl="data:image/png;base64,"+str(pdiurl)

                            

                            marks_data.append({'bar':diurl,'pie':pdiurl,'os_marks':os,'os_out_of':ost,'dbms_marks':dbms,'dbms_out_of':dbmst,'automata_marks':automata,'automata_out_of':automatat})
                    else:

                        marks_data.append({'os_marks':os,'os_out_of':ost,'dbms_marks':dbms,'dbms_out_of':dbmst,'automata_marks':automata,'automata_out_of':automatat})
                    

            else:
                marks_data={}
                marks_data['no_data']=True

        finally:
            conn.close()
 
        return json.dumps(marks_data)




@marks_app.route('/opensourceca/itsabhisehk/submitmarks/<int:sid>',methods=['POST'])
def submitdata(sid):
    # print(request.data)
    data=json.loads(request.data.decode('utf-8'))
    # print(data)
    conn=openconnection_for_ca(databasename='abhishekca')
    return_data={}
 
    if conn!=101:
        cursor=conn.cursor()
        try:
            os,ost,dbms,dbmst,automata,automatat=float(data['os']['os_marks']),int(data['os']['os_out_of']),float(data['dbms']['dbms_marks']),int(data['dbms']['dbms_out_of']),float(data['automata']['automata_marks']),int(data['automata']['automata_out_of'])
            percentage=((os/ost)*100)+((dbms/dbmst)*100)+((automata/automatat)*100)
         
            percentage=(percentage/3)
         
            cursor.execute("insert into marks values({},{},{},{},{},{},{},{})".format(int(sid),os,ost,dbms,dbmst,automata,automatat,float(percentage)))
            conn.commit()
            return_data['success']=True
        except:
            return_data['failure']=True


        finally:
            conn.close()
    return json.dumps(return_data)


if '__main__'==__name__:
    # create and configure the app

    """
    the main object is application as it is registered with flask
    application = Flask(__name__, instance_relative_config=True)

    """
    

    

    marks_app.run(host='0.0.0.0',port=5002)

