# app.py - Flask application for birthday wishes
from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
import os
import json

app = Flask(__name__)
app.secret_key = "birthday_secret_key"  # Required for flashing messages

# Configuration
FRIEND_NAME = "Sanskrutiii"  # Change this to your friend's name
BIRTHDAY_DATE = "September 9"  # Change this to your friend's birthday
WISHES_FILE = "wishes.json"  # File to store wishes

# Ensure the photos directory exists
os.makedirs('static/photos', exist_ok=True)

# Load existing wishes or create empty list
def load_wishes():
    if os.path.exists(WISHES_FILE):
        with open(WISHES_FILE, 'r') as f:
            return json.load(f)
    return []

# Save wishes to file
def save_wish(wish, name="Anonymous"):
    wishes = load_wishes()
    wishes.append({
        'wish': wish,
        'name': name,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(WISHES_FILE, 'w') as f:
        json.dump(wishes, f)

@app.route('/')
def home():
    today = datetime.datetime.now().strftime("%B %d")
    is_birthday = today == BIRTHDAY_DATE
    wishes = load_wishes()
    return render_template('index.html', 
                          friend_name=FRIEND_NAME, 
                          birthday_date=BIRTHDAY_DATE,
                          is_birthday=is_birthday,
                          wishes=wishes)

@app.route('/wishes', methods=['POST'])
def add_wish():
    new_wish = request.form.get('wish')
    name = request.form.get('name', 'Anonymous')
    
    if new_wish and new_wish.strip():
        save_wish(new_wish, name)
        flash('Your birthday wish has been added!')
    else:
        flash('Please enter a wish message')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)