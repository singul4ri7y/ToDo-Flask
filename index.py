from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

w_app = Flask( __name__ )
w_app.config[ 'TRAP_BAD_REQUEST_ERRORS' ] = True
w_app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///test.db'
db = SQLAlchemy( w_app )

class ToDo(db.Model): 
	id = db.Column( db.Integer, primary_key = True )
	title = db.Column( db.String(100), nullable = False )
	content = db.Column( db.String( 200 ), nullable = False, default = 'No content to show!' )
	date_created = db.Column( db.DateTime, default = datetime.utcnow )
	
	def __repr__( self ):
		return '<Task %r>' % self.id

@w_app.route( '/', methods = [ 'POST', 'GET' ] )

def index(): 
	if request.method == 'POST': 
		title = request.form[ 'title' ]
		content = request.form[ 'content' ]
		
		new_task = ToDo( title = title, content = content )
		
		try: 
			db.session.add( new_task )
			db.session.commit()
			
			return redirect( '/' )
		except: 
			return 'There was an issue adding the task!'
	
	tasks = ToDo.query.order_by( ToDo.date_created ).all()
	
	return render_template( 'index.html', tasks = tasks )

@w_app.route( '/delete/<int:id>' )

def delete(id): 
	task_to_delete = ToDo.query.get_or_404( id )
	
	try: 
		db.session.delete( task_to_delete )
		db.session.commit()
	except: 
		return 'Failed to delete task!'
	
	return redirect( '/' )

@w_app.route( '/update/<int:id>', methods = [ 'POST', 'GET' ] )

def update(id):
	task = ToDo.query.get_or_404( id )
	
	if request.method == 'POST': 
		task.title = request.form[ 'title' ]
		task.content = request.form[ 'content' ]
	
		try: 
			db.session.commit()
		except: 
			return 'Failed to commit changes!'
		
		return redirect( '/' )
	
	return render_template( 'update.html', task = task )

@w_app.route( '/content/<int:id>' )

def content(id): 
	task = ToDo.query.get_or_404( id )
	return render_template( 'content.html', task = task )

if __name__ == '__main__': 
	w_app.run( debug = True )