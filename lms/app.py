from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'password'  # Required for flash messages

# Function to load books from JSON
def load_books():
    try:
        with open('books.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save books to JSON
def save_books(books):
    with open('books.json', 'w') as file:
        json.dump(books, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple login validation logic (replace with real validation as needed)
        if username == 'admin' and password == 'password':  # Example credentials
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.')
    
    return render_template('login.html')

@app.route('/api/books', methods=['GET'])
def get_books():
    books = load_books()
    return jsonify(books)

@app.route('/api/books', methods=['POST'])
def add_book():
    new_book = request.json
    books = load_books()
    books.append(new_book)
    save_books(books)
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = load_books()
    books = [book for book in books if book['id'] != book_id]
    save_books(books)
    return jsonify({'message': 'Book deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
