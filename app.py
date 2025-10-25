from flask import Flask, render_template, url_for, request, redirect, flash
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

@app.route('/', methods=['GET','POST'])
def home_page():

    if request.method == 'POST':
        task_content = request.form['content']
        if not task_content:
            flash("Task cannot be empty")
            return redirect('/')
        try:
            supabase.table('todo').insert({'task': task_content}).execute()
            return redirect('/')
        except Exception as e:
            print(e)
            return "There was an error"
    else:
        response = supabase.table('todo').select('*').execute()
        tasks = response.data
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<id>')
def delete_task(id):
    try:
        data = supabase.table("todo").delete().eq("id", id).execute()
        return redirect('/')
    except:
        return "There was an issue deleting this task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        new_task = request.form['content']  # get new task text from form input
        try:
            supabase.table("todo").update({"task": new_task}).eq("id", id).execute()
            return redirect('/')
        except Exception as e:
            print(e)
            return "There was an issue updating this task"
    else:
        # Optional: load the existing task for the edit form
        response = supabase.table('todo').select('*').eq('id', id).single().execute()
        task = response.data
        return render_template('update.html', task=task)


if __name__ == ('__main__'):
    app.run(debug=True, port=8585)