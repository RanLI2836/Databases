#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://rl2836:2836@104.196.18.7/w4111"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None
  else:
    print "successfully connected to the db"

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


"""

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  ""
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  ""

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")
"""

#homepage

@app.route('/')
def home():
  cursor = g.conn.execute("SELECT * FROM itinerary")
  itinerarys = []
  for itinerary in cursor:
    print itinerary
    itinerarys.append((itinerary['iid'], itinerary['iname'],itinerary['departdate'],itinerary['returndate'],itinerary['departure'],itinerary['destination'],itinerary['standardprice']))
  cursor.close()
  # print "yay"
  return render_template("home.html", itinerarys=itinerarys)



@app.route('/searchitinerary', methods=['POST'])
def searchitinerary():
  print "search for itinerary!"
  record = request.form
  print record
  query = """select I7.iid,I7.iname,I7.guidename,I7.hotelname,I7.vehicletype,array_to_string(array_agg(TC.groupNO),', ') as groupNO from (SELECT I6.iid,I6.iname,I6.vehicletype,I6.hotelname,array_to_string(array_agg(G2.name),', ') as guidename FROM (SELECT I5.iid,I5.iname,I5.vehicletype,I5.hotelname,G.gid FROM( select I4.iid,I4.iname,I4.vehicletype,array_to_string(array_agg(H.hname), ', ') as hotelname from (SELECT I3.iid,I3.iname,St.hid,I3.vehicletype FROM (select I2.iid, I2.iname,array_to_string(array_agg(V.vtype), ', ') as vehicletype from (SELECT distinct I1.iid, I1.iname, T.vid FROM (select I.iid, I.iname from (select sid from scenicspot where sname ilike '%""" + str(record['destination']) + """%') S,  itinerary I, visit V1 where V1.sid = S.sid AND V1.iid = I.iid) I1 left outer join transport T on T.iid = I1.iid) I2, Vehicle V where V.vid = I2.vid group BY I2.iid,I2.iname) I3 LEFT OUTER JOIN stay St ON St.iid = I3.iid) I4 left outer join hotel H on H.hid = I4.hid GROUP BY I4.iid,I4.iname,I4.vehicletype) I5 LEFT OUTER JOIN guide G ON G.iid = I5.iid) I6, tourguide G2 WHERE G2.gid = I6.gid group BY I6.iid,I6.iname,I6.vehicletype,I6.hotelname) I7 LEFT OUTER JOIN tourgroup_cont TC ON TC.iid = I7.iid GROUP BY I7.iid,I7.iname,I7.guidename,I7.hotelname,I7.vehicletype"""
  # print query
  try:
    cursor = g.conn.execute(text(query))   
    print "have got the info!"
    search_itinerary = []
    for i in cursor:
      print i
      search_itinerary.append((i['iid'],i['iname'],i['guidename'],i['hotelname'],i['vehicletype'],i['groupno']))
    cursor.close()
  except:
    return render_template("error.html",error="Failed")
  return render_template("itinerary.html", its=search_itinerary)


# search group infomation (in itinerary page)
@app.route('/searchgroup', methods=['POST'])
def searchpeople():
  print "who are in this group??"
  record = request.form
  print record
  try:
    cursor=g.conn.execute("""select T.tname, T.tgender, T.tphone from composedof C, tourist T where T.tid = C.tid AND C.groupNO = %s """, record['No'])
    print "got the info!"
    people = []
    for x in cursor:
      print x
      people.append((x['tname'],x['tgender'],x['tphone']))
    cursor.close()
  except:
    return render_template("error.html",error="Failed")
  return render_template("tourgroup.html", people=people)


@app.route('/tourist')
def tourist():
  print "someone requested the tourist page"
  try:
    cursor = g.conn.execute("SELECT * FROM tourist") #db 
    tourists = []
    for tourist in cursor:
      print tourist
      #may need to append all the columns
      tourists.append((tourist['tid'],tourist['tname'],tourist['tgender']))  # can also be accessed using result[0]
  except:
    return render_template("error.html",error="Operation failed!")
  cursor.close()
                                      #html  #python 
  return render_template("tourist.html",tourists=tourists)


@app.route('/addtourist', methods=['POST'])
def addtourist():
  print request.form
  # --> ImmutableMultiDict([('hid', u'11212'), ('tel', u'1234'), ('hname', u'name'), ('hname', u'addd'), ('star', u'5')])
  record = request.form
  print record
  print record['tid'] 
  print record['tname']
  print record['tgender']
  print record['dob']
  print (record['tphone'])  
  try:
  # # (hid,hname,hadd,htel,star)
  # record = {str(ele) for ele in raw_record.values()}
  # print record
    g.conn.execute('INSERT INTO tourist VALUES (%s,%s,%s,%s,%s,%s)', record['tid'], record['tname'], record['tgender'].upper(), record['dob'],(record['tphone']), record['tadd'])
  except:
    return render_template("error.html",error="failed")

  return redirect('/tourist')


@app.route('/edittourist', methods=['POST'])
def edittourist():
  # print request.form
  # --> ImmutableMultiDict([('hid', u'11212'), ('tel', u'1234'), ('hname', u'name'), ('hname', u'addd'), ('star', u'5')])
  record = request.form
  print record
  print record['tid'] 
 
  # UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  # WHERE city = 'San Francisco' AND date = '2003-07-03';
  try:
    sql = "select * from tourist where tid = '" + record['tid'] + "'"
    t=()
    cursor = g.conn.execute(text(sql))
    for tourist in cursor:
      print tourist
      t = tourist
      #(u'20171111', u'special t', u'M', datetime.date(1999, 11, 22), u'8123617185', u'addd')
  except:
    return render_template("error.html",error="failed")

  return render_template("edittourist.html",t=t)


@app.route('/editaction', methods=['POST'])
def editaction():
  record = request.form
  print record
  print record['tid'] 
  
  try:
    sql = "UPDATE tourist SET tname='" + record['tname'] + "',tgender='" + record['tgender'] + "', dob='" + record['dob'] + "', tphone='"+ record['tphone'] + "' ,tadd='"+ record['tadd'] + "' WHERE tid ='" + record['tid'] + "'"
    print sql
    g.conn.execute(text(sql))
    
  except:
    return render_template("error.html",error="edit tourist failed")

  return redirect('/tourist')



@app.route('/deltourist', methods=['POST'])
def deltourist():
  # print request.form
  record = request.form
  print record
  try:
    sql = "delete from tourist where tid ='" + record['tid'] + "'"
    g.conn.execute(text(sql))
  except:
    return render_template("error.html",error="deletion failed")

  return redirect('/tourist')


@app.route('/hotel')
def hotel():
  print "someone requested the hotel page"
  try:
    cursor = g.conn.execute("SELECT * FROM hotel") #db 
    hotels = []
    for hotel in cursor:
      print hotel
      #may need to append all the columns
      hotels.append((hotel['hname'],hotel['htel'],hotel['hadd'],hotel['star']))  # can also be accessed using result[0]
  except:
    return render_template("error.html",error="Operation failed!")
  cursor.close()
                                      #html  #python 
  return render_template("hotel.html",hotels=hotels)


@app.route('/addhotel', methods=['POST'])
def addhotel():
  # print request.form
  # --> ImmutableMultiDict([('hid', u'11212'), ('tel', u'1234'), ('hname', u'name'), ('hname', u'addd'), ('star', u'5')])
  record = request.form
  print record
  print record['hid'] 
  print record['hname']
  print record['hadd']
  print record['tel']
  print (record['star'])  
  try:
  # # (hid,hname,hadd,htel,star)
  # record = {str(ele) for ele in raw_record.values()}
  # print record
    g.conn.execute('INSERT INTO hotel VALUES (%s,%s,%s,%s,%s)', record['hid'], record['hname'], record['hadd'], record['tel'],(record['star']))
  except:
    return render_template("error.html",error="failed")

  return redirect('/hotel')
   

@app.route('/scenicspot')
def scenicspot():
  print "someone requested the scenicspot page"
  try:
    cursor = g.conn.execute("SELECT * FROM scenicspot") #db 
    scenicspots = []
    for scenicspot in cursor:
      print scenicspot
      #may need to append all the columns
      scenicspots.append((scenicspot['sname'],scenicspot['stype']))  # can also be accessed using result[0]
  except:
    return render_template("error.html",error="Operation failed!")
  cursor.close()
                                      #html  #python 
  return render_template("scenicspot.html",scenicspots=scenicspots)


@app.route('/addscenicspot', methods=['POST'])
def addscenicspot():
  # print request.form
  # --> ImmutableMultiDict([('hid', u'11212'), ('tel', u'1234'), ('hname', u'name'), ('hname', u'addd'), ('star', u'5')])
  record = request.form
  print record
  print record['sid'] 
  print record['sname']
  print record['stype']
  try:
  # # (hid,hname,hadd,htel,star)
  # record = {str(ele) for ele in raw_record.values()}
  # print record
    g.conn.execute('INSERT INTO scenicspot VALUES (%s,%s,%s)', record['sid'], record['sname'], record['stype'])
  except:
    return render_template("error.html",error="failed")

  return redirect('/scenicspot')


@app.route('/insurance')
def insurance():
  print "someone requested the insurance page"
  try:
    cursor1 = g.conn.execute("SELECT * FROM insurance") #db 
    insurances = []
    for insurance in cursor1:
      insurances.append((insurance['policyidno'],insurance['type']))
    cursor1.close()

    cursor2 = g.conn.execute("SELECT distinct E3.tid, E3.tname FROM(SELECT E2.tid, T.tname, E1.policyIDNO, I.type FROM tourist T, insurance I, enroll E1,(SELECT E.tid, count(*) AS enrollment FROM enroll E GROUP BY E.tid) E2 WHERE E2.enrollment>1 AND E1.tid=E2.tid AND I.policyIDNO=E1.policyIDNO AND T.tid=E2.tid ORDER BY E2.tid) E3")
    customers = []
    for customer in cursor2:
      customers.append((customer['tid'],customer['tname']))
  except:
    return render_template("error.html",error="Operation failed!")
                                          #html  #python 
  return render_template("insurance.html",insurances=insurances, customers=customers)


@app.route('/tourguide')
def tourguide():
  print "someone requested the tourguide page"

  try:
    # star guide!
    cursor1 = g.conn.execute("SELECT T.GID, T.name, T.GENDER, T.PHONE,T.ADDRESS, S.total_num FROM (SELECT G1.GID, SUM(I1.tour_num) AS total_num FROM guide G1,(SELECT C1.iid, C1.groupNO, C2.tourist_num AS tour_num FROM tourgroup_cont C1, (SELECT C.groupNO, count(*) AS tourist_num FROM composedof C GROUP BY C.groupNO) C2 WHERE C1.groupNO=C2.groupNO AND C2.tourist_num>2)I1 WHERE G1.iid=I1.iid GROUP BY G1.GID) S, tourguide T WHERE S.GID=T.GID AND S.total_num>6 ORDER BY S.total_num")#
    starguides = []
    for starguide in cursor1:
      print starguide
      starguides.append((starguide['name'],starguide['gid'], starguide['total_num']))
    # 
    cursor2 = g.conn.execute("SELECT * FROM tourguide") #db 
    tourguides = []
    for tourguide in cursor2:
      print tourguide
      #may need to append all the columns
      tourguides.append((tourguide['name'],tourguide['gender'],tourguide['phone'],tourguide['address'],tourguide['language']))  # can also be accessed using result[0]
  except:
    return render_template("error.html",error="Operation failed!")
  cursor1.close()
  cursor2.close()
                                      #html  #python 
  return render_template("tourguide.html",tourguides=tourguides, starguides=starguides)



@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
