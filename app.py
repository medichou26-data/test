from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

# Configuration MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'librarydb'

# Configuration Upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

mysql = MySQL(app)

# Créer les dossiers nécessaires
os.makedirs(os.path.join(UPLOAD_FOLDER, 'books'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'covers'), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HOME
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM authors")
    total_authors = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM categories")
    total_categories = cur.fetchone()[0]
    
    # Derniers livres ajoutés
    cur.execute("""
        SELECT books.id, books.title, authors.name, books.cover_image
        FROM books
        JOIN authors ON books.author_id = authors.id
        ORDER BY books.id DESC LIMIT 6
    """)
    recent_books = cur.fetchall()
    
    cur.close()
    return render_template("index.html", 
                         total_books=total_books,
                         total_authors=total_authors,
                         total_categories=total_categories,
                         recent_books=recent_books)

# CRUD AUTEURS
@app.route('/authors')
def authors():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT authors.id, authors.name, authors.bio, COUNT(books.id) as book_count
        FROM authors
        LEFT JOIN books ON authors.id = books.author_id
        GROUP BY authors.id
    """)
    data = cur.fetchall()
    cur.close()
    return render_template("authors.html", authors=data)

@app.route('/add_author', methods=['POST'])
def add_author():
    name = request.form['name']
    bio = request.form.get('bio', '')
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO authors (name, bio) VALUES (%s, %s)", (name, bio))
    mysql.connection.commit()
    cur.close()
    
    flash('Auteur ajouté avec succès!', 'success')
    return redirect(url_for('authors'))

@app.route('/delete_author/<int:id>')
def delete_author(id):
    cur = mysql.connection.cursor()
    # Vérifier si l'auteur a des livres
    cur.execute("SELECT COUNT(*) FROM books WHERE author_id=%s", (id,))
    count = cur.fetchone()[0]
    
    if count > 0:
        flash(f'Impossible de supprimer cet auteur. {count} livre(s) lui sont associés.', 'danger')
    else:
        cur.execute("DELETE FROM authors WHERE id=%s", (id,))
        mysql.connection.commit()
        flash('Auteur supprimé avec succès!', 'success')
    
    cur.close()
    return redirect(url_for('authors'))

# CRUD CATÉGORIES
@app.route('/categories')
def categories():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT categories.id, categories.name, categories.description, COUNT(books.id) as book_count
        FROM categories
        LEFT JOIN books ON categories.id = books.category_id
        GROUP BY categories.id
    """)
    data = cur.fetchall()
    cur.close()
    return render_template("categories.html", categories=data)

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    description = request.form.get('description', '')
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
    mysql.connection.commit()
    cur.close()
    
    flash('Catégorie ajoutée avec succès!', 'success')
    return redirect(url_for('categories'))

@app.route('/delete_category/<int:id>')
def delete_category(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM books WHERE category_id=%s", (id,))
    count = cur.fetchone()[0]
    
    if count > 0:
        flash(f'Impossible de supprimer cette catégorie. {count} livre(s) lui sont associés.', 'danger')
    else:
        cur.execute("DELETE FROM categories WHERE id=%s", (id,))
        mysql.connection.commit()
        flash('Catégorie supprimée avec succès!', 'success')
    
    cur.close()
    return redirect(url_for('categories'))

# CRUD LIVRES
@app.route('/books')
def books():
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    cur = mysql.connection.cursor()
    
    query = """
        SELECT books.id, books.title, authors.name, categories.name, 
               books.year, books.pdf_file, books.cover_image, books.description
        FROM books
        JOIN authors ON books.author_id = authors.id
        JOIN categories ON books.category_id = categories.id
        WHERE 1=1
    """
    
    params = []
    if search:
        query += " AND (books.title LIKE %s OR authors.name LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category_filter:
        query += " AND books.category_id = %s"
        params.append(category_filter)
    
    query += " ORDER BY books.id DESC"
    
    cur.execute(query, params)
    data = cur.fetchall()

    cur.execute("SELECT * FROM authors ORDER BY name")
    authors = cur.fetchall()

    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()

    cur.close()
    return render_template("books.html", books=data, authors=authors, 
                         categories=categories, search=search, 
                         category_filter=category_filter)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author_id = request.form['author_id']
    category_id = request.form['category_id']
    year = request.form['year']
    description = request.form.get('description', '')
    
    # Upload PDF
    pdf_filename = None
    if 'pdf_file' in request.files:
        pdf = request.files['pdf_file']
        if pdf and pdf.filename and allowed_file(pdf.filename):
            pdf_filename = secure_filename(pdf.filename)
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], 'books', pdf_filename))
    
    # Upload Cover
    cover_filename = 'default-cover.jpg'
    if 'cover_image' in request.files:
        cover = request.files['cover_image']
        if cover and cover.filename and allowed_file(cover.filename):
            cover_filename = secure_filename(cover.filename)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], 'covers', cover_filename))

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO books (title, author_id, category_id, year, description, pdf_file, cover_image)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (title, author_id, category_id, year, description, pdf_filename, cover_filename))
    mysql.connection.commit()
    cur.close()

    flash('Livre ajouté avec succès!', 'success')
    return redirect(url_for('books'))

@app.route('/book/<int:id>')
def book_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT books.*, authors.name as author_name, categories.name as category_name
        FROM books
        JOIN authors ON books.author_id = authors.id
        JOIN categories ON books.category_id = categories.id
        WHERE books.id = %s
    """, (id,))
    book = cur.fetchone()
    cur.close()
    
    if not book:
        flash('Livre introuvable', 'danger')
        return redirect(url_for('books'))
    
    return render_template("book_detail.html", book=book)

@app.route('/edit_book/<int:id>')
def edit_book(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cur.fetchone()
    
    cur.execute("SELECT * FROM authors ORDER BY name")
    authors = cur.fetchall()
    
    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()
    
    cur.close()
    return render_template("edit_book.html", book=book, authors=authors, categories=categories)

@app.route('/update_book/<int:id>', methods=['POST'])
def update_book(id):
    title = request.form['title']
    author_id = request.form['author_id']
    category_id = request.form['category_id']
    year = request.form['year']
    description = request.form.get('description', '')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT pdf_file, cover_image FROM books WHERE id=%s", (id,))
    current_files = cur.fetchone()
    
    pdf_filename = current_files[0]
    cover_filename = current_files[1]
    
    # Update PDF if new file uploaded
    if 'pdf_file' in request.files:
        pdf = request.files['pdf_file']
        if pdf and pdf.filename and allowed_file(pdf.filename):
            pdf_filename = secure_filename(pdf.filename)
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], 'books', pdf_filename))
    
    # Update Cover if new file uploaded
    if 'cover_image' in request.files:
        cover = request.files['cover_image']
        if cover and cover.filename and allowed_file(cover.filename):
            cover_filename = secure_filename(cover.filename)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], 'covers', cover_filename))
    
    cur.execute("""
        UPDATE books
        SET title=%s, author_id=%s, category_id=%s, year=%s, 
            description=%s, pdf_file=%s, cover_image=%s
        WHERE id=%s
    """, (title, author_id, category_id, year, description, pdf_filename, cover_filename, id))
    mysql.connection.commit()
    cur.close()

    flash('Livre modifié avec succès!', 'success')
    return redirect(url_for('books'))

@app.route('/delete_book/<int:id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Livre supprimé avec succès!', 'success')
    return redirect(url_for('books'))

if __name__ == "__main__":
    app.run(debug=True)