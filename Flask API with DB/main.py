from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False



db = SQLAlchemy(app)
ma = Marshmallow(app)
# obj = user_model

class Books(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    price=db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

class BookSchema(ma.Schema):
    class Meta:
        fields=["name","price"]
   
book_schema=BookSchema()
books_schema=BookSchema(many=True)

# @app.route('/book')
# def get_all_books():
#     return jsonify({'books':books_db})

@app.route('/book/<string:name>') 
def get_book(name):
    book=Books.query.filter_by(name=name).first()
    if book:
        return book_schema.jsonify(book)
        
    return jsonify({'message':'book not found'})

@app.route('/books',methods=['GET']) 
def get_books():
    book=Books.query.all()
    if book:
        return books_schema.jsonify(book)
        
    return jsonify({'message':'books not found'})




@app.route('/book',methods=['POST','GET'])
def create_book():
    if request.method=="POST":
        body_data = request.get_json() 
        print(body_data,"............")
        name=body_data["name"]
        price=body_data["price"]
        print("name..........",name)
        print("price.....",price)
        book=Books(name=name,price=price)
        db.session.add(book)
        db.session.commit()
    
    books=Books.query.all()
    print(books)

    return books_schema.jsonify(books)

 
@app.route("/book/addmultiple", methods=["POST"])
def add_multiple_user():
    # if request.method=="POST":
        return  user_add_multiple_data(request.get_json())

def user_add_multiple_data( data):
    print("this is data",data)

    # qry="INSERT INTO books(name, price) VALUES"
    for userdata in data:
        print(userdata["name"],"......")
        col1=userdata["name"]
        col2=userdata["price"]
        main = Books(name=col1, price=col2)
        db.session.add(main)
     
    db.session.commit()
    return jsonify({"message":"CREATED_SUCCESSFULLY"})


@app.route('/')
def home():
    return "hey"


if __name__=="__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()