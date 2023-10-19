from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wifi_profiles.db'
db = SQLAlchemy(app)

class WiFiProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    wifi_info = WiFiProfile.query.all()
    return render_template('index.html', wifi_info=wifi_info)

if __name__ == '__main__':
    db.create_all()
    
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    
    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                wifi_profile = WiFiProfile(profile_name=i, password=results[0])
                db.session.add(wifi_profile)
                db.session.commit()
            except IndexError:
                pass
        except subprocess.CalledProcessError:
            pass
    
    app.run(debug=True)