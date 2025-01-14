from flask import Flask, render_template, request, redirect, url_for,jsonify
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from flask import session
from hashtable import HashTable
from feedback_stack import FeedbackList


json_files = {
    'electrical': 'electrical.json',
    'civil_mason': 'civil_mason.json',
    'plumbing': 'plumbing.json',
    'wifi_problem': 'wifi_problem.json',
    'carpentery': 'carpentery.json'
}

hash_tables = {
    'electrical': HashTable(size=100),
    'plumbing': HashTable(size=100),
    'wifi_problem': HashTable(size=100),
    'carpentery': HashTable(size=100),
    'civil_mason': HashTable(size=100)
}



# Retrieve the email and password from environment variables
SENDER_EMAIL ="ssn.help.deskk@gmail.com" #os.getenv("EMAIL_USER")
SENDER_PASSWORD ="uquw xmct qycs aigo" #os.getenv("EMAIL_PASS")

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

current_directory = os.path.dirname(os.path.abspath(__file__))

# Ensure the JSON files exist
signup_json_file_name = 'signup_data.json'
complaint_json_file_name = 'clog.json'
electrical_json_file_name = 'electrical.json'
plumbing_json_file_name='plumbing.json'
wifi_problem_json_file_name='wifi_problem.json'
carpentery_json_file_name='carpentery.json'
civil_json_file_name='civil_mason.json'



agents_json_file_path = os.path.join(current_directory, 'agents.json')
signup_json_file_path = os.path.join(current_directory, signup_json_file_name)
complaint_json_file_path = os.path.join(current_directory, complaint_json_file_name)
electrical_json_file_path = os.path.join(current_directory, electrical_json_file_name)
plumbing_json_file_path = os.path.join(current_directory, plumbing_json_file_name)
wifi_problem_json_file_path = os.path.join(current_directory, wifi_problem_json_file_name)
carpentery_json_file_path = os.path.join(current_directory, carpentery_json_file_name)
civil_json_file_path = os.path.join(current_directory, civil_json_file_name)
admin_json_file_path = os.path.join(current_directory, 'adminlogin.json')
feedback_json_file_path = os.path.join(current_directory, 'feedback.json')
feedback_list = FeedbackList(feedback_json_file_path)
def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)  # Write an empty list as the initial content
        print(f"Created new file: {file_path}")

def ensure_resolved_file_exists():
    for topic in json_files.keys():
        resolved_file_path = os.path.join(current_directory, f'resolved_{topic}.json')
        ensure_file_exists(resolved_file_path)

ensure_resolved_file_exists()

ensure_file_exists(signup_json_file_path)
ensure_file_exists(complaint_json_file_path)
ensure_file_exists(agents_json_file_path)
ensure_file_exists(admin_json_file_path)
ensure_file_exists(feedback_json_file_path)



def read_json_file(file_path):
    if os.stat(file_path).st_size == 0:
        return []
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



def send_signin_email(user_email,ticket,name):
    subject = f"Your Ticket Confirmation - Ticket {ticket}"
    body = f'''
    
Dear {name},

Thank you for reaching out to us.

We have successfully created a ticket for your request. Your ticket number is {ticket}. 

Our team is currently reviewing your request, and we will keep you updated on the progress. If you have any additional information or questions, please do not hesitate to reply to this email or contact our support team.

Thank you for your patience and cooperation.

Best regards,

SSN help-desk  '''

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, user_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")




@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/signin')
def signin():
    return render_template('trial.html')

@app.route('/signup')
def signup():
    return render_template('trialsignup.html')

def get_client_name(user_email):
    with open(signup_json_file_path, 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == user_email:
                return user['fullname']
    return None



@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    data = request.get_json()
    name = data['fullname']
    email = data['email']
    password = data['password']
    role = 'client'
    session['email']=email

    with open(signup_json_file_path, 'r') as file:
        users = json.load(file)
    
    # Append the new user
    users.append({'fullname': name, 'email': email, 'password': password, 'role': role})
    
    # Save the updated data
    write_json_file(signup_json_file_path, users)
    
    return jsonify(success=True), 200


@app.route('/submit_signin_user', methods=['POST'])
def submit_signin_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    # Check the JSON file for matching credentials
    users = read_json_file(signup_json_file_path)
    for user in users:
            if user['email'] == email and user['password'] == password :
                
                session['email']=email
                return jsonify(success=True, message="User sign-in successful!"), 200
    return jsonify(success=False, message="Incorrect email or password"), 401
    
@app.route('/submit_signin_agent', methods=['POST'])
def submit_signin_agent():
    data = request.get_json()
    email = data['email']
    password = data['password']
# Check agent credentials
    agents = read_json_file(agents_json_file_path)
    for agent in agents:
        if agent['email'] == email and agent['password'] == password :
            session['agent'] = agent['help_topic']  # Store help_topic in session for redirection
            return jsonify(success=True, message="Agent sign-in successful!", agent=True), 200
    return jsonify(success=False, message="Incorrect email or password"), 401
@app.route('/submit_signin_admin', methods=['POST'])      
def submit_signin_admin():
    data = request.get_json()
    email = data['email']
    password = data['password'] 
    admin = read_json_file(admin_json_file_path)
    for admin in admin:
        if admin['email'] == email and admin['password'] == password :
            return jsonify(success=True, message="Admin sign-in successful!", agent=True), 200   
    return jsonify(success=False, message="Incorrect email or password"), 401

@app.route('/admin_login')
def admin_login():
    return render_template('trialadminlogin.html')

@app.route('/ticketsystem')
def ticket_system():
    return render_template('ticketsystem.html')

@app.route('/complaintlog')
def clog():
    user_email = session.get('email')
    sign_up_data=read_json_file(signup_json_file_path)
    for data in sign_up_data:
        if data['email']==user_email:
            name=data['fullname']
            break
    return render_template('complaintlog.html',name=name)

@app.route('/submit_clog', methods=['POST'])
def submit_clog():
    data = request.get_json()
    name=None
    help_topic = data.get('help_topic')
    description = data.get('description')
    location = data.get('location')
    room_no = data.get('room_no')
    mob_no = data.get('mob_no')
    preferred_time = data.get('preferred_time')
    user_email = session.get('email')
    ticket=randint(100000,1000000)
    sign_up_data=read_json_file(signup_json_file_path)
    for data in sign_up_data:
        if data['email']==user_email:
            name=data['fullname']
            break
    if name:
        send_signin_email(user_email, ticket, name)
    else:
        return jsonify(success=False, message="User not found in signup data"), 404

    
    # Define the path for the help topic-specific JSON file
    complaint_json_file_path = os.path.join(current_directory, f'{help_topic}.json')

    # Ensure the JSON file exists
    ensure_file_exists(complaint_json_file_path)
    
    # Load existing complaints
    complaints = read_json_file(complaint_json_file_path)
    
    new_complaint={
        'help_topic': help_topic,
        'description': description,
        'location': location,
        'room_no': room_no,
        'mob_no': mob_no,
        'preferred_time': preferred_time,
        'ticket id':ticket,
        'user-email':user_email,
        'status': 'open'
    }
    # Append the new complaint
    complaints.append(new_complaint)
    
    # Save the updated complaints
    write_json_file(complaint_json_file_path, complaints)

     # Insert into hash table
    hash_tables[help_topic].insert(ticket, new_complaint)

    return jsonify(success=True), 200


@app.route('/agent_login')
def agent_login():
    return render_template('trialagentsignin.html')


@app.route('/electrical_data')
def electrical_data():
    return help_topic_data('electrical')

@app.route('/plumbing_data')
def plumbing_data():     
    return help_topic_data('plumbing')

@app.route('/carpentery_data')
def carpentery_data():      
    return help_topic_data('carpentery')

@app.route('/internet_data')
def internet_data():      
         return help_topic_data('wifi_problem')

@app.route('/civil_data')
def civil_data():
         return help_topic_data('civil_mason')
    
def sort_tickets_by_time(tickets):
    return sorted(tickets, key=lambda x: x['preferred_time'])

@app.route('/<help_topic>_data')

def help_topic_data(help_topic):
    if help_topic not in hash_tables:
        return redirect(url_for('home'))
    # Retrieve data from the hash table
    data = hash_tables[help_topic].get_all()
    # Sort data by preferred time
    sorted_data = sort_tickets_by_time(data)
    return render_template(f'{help_topic}.html', data=sorted_data)



@app.route('/agent_redirect')
def agent_redirect():
    agent_topic = session.get('agent')
    if agent_topic == 'plumbing':
        return redirect(url_for('plumbing_data'))
    elif agent_topic == 'civil-mason':
        return redirect(url_for('civil_data'))
    elif agent_topic == 'carpentery':
        return redirect(url_for('carpentery_data'))
    elif agent_topic == 'electrical':
        return redirect(url_for('electrical_data'))
    elif agent_topic == 'wifi_problem':
        return redirect(url_for('internet_data'))
    else:
        return redirect(url_for('home'))
    


@app.route('/update_ticket_status', methods=['POST'])
def update_ticket_status():
    data = request.get_json()
    ticket_id = int(data['ticket_id'])
    new_status = data['status']
    help_topic = data['help_topic']

    # Update the hash table
    ticket = hash_tables[help_topic].retrieve(ticket_id)
    if ticket:
        ticket['status'] = new_status
        # Remove the ticket if resolved
        if new_status == 'resolved':
            hash_tables[help_topic].delete(ticket_id)
            append_to_resolved_json(help_topic, ticket)
            update_json_file(help_topic)#updating the existing file
        else:
            save_data_from_hash_table(help_topic)
    return jsonify(success=True), 200

def append_to_resolved_json(help_topic, ticket):
    resolved_file_path = os.path.join(current_directory, f'resolved_{help_topic}.json')
    resolved_tickets = read_json_file(resolved_file_path)
    resolved_tickets.append(ticket)
    write_json_file(resolved_file_path, resolved_tickets)

def update_json_file(help_topic):
    file_path = os.path.join(current_directory, json_files[help_topic])
    data = hash_tables[help_topic].get_all()
    write_json_file(file_path, data)


def save_data_from_hash_table(help_topic):
    file_path = os.path.join(current_directory, json_files[help_topic])
    data = hash_tables[help_topic].get_all()
    write_json_file(file_path, data)

#this function ensures whether the ticket-id is present 
def load_data_to_hash_tables():
    for topic, file_name in json_files.items():
        file_path = os.path.join(current_directory, file_name)
        data = read_json_file(file_path)
        for entry in data:
             # Ensure 'ticket id' key exists and is an integer
            if 'ticket id' not in entry:
                print(f"Missing 'ticket id' in entry: {entry}")
                entry['ticket id'] = randint(100000, 1000000)
            entry['ticket id'] = int(entry['ticket id'])  # Ensure ticket id is an integer
            hash_tables[topic].insert(entry['ticket id'], entry)

load_data_to_hash_tables()

def save_data_from_hash_tables():
    for topic, table in hash_tables.items():
        file_path = os.path.join(current_directory, json_files[topic])
        data = table.get_all()
        write_json_file(file_path, data)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    save_data_from_hash_tables()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@app.route('/check_ticket_status')
def check_ticket_status():
    
    return render_template('check_ticket_status.html')

@app.route('/ticket_status/<int:ticket_id>')
def ticket_status(ticket_id):
    user_email = session.get('email')
    for topic, table in hash_tables.items():
        ticket = table.retrieve(ticket_id)
        if ticket:
            
            break

    # If not found in hash table, check resolved JSON files
    if not ticket:
        for topic in json_files.keys():
            resolved_file_path = os.path.join(current_directory, f'resolved_{topic}.json')
            tickets = read_json_file(resolved_file_path)
            for t in tickets:
                if t['ticket id'] == ticket_id:
                    ticket = t
                    
                    break
            if ticket:
                break


    if ticket:
            if ticket['user-email'] != user_email:
                return render_template('unauthorized.html'), 403

            if ticket['status'] == 'resolved':
                return render_template('resolved_ticket.html', ticket=ticket)
            else:
                return render_template('ticket_status.html', ticket=ticket)
    return jsonify({'error': 'Ticket not found'}), 404

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    ticket_id = request.form.get('ticket_id')
    rating = request.form.get('rating')
    feedback = request.form.get('feedback')
    
    # Logic to save feedback, e.g., in a database or a separate feedback JSON file
    feedback_data = {
        'ticket_id': ticket_id,
        'rating': rating,
        'feedback': feedback,
        'user_email': session.get('email'),
        'help_topic': get_help_topic_by_ticket_id(ticket_id)
    }

    feedback_list.add_feedback(feedback_data)
    return render_template('feedback.html'), 200

def get_help_topic_by_ticket_id(ticket_id):
    for topic, table in hash_tables.items():
        ticket = table.retrieve(int(ticket_id))
        if ticket:
            return topic
    return None



@app.route('/admin')
def admin():
    feedback_data = feedback_list.get_all_feedback()
    if not feedback_data:
        print("No feedback data found.")
    else:
        print(f"Loaded feedback data: {feedback_data}")
    return render_template('admin.html', feedback_data=feedback_data)

@app.route('/ticket_details/<ticket_id>')
def ticket_details(ticket_id):
    ticket_data = None
    resolved_files = [
        'resolved_carpentery.json',
        'resolved_civil_mason.json',
        'resolved_electrical.json',
        'resolved_plumbing.json',
        'resolved_wifi_problem.json'
    ]
    for file_name in resolved_files:
        file_path = os.path.join(current_directory, file_name)
        tickets = read_json_file(file_path)
        for ticket in tickets:
            if str(ticket['ticket id']) == ticket_id:
                ticket_data = ticket
                break
        if ticket_data:
            break

    if not ticket_data:
        return "Ticket not found", 404

    return render_template('ticket_details.html', ticket=ticket_data)


if __name__ == '__main__':
    app.run(debug=True)