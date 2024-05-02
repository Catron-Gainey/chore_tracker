from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.chore import Chore
from flask_app.models.user import User # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create 
@app.route('/create/chore', methods=['POST'])
def create_chore():
    if not Chore.validate_chore(request.form):
        # redirect to the appropriate route 
        return redirect('/add/chore')
    Chore.save_chore({
        **request.form,
        'user_id': session['user_id']
    })
    return redirect('/dashboard')

@app.route('/add/chore')
def add_recipe():
    user_id = session['user_id']
    return render_template('add_chore.html', user_id=user_id)

#Read
@app.route('/view/one/chore/<int:id>')
def view_one_chore_with_user(id):
    user_id = session['user_id']
    chore = Chore.get_one_chore_with_user(id)
    return render_template('view_one_chore.html', chore=chore)

#Update
@app.route('/edit/<int:id>')
def edit(id):
    chore = Chore.get_one_chore_with_user(id)
    return render_template('edit_chore.html', chore=chore)

@app.route('/update/<int:id>',methods=['POST'])
def update_chore(id):
    if not Chore.validate_chore(request.form):
        # redirect to the appropriate route.
        return redirect(f'/edit/{id}')
    chore_dict = {
        "name": request.form["name"],
        "description": request.form["description"],
        "location":request.form["location"],
        "id":id
        }
    Chore.update_chore(chore_dict)
    return redirect("/dashboard")

@app.route('/delete/<int:id>')
def remove_recipe(id):
    Chore.delete_chore(id)
    return redirect("/dashboard")