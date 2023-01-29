from flask import Flask,render_template,request,redirect,url_for
import psycopg2
import psycopg2.extras
app = Flask(__name__)


DB_HOST='127.0.0.1'
DB_NAME='Wash_db'
DB_USER='postgres'
DB_PASS='ilyas13!A'

conn = psycopg2.connect(
database="Wash_db", 
user="postgres", 
password="ilyas13!A", 
host="127.0.0.1", 
port="5432")


@app.route("/")
def Index():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s="SELECT *  from service"
   cur.execute(s)
   list_users=cur.fetchall()
   return render_template('index.html',list_users=list_users)

@app.route('/add_service',methods=['POST'])
def add_service():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      service_name = request.form['service_name']
      price = request.form['price']
      cur.execute("INSERT INTO service (service_name,price) VALUES (%s,%s)",(service_name,price))
      conn.commit()
      return redirect(url_for('Index'))

@app.route('/edit/<id>',methods = ['POST','GET'])
def get_service(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

   cur.execute('SELECT * FROM service WHERE service_id = %s',(id,))
   data=cur.fetchall()
   cur.close()
   print(data[0])
   return render_template('edit.html',service=data[0])

@app.route('/update/<id>',methods=['POST'])
def update_service(id):
   if request.method == 'POST':
      service_name = request.form['service_name']
      price = request.form['price']
   
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute("""
         UPDATE service
         SET service_name = %s,
             price = %s
         WHERE service_id =%s 
      """,(service_name,price,id))
      conn.commit()
      return redirect(url_for('Index'))
      
@app.route('/delete/<string:id>',methods = ['POST','GET'])
def delete_service(id):
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute('DELETE FROM service WHERE service_id={0}'.format(id))
      conn.commit()
      return redirect(url_for('Index'))

@app.route("/client")
def Client():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s="SELECT *  from client"
   cur.execute(s)
   list_client=cur.fetchall()
   return render_template('client_index.html',list_client=list_client)

@app.route('/add_client',methods=['POST'])
def add_client():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      full_name = request.form['full_name']
      number = request.form['number']
      cur.execute("INSERT INTO client (full_name,number) VALUES (%s,%s)",(full_name,number))
      conn.commit()
      return redirect(url_for('Client'))

@app.route('/edit1/<id>',methods = ['POST','GET'])
def get_client(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

   cur.execute('SELECT * FROM client WHERE client_id = %s',(id,))
   data=cur.fetchall()
   cur.close()
   print(data[0])
   return render_template('client_edit.html',client=data[0])

@app.route('/update1/<id>',methods=['POST'])
def update_client(id):
   if request.method == 'POST':
      full_name = request.form['full_name']
      number = request.form['number']
   
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute("""
         UPDATE client
         SET full_name = %s,
             number = %s
         WHERE client_id =%s 
      """,(full_name,number,id))
      conn.commit()
      return redirect(url_for('Client'))

@app.route('/delete1/<string:id>',methods = ['POST','GET'])
def delete_client(id):
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute('DELETE FROM client WHERE client_id={0}'.format(id))
      conn.commit()
      return redirect(url_for('Client'))

@app.route('/job')
def job():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s='SELECT * FROM job'
   cur.execute(s)
   list_job=cur.fetchall()
   return render_template('job_index.html',list_job=list_job)


@app.route('/schedule')
def schedule():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s='SELECT * FROM schedule'
   cur.execute(s)
   list_schedule=cur.fetchall()
   return render_template('schedule_index.html',list_schedule=list_schedule)

@app.route('/employees')
def Employees():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s='''select Employees_id,first_name,last_name,salary,job.job_name,schedule.schedule
from employees
inner join job
on employees.job_id=job.job_id
inner join schedule
on employees.schedule_id=schedule.schedule_id'''
   cur.execute(s)
   list_employees=cur.fetchall()

   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   a='select job_name from job'
   cur.execute(a)
   list_options5=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   b="SELECT schedule from schedule"
   cur.execute(b)
   list_options6=cur.fetchall()

   return render_template('employees_index.html',list_employees=list_employees,list_options5=list_options5,list_options6=list_options6)

@app.route('/add_employees',methods=['POST'])
def add_employees():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      salary = request.form['salary']
      #job_id = request.form['job_id']
      #schedule_id = request.form['schedule_id']
      
      job_name = request.form['job_id']
      cur.execute("SELECT job_id FROM job WHERE job_name = %s",[job_name,])
      job_id=cur.fetchall()
      job_id=job_id[0][0]

      schedule = request.form['schedule_id']
      cur.execute("SELECT schedule_id FROM schedule WHERE schedule = %s",[schedule,])
      schedule_id=cur.fetchall()
      schedule_id=schedule_id[0][0]

      cur.execute("INSERT INTO employees (first_name,last_name,salary,job_id,schedule_id) VALUES (%s,%s,%s,%s,%s)",(first_name,last_name,salary,job_id,schedule_id))
      conn.commit()
      return redirect(url_for('Employees'))

@app.route('/edit6/<id>',methods = ['POST','GET'])
def get_employees(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

   cur.execute('SELECT * FROM employees WHERE employees_id = %s',(id,))
   data=cur.fetchall()
   cur.close()
   print(data[0])
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   a='select job_name from job'
   cur.execute(a)
   list_options5=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   b="SELECT schedule from schedule"
   cur.execute(b)
   list_options6=cur.fetchall()
   return render_template('edit_employees.html',employees=data[0],list_options5=list_options5,list_options6=list_options6)     

@app.route('/update6/<id>',methods=['POST'])
def update_employees(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      salary = request.form['salary']
      
      job_name = request.form['job_id']
      cur.execute("SELECT job_id FROM job WHERE job_name = %s",[job_name,])
      job_id=cur.fetchall()
      job_id=job_id[0][0]

      schedule = request.form['schedule_id']
      cur.execute("SELECT schedule_id FROM schedule WHERE schedule = %s",[schedule,])
      schedule_id=cur.fetchall()
      schedule_id=schedule_id[0][0]
     
   
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute("""
         UPDATE employees
         SET first_name = %s,
             last_name = %s,
             salary = %s,
             job_id = %s,
             schedule_id = %s
         WHERE employees_id =%s
      """,(first_name,last_name,salary,job_id,schedule_id,id))
      conn.commit()
      return redirect(url_for('Employees'))

@app.route('/delete6/<string:id>',methods = ['POST','GET'])
def delete_employees(id):
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute('DELETE FROM employees WHERE employees_id={0}'.format(id))
      conn.commit()
      return redirect(url_for('Employees'))


@app.route('/orders')
def orders():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s='''select order_id ,date,first_name,full_name,service_name
from orders
inner join employees
on orders.employees_id=employees.employees_id
inner join client
on orders.client_id=client.client_id
inner join service
on orders.service_id=service.service_id'''
   cur.execute(s)
   list_orders=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   a='select first_name from employees'
   cur.execute(a)
   list_options=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   b="SELECT full_name from client"
   cur.execute(b)
   list_options1=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   c="SELECT service_name from service"
   cur.execute(c)
   list_options2=cur.fetchall()
   return render_template('orders_index.html',list_orders=list_orders,list_options=list_options,list_options1=list_options1,list_options2=list_options2)

@app.route('/add_orders',methods=['POST'])
def add_orders():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      date = request.form['date']

      first_name = request.form['employees_id']
      cur.execute("SELECT employees_id FROM employees WHERE first_name = %s",[first_name,])
      employees_id=cur.fetchall()
      employees_id=employees_id[0][0]

      full_name = request.form['client_id']
      cur.execute("SELECT client_id FROM client WHERE full_name = %s",[full_name,])
      client_id=cur.fetchall()
      client_id=client_id[0][0]

      service_name = request.form['service_id']
      cur.execute("SELECT service_id FROM service WHERE service_name = %s",[service_name,])
      service_id=cur.fetchall()
      service_id=service_id[0][0]

      cur.execute("INSERT INTO orders (date,employees_id,client_id,service_id) VALUES  (%s,%s,%s,%s)",(date,employees_id,client_id,service_id))
      conn.commit()
      return redirect(url_for('orders'))

@app.route('/edit5/<id>',methods = ['POST','GET'])
def get_orders(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

   cur.execute('SELECT * FROM orders WHERE order_id = %s',(id,))
   data=cur.fetchall()
   cur.close()
   print(data[0])
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   a='SELECT first_name from employees'
   cur.execute(a)
   list_options=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   b='SELECT full_name from client'
   cur.execute(b)
   list_options1=cur.fetchall()
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   c='SELECT service_name from service'
   cur.execute(c)
   list_options2=cur.fetchall()
   return render_template('edit_orders.html',orders=data[0],list_options=list_options,list_options1=list_options1,list_options2=list_options2)

@app.route('/update5/<id>',methods=['POST'])
def update_orders(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      date = request.form['date']

      first_name = request.form['employees_id']
      cur.execute("SELECT employees_id FROM employees WHERE first_name = %s",[first_name,])
      employees_id=cur.fetchall()
      employees_id=employees_id[0][0]

      full_name = request.form['client_id']
      cur.execute("SELECT client_id FROM client WHERE full_name = %s",[full_name,])
      client_id=cur.fetchall()
      client_id=client_id[0][0]

      service_name = request.form['service_id']
      cur.execute("SELECT service_id FROM service WHERE service_name = %s",[service_name,])
      service_id=cur.fetchall()
      service_id=service_id[0][0]
   
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute("""
         UPDATE orders
         SET date = %s,
             employees_id = %s,
             client_id = %s,
             service_id = %s
         WHERE order_id =%s
      """,(date,employees_id,client_id,service_id,id))
      conn.commit()
      return redirect(url_for('orders'))

@app.route('/delete5/<string:id>',methods = ['POST','GET'])
def delete_orders(id):
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute('DELETE FROM orders WHERE order_id={0}'.format(id))
      conn.commit()
      return redirect(url_for('orders'))


@app.route("/inventory")
def Inventory():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   s="SELECT *  from inventory"
   cur.execute(s)
   list_inventory=cur.fetchall()
   return render_template('inventory_index.html',list_inventory=list_inventory)

@app.route('/add_inventory',methods=['POST'])
def add_inventory():
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
      date = request.form['date']
      status = request.form['status']
      cur.execute("INSERT INTO inventory (date,status) VALUES (%s,%s)",(date,status))
      conn.commit()
      return redirect(url_for('Inventory'))

@app.route('/edit3/<id>',methods = ['POST','GET'])
def get_inventory(id):
   cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

   cur.execute('SELECT * FROM inventory WHERE inventory_id = %s',(id))
   data=cur.fetchall()
   cur.close()
   print(data[0])
   return render_template('inventory_edit.html',inventory=data[0])

@app.route('/update3/<id>',methods=['POST'])
def update_inventory(id):
   if request.method == 'POST':
      date = request.form['date']
      status = request.form['status']
   
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute("""
         UPDATE inventory
         SET date = %s,
             status = %s
         WHERE inventory_id =%s 
      """,(date,status,id))
      conn.commit()
      return redirect(url_for('Inventory'))

@app.route('/delete3/<string:id>',methods = ['POST','GET'])
def delete_inventory(id):
      cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute('DELETE FROM inventory WHERE inventory_id={0}'.format(id))
      conn.commit()
      return redirect(url_for('Inventory'))




if __name__=="main":
   app.run(debug=True)
   
    

