from flask import render_template, request
import hashlib

from app.hash_calculator import hash_calculator_bp


@hash_calculator_bp.route('/')
def index():
    return render_template('hash_dashboard.html', title="Hash calculator")

@hash_calculator_bp.route('/hash_calculator', methods=['POST'])
def hash_string():
    hash_type = request.form['hash_type']
    string_to_hash = request.form['string_to_hash']
    if string_to_hash:
        if hash_type == 'md5':
            hashed_string = hashlib.md5(string_to_hash.encode()).hexdigest()
        elif hash_type == 'sha1':
            hashed_string = hashlib.sha1(string_to_hash.encode()).hexdigest()
        elif hash_type == 'sha256':
            hashed_string = hashlib.sha256(string_to_hash.encode()).hexdigest()
        else:
            return "Invalid hash type"
        
        return render_template('hash_result.html', hashed_string=hashed_string)
    return render_template('hash_dashboard.html')

