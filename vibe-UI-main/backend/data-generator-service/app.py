from flask import Flask, jsonify
from flask_cors import CORS
import time
import random
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Function to generate random data for different datasets
def generate_dataset_1():
    categories = ['Sales', 'Finance', 'Tech']
    regions = ['North', 'South', 'East', 'West']
    years = [2023, 2024]
    return [
        {
            'id': i,
            'category': random.choice(categories),
            'region': random.choice(regions),
            'value': random.randint(10, 100),
            'date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'year': random.choice(years)
        }
        for i in range(1, 21)
    ]

def generate_dataset_2():
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer']
    banks = ['Bank A', 'Bank B', 'Bank C']
    years = [2023, 2024]
    return [
        {
            'id': i,
            'transaction_type': random.choice(transaction_types),
            'bank': random.choice(banks),
            'amount': random.randint(100, 1000),
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
            'year': random.choice(years)
        }
        for i in range(1, 21)
    ]

import random
from datetime import datetime, timedelta

# Function to generate recruitment dataset
def generate_recruitment_data():
    technologies = ['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Ruby', 'Swift', 'Kotlin']
    technology_domains = ['Web Development', 'AI/ML', 'Cloud Computing', 'Cybersecurity', 'Data Science', 'Mobile Development']
    functional_domains = ['Finance', 'Healthcare', 'E-commerce', 'Education', 'Automotive', 'Retail']
    regions = ['North', 'South', 'East', 'West']
    experience_range = list(range(1, 21))  # Years of experience from 1 to 20
    compensation_bands = ['40K-60K', '60K-80K', '80K-100K', '100K-120K', '120K-150K']
    recruitment_statuses = ['In Progress', 'Rejected', 'Submitted', 'In Consideration', 'Back Fill', 'Backed Out']
    
    def random_phone_number():
        return f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    def random_email(name):
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
        return f"{name.lower().replace(' ', '.')}@{random.choice(domains)}"

    candidates = []
    
    for i in range(1, 51):  # Generate 50 candidates
        name = f"Candidate {i}"
        candidate = {
            'id': i,
            'candidate_name': name,
            'technology': random.choice(technologies),
            'technology_domain': random.choice(technology_domains),
            'functional_domain': random.choice(functional_domains),
            'region': random.choice(regions),
            'years_of_experience': random.choice(experience_range),
            'compensation_band': random.choice(compensation_bands),
            'recruitment_status': random.choice(recruitment_statuses),
            'phone_number': random_phone_number(),
            'email_address': random_email(name)
        }
        candidates.append(candidate)

    return candidates



def generate_dataset_3():
    departments = ['HR', 'Marketing', 'Engineering']
    tasks = ['Hiring', 'Budget Planning', 'System Upgrade']
    years = [2023, 2024]
    return [
        {
            'id': i,
            'department': random.choice(departments),
            'task': random.choice(tasks),
            'completion_rate': random.randint(50, 100),
            'deadline': (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'year': random.choice(years)
        }
        for i in range(1, 21)
    ]

@app.route('/api/data', methods=['GET'])
def get_random_data():
    time.sleep(1)  # Simulate network delay
    random_choice = random.randint(1, 5)  # Generate a random number (1, 2, 3, 4, or 5)
    #random_choice= 4
    if random_choice == 1:
        return jsonify(generate_dataset_1())
    elif random_choice == 2:
        return jsonify(generate_dataset_2())
    elif random_choice == 3:
        return jsonify(generate_dataset_3())
    elif random_choice == 4:
        return jsonify(generate_recruitment_data())
    elif random_choice == 5:
        # Return sample finance data
        sample_data_path = os.path.join(os.path.dirname(__file__), 'sample_finance_data.json')
        if os.path.exists(sample_data_path):
            with open(sample_data_path, 'r') as f:
                sample_data = json.load(f)
            return jsonify(sample_data)
        else:
            # Fallback to recruitment data if sample file not found
            return jsonify(generate_recruitment_data())
    

if __name__ == '__main__':
    app.run(port=5001, debug=True)
