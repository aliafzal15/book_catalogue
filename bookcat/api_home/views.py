from bookcat.api_home import home
from flask import session
from flask import g
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required
from bookcat.api_home.forms import EditBookForm, CreateBookForm

@home.route('/home/')
def get_home():
    return 'Welcome To Home'

@home.route('/home/add/publications')
def add_data_publication():
    from bookcat.shared_models import Publication
    p2 = Publication("Paramount Press")
    p3 = Publication("Oracle Books Inc")
    p4 = Publication("Vintage Books and Comics")
    p5 = Publication("Trolls Press")
    p6 = Publication("Broadway Press")
    p7 = Publication("Downhill Publishers")
    p8 = Publication("Kingfisher Inc")

    from bookcat import db
    db.session.add_all([p2, p3, p4, p5, p6, p7, p8])
    db.session.commit()

    return 'Added Data in Publication Table'

@home.route('/home/add/books')
def add_data_books():
    from bookcat.shared_models import Books
    b1 = Books("Miky's Delivery Service", "William Dobelli", 3.9, "ePub", "broom-145379.svg", 123, 1)
    b2 = Books("The Secret Life of Walter Kitty", "Kitty Stiller", 4.1, "Hardcover", "cat-150306.svg", 133, 1)
    b3 = Books("The Empty Book of Life", "Roy Williamson", 4.2, "eBook", "book-life-34063.svg", 153, 1)
    b4 = Books("Life After Dealth", "Nikita Kimmel", 3.8, "Paperback", "mummy-146868.svg", 175, 2)
    b5 = Books("Sali The Dali", "Charles Rowling", 4.6, "Hardcover", "el-salvador-dali-889515.jpg", 253, 2)
    b6 = Books("Taming Dragons", "James Vonnegut", 4.5, "MassMarket Paperback", "dragon-23164.svg", 229, 2)
    b7 = Books("The Singing Magpie", "Oscar Steinbeck", 5, "Hardcover", "magpie-147852.svg", 188, 3)
    b8 = Books("Mr. Incognito", "Amelia Funke", 4.2, "Hardcover", "incognito-160143.svg", 205, 3)
    b9 = Books("A Dog without purpose", "Edgar Dahl", 4.8, "MassMarket Paperback", "dog-159271.svg", 300, 4)
    b10 = Books("A Frog's Life", "Herman Capote", 3.9, "MassMarket Paperback", "amphibian-150342.svg", 190, 4)
    b11 = Books("Logan Returns", "Margaret Elliot", 4.6, "Hardcover", "wolf-153648.svg", 279, 5)
    b12 = Books("Thieves of Kaalapani", "Mohit Gustav", 4.1, "Paperback", "boat-1296201.svg", 270, 5)
    b13 = Books("As Men Thinketh", "Edward McPhee", 4.5, "Paperback", "cranium-2028555.svg", 124, 6)
    b14 = Books("Mathematics of Music", "Mary Turing", 4.5, "Hardcover", "music-306008.svg", 120, 6)
    b15 = Books("The Mystery of Mandalas", "Jack Morrison", 4.2, "Paperback", "mandala-1817599.svg", 221, 6)
    b16 = Books("The Sacred Book of Kairo", "Heidi Zimmerman", 3.8, "ePub", "book-1294676.svg", 134, 7)
    b17 = Books("Love is forever, As Long as it lasts", "Kovi O'Hara", 4.5, "Hardcover", "love-2026554.svg", 279, 8)
    b18 = Books("Order in Chaos", "Wendy Sherman", 3.5, "MassMarket Paperback", "chaos-1769656.svg", 140, 8)

    from bookcat import db
    db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18])
    db.session.commit()

    return 'Added Data in Books Table'

@home.route('/home/get/books/')
def get_books():

    from bookcat.shared_models import Books
    all = Books.query.all()
    book1 = Books.query.first()
    book2 = Books.query.get(2)  #return on the basis of primary key passed in get(2)
    book3 = Books.query.filter_by(id=1).first() #filtering on the basis of a field
    book4 = Books.query.order_by(Books.title).all()

    return book3.title


@home.route('/home/update/books')
def update_books():

    from bookcat.shared_models import Books
    book1 = Books.query.get(16)
    book1.format = 'hardcover2'

    from bookcat import db
    db.session.commit()

    book1 = Books.query.get(16)
    return book1.format


@home.route('/home/session/')
def session_data():

    if 'name' not in session:         #refrences secret_key in config.py so this attribute must exist in config.py
        session['name'] = 'Ali'
    return "Session added" + g.string


@home.route('/home/books')
def display_books():
    from bookcat.shared_models import Books
    books = Books.query.all()
    return render_template('home.html', books=books)

@home.route('/home/books/publisher/<publisher_id>')
def display_publisher(publisher_id):
    from bookcat.shared_models import Publication
    from bookcat.shared_models import Books

    publisher = Publication.query.filter_by(id=publisher_id).first()
    publisher_books = Books.query.filter_by(pub_id=publisher.id).all()

    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books)


@home.route('/book/delete/<book_id>', methods=['GET','POST'])
@login_required
def delete_book(book_id):
    from bookcat.shared_models import Books

    book = Books.query.get(book_id)

    if request.method == 'POST':

        from bookcat import db
        db.session.delete(book)
        db.session.commit()
        flash('Book Deleted Successfully')
        return redirect(url_for('api_home.display_books'))
    return render_template('delete_book.html', book=book, book_id=book.id)

@home.route('/edit/book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    from bookcat.shared_models import Books

    book = Books.query.get(book_id)
    form = EditBookForm(obj=book)  #Pre-populates the data in the form
    if form.validate_on_submit():
        book.title =form.title.data
        book.format =form.format.data
        book.num_pages = form.num_pages.data

        from bookcat import db
        db.session.add(book)
        db.session.commit()
        flash('Book Updated Successfully')
        return redirect(url_for('api_home.display_books'))
    return render_template('edit_book.html', form=form)


@home.route('/create/book/<pub_id>', methods=['GET', 'POST'])
@login_required
def create_book(pub_id):
    from bookcat.shared_models import Books

    form = CreateBookForm()

    if form.validate_on_submit():
        book =Books(title=form.title.data, author=form.author.data, avg_rating=form.rating.data,format=form.format.data,
                    image=form.img_url.data, num_pages=form.num_pages.data, pub_id=form.pub_id.data)

        from bookcat import db
        db.session.add(book)
        db.session.commit()
        flash('Book added Successfully')
        return redirect(url_for('api_home.display_publisher', publisher_id=book.pub_id))
    return render_template('create_book.html', form=form)