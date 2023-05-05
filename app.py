from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from datetime import datetime
from sqlalchemy import func
import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)
class Product(db.Model):
    __tablename__ = 'products'
    productId = db.Column(db.String(200), primary_key=True)
    part_id = db.Column(db.Integer)
    area = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Product %r>' % self.productId
class Vendor(db.Model):
    __tablename__ = 'vendor'
    vendor_id = db.Column(db.String(200), primary_key=True)
    vendor_address = db.Column(db.Integer)
    vendor_phn = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Vendor %r>' % self.vendor_id
class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.String(200), primary_key=True)
    location_area = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Location %r>' % self.location_id


class Person(db.Model):
    __tablename__ = 'operationperson'
    operationperson_id = db.Column(db.String(200), primary_key=True)
    operationperson_phn = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Person %r>' % self.operationperson_id


class Inwarding(db.Model):
    __tablename__ = 'inwarding'
    inwarding_id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'))
    part_id = db.Column(db.Integer, db.ForeignKey('products.part_id'))
    area = db.Column(db.Integer, db.ForeignKey('products.area'))
    cost = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    remaining_area = db.Column(db.Integer)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.vendor_id'))
    vendor_address = db.Column(db.Integer, db.ForeignKey('vendor.vendor_address'))
    vendor_phn = db.Column(db.Integer, db.ForeignKey('vendor.vendor_phn'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    location_area = db.Column(db.Integer, db.ForeignKey('location.location_area'))
    operationperson_id = db.Column(db.Integer, db.ForeignKey('operationperson.operationperson_id'))
    operationperson_phn = db.Column(db.Integer, db.ForeignKey('operationperson.operationperson_phn'))
    inwarding_time = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product',  backref='inwarding',foreign_keys=[productId])
    part = db.relationship('Product', foreign_keys=part_id)
    area1 = db.relationship('Product', foreign_keys=area)
    vendorid = db.relationship("Vendor", foreign_keys=vendor_id)
    vendorphn = db.relationship("Vendor", foreign_keys=vendor_phn)
    vendoraddress = db.relationship("Vendor", foreign_keys=vendor_address)
    location = db.relationship("Location", foreign_keys=location_id)
    larea = db.relationship("Location", foreign_keys=location_area)

    operationperson = db.relationship("Person", foreign_keys=operationperson_id)
    operationpersonphn = db.relationship("Person", foreign_keys=operationperson_phn)

    def __repr__(self):
        return '<Inwarding %r>' % self.inwarding_id
class ProductMovement(db.Model):
    __tablename__ = 'productmovements'
    movement_id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('inwarding.productId'))
    part_id = db.Column(db.Integer, db.ForeignKey('inwarding.part_id'))
    area  =db.Column(db.Integer,db.ForeignKey('inwarding.area'))
    operationperson_id = db.Column(db.Integer, db.ForeignKey('inwarding.operationperson_id'))
    operationperson_phn = db.Column(db.Integer, db.ForeignKey("inwarding.operationperson_phn"))
    quantity = db.Column(db.Integer)
    from_location = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    to_location = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    movement_time = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Inwarding', foreign_keys=productId)
    larea= db.relationship('Inwarding', foreign_keys=area)
    fromLoc = db.relationship('Location', foreign_keys=from_location)
    toLoc = db.relationship('Location', foreign_keys=to_location)
    operationpersonid = db.relationship('Inwarding', foreign_keys=operationperson_id)
    operationpersonphn = db.relationship('Inwarding', foreign_keys=operationperson_phn)

    def __repr__(self):
        return '<ProductMovement %r>' % self.movement_id


@app.route('/', methods=["POST", "GET"])
def index():
    if (request.method == "POST") and ('productId' in request.form) and ("part_id" in request.form) and (
            "area" in request.form):
        productId= request.form["productId"]
        part_id = request.form["part_id"]
        area = request.form["area"]
        new_product = Product(productId=productId, part_id=part_id, area=area)
        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/")

        except:
            return "There Was an issue while add a new Product"

    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template("index.html", products=products)
@app.route('/get_remaining_area', methods=['GET', 'POST'])
def get_remaining_area():
  location_id = request.args.get('location_id')
  locations = Location.query.order_by(Location.date_created).all()
  remaining_area = None
  inwards = Inwarding.query \
      .join(Product, Inwarding.productId == Product.productId) \
      .add_columns(
      Inwarding.inwarding_id,
      Inwarding.productId,
      Inwarding.part_id,
      Inwarding.cost,
      Inwarding.area,
      Inwarding.quantity,
      Inwarding.location_id,
      Inwarding.location_area,
      Inwarding.operationperson_id,
      Inwarding.operationperson_phn,
      Inwarding.vendor_id,
      Inwarding.vendor_address,
      Inwarding.vendor_phn,
      (Inwarding.cost * Inwarding.quantity).label('Tcost'),
      (Inwarding.area * Inwarding.quantity).label('Tarea'),
      func.sum(Inwarding.area).label('total_area')  # Sum the area for each location
  ) \
      .group_by(Inwarding.inwarding_id) \
      .subquery()

  movs = ProductMovement.query \
      .join(Inwarding, ProductMovement.productId == Inwarding.productId) \
      .add_columns(
      ProductMovement.movement_id,
      ProductMovement.quantity,
      ProductMovement.productId,
      ProductMovement.part_id,
      ProductMovement.area,
      ProductMovement.operationperson_id,
      ProductMovement.operationperson_phn,
      ProductMovement.from_location,
      ProductMovement.to_location,
      ProductMovement.movement_time,
      (ProductMovement.area * ProductMovement.quantity).label('Tarea')) \
      .subquery()
  outward_movements = ProductMovement.query \
      .filter(ProductMovement.from_location == location_id) \
      .join(Product, ProductMovement.productId == Product.productId) \
      .add_columns(func.sum(ProductMovement.quantity * ProductMovement.area).label('total_area')) \
      .group_by(ProductMovement.productId) \
      .subquery()
  inward_movements = ProductMovement.query \
      .filter(ProductMovement.to_location == location_id) \
      .join(Product, ProductMovement.productId == Product.productId) \
      .add_columns(func.sum(ProductMovement.quantity * Product.area).label('total_area')) \
      .group_by(ProductMovement.productId) \
      .subquery()
  remaining_areas = db.session.query(
      locations.c.location_id,
      locations.c.location_area,
      func.coalesce(inwards.c.total_area, 0) -func.coalesce(outward_movements.c.total_area, 0) + func.coalesce(
          inward_movements.c.total_area, 0)
      .label('total_area')
  ).outerjoin(inwards, locations.c.location_id == inwards.c.location_id) \
      .outerjoin(outward_movements, Product.productId == outward_movements.c.productId) \
      .outerjoin(inward_movements, Product.productId == inward_movements.c.productIdd) \
      .group_by(locations.c.location_id) \
      .all()

  for location in remaining_areas:
      if location['location_id'] == location_id:
          remaining_area = location['location_area'] - location['total_area']
          break

  if remaining_area is None:
      return jsonify({'error': 'Location not found'})
  else:
      return jsonify({'remaining_area': remaining_area})


@app.route('/locations/', methods=["POST", "GET"])
def viewLocation():
    if (request.method == "POST") and ('location_id' in request.form) and ('location_area' in request.form):
        location_id = request.form["location_id"]
        location_area = request.form["location_area"]
        new_location = Location(location_id=location_id, location_area=location_area)
        try:
            db.session.add(new_location)
            db.session.commit()
            return redirect("/locations/")
        except:
            locations = Location.query.order_by(Location.date_created).all()
            return "There Was an issue while add a new Location"
    else:
        locations = Location.query.order_by(Location.date_created).all()
        return render_template("locations.html", locations=locations)
@app.route("/inwarding/", methods=["POST", "GET"])
def viewMovement():
    if request.method == "POST":
        productId = request.form["productId"]
        part_id = request.form["part_id"]
        area = request.form["area"]
        cost = request.form["cost"]
        quantity = request.form["quantity"]
        location_id = request.form["location_id"]
        location_area = request.form["location_area"]
        vendor_id = request.form["vendor_id"]
        vendor_address = request.form["vendor_address"]
        vendor_phn = request.form["vendor_phn"]
        operationperson_id = request.form["operationperson_id"]
        operationperson_phn = request.form["operationperson_phn"]
        existing_inward = Inwarding.query.filter_by(productId=productId, area=area, vendor_address=vendor_address,
                                                     cost=cost, location_id=location_id,location_area=location_area,
                                                    operationperson_id=operationperson_id,
                                                    operationperson_phn=operationperson_phn, vendor_id=vendor_id,
                                                    vendor_phn=vendor_phn
                                                    ).first()

        if existing_inward:
            existing_inward.quantity += int(quantity)
            db.session.commit()
        else:
            new_inward = Inwarding(
                productId=productId,
                part_id=part_id,
                area=area,
                cost=cost,
                quantity=quantity,
                location_id=location_id,
                location_area=location_area,
                operationperson_id=operationperson_id,
                operationperson_phn=operationperson_phn,
                vendor_id=vendor_id,
                vendor_address=vendor_address,
                vendor_phn=vendor_phn
            )
            try:
                db.session.add(new_inward)
                db.session.commit()
            except:
                return "There was an issue while adding a new entry"

        return redirect("/inwarding/")

    else:
        products = Product.query.order_by(Product.date_created).all()
        locations = Location.query.order_by(Location.date_created).all()
        persons = Person.query.order_by(Person.date_created).all()
        vendors = Vendor.query.order_by(Vendor.date_created).all()
        form_dict = request.form.to_dict()
        total_tarea_subquery = db.session.query(
            Inwarding.location_id,
            func.sum(Inwarding.area * Inwarding.quantity).label('total_tarea')
        ).group_by(Inwarding.location_id).subquery()

        inwards = Inwarding.query \
            .join(Product, Inwarding.productId == Product.productId) \
            .add_columns(
            Inwarding.inwarding_id,
            Inwarding.productId,
            Inwarding.part_id,
            Inwarding.cost,
            Inwarding.area,
            Inwarding.quantity,
            Inwarding.location_id,
            Inwarding.location_area,
            Inwarding.operationperson_id,
            Inwarding.operationperson_phn,
            Inwarding.vendor_id,
            Inwarding.vendor_address,
            Inwarding.vendor_phn,
            (Inwarding.cost * Inwarding.quantity).label('Tcost'),
            (Inwarding.area * Inwarding.quantity).label('Tarea'),
            func.sum(Inwarding.area).label('total_area')
        ) \
            .group_by(Inwarding.inwarding_id) \
            .all()
        remaining_areas = {}
        for location in locations:
            location_id = location.location_id
            selected_location_id = request.args.get('location_id')
            location_area = location.location_area
            total_area = sum([inward.Tarea for inward in inwards if inward.location_id == location_id])
            remaining_areas[location_area] = {'Remaining Area': location_area - total_area, 'Total Area': location_area,
                                              'Location ID': location_id}

        return render_template("inwarding.html", inwards=inwards, products=products, locations=locations,
                               persons=persons, vendors=vendors, remaining_areas=remaining_areas)
@app.route("/movements/", methods=["POST", "GET"])
def viewMovements():
    if request.method == "POST":
        print(request.form)
        productId = request.form["productId"]
        part_id = request.form["part_id"]
        area =request.form["area"]
        quantity = int(request.form["quantity"])
        operationperson_id = request.form["operationperson_id"]
        operationperson_phn = request.form["operationperson_phn"]
        fromLocation = request.form["fromLocation"]
        toLocation = request.form["toLocation"]
        location_id = Location.query.filter_by(location_id=fromLocation).first().location_id
        location_id1= Location.query.filter_by(location_id=toLocation).first().location_id
        inwarding_entry = Inwarding.query.filter_by(productId=productId, part_id=part_id,
                                                    location_id=location_id).first()
        outwarding_entry = Inwarding.query.filter_by(productId=productId, part_id=part_id,
                                                    location_id=location_id1).first()
        if outwarding_entry is None:
            new_inwarding = Inwarding(productId=productId, part_id=part_id, area=area, quantity=0,cost=0)

            outwarding_entry = new_inwarding
        existing_movement = ProductMovement.query.filter_by(productId=productId, from_location=fromLocation,
                                                            to_location=toLocation).first()
        locations = Location.query.order_by(Location.date_created).all()
        inwards = Inwarding.query \
            .join(Product, Inwarding.productId == Product.productId) \
            .add_columns(
            Inwarding.inwarding_id,
            Inwarding.productId,
            Inwarding.part_id,
            Inwarding.cost,
            Inwarding.area,
            Inwarding.quantity,
            Inwarding.location_id,
            Inwarding.operationperson_id,
            Inwarding.operationperson_phn,
            Inwarding.vendor_id,
            Inwarding.vendor_address,
            Inwarding.vendor_phn,
            (Inwarding.cost * Inwarding.quantity).label('Tcost'),
            (Inwarding.area * Inwarding.quantity).label('Tarea'),
            func.sum(Inwarding.area).label('total_area')  # Sum the area for each location
        ) \
            .group_by(Inwarding.inwarding_id) \
            .all()
        remaining_areas = {}
        for location in locations:
            location_id = location.location_id
            selected_location_id = request.args.get('location_id')
            location_area = location.location_area
            total_area = sum([inward.Tarea for inward in inwards if inward.location_id == location_id])
            remaining_areas[location_area] = {'Remaining Area': location_area - total_area, 'Total Area': location_area,
                                              'Location ID': location_id}
            rest = remaining_areas.values()
            print(rest)



        if existing_movement:
            existing_movement.quantity += quantity
            db.session.commit()
        else:
            new_movement = ProductMovement(
                productId=productId, part_id=part_id,area=area, operationperson_id=operationperson_id,
                operationperson_phn=operationperson_phn, quantity=quantity, from_location=fromLocation,
                to_location=toLocation)
            try:
                db.session.add(new_movement)
                db.session.commit()
            except:
                return jsonify({"message": "There was an issue while adding a new Movement."})

        inwarding_entry.quantity -= quantity
        outwarding_entry.quantity +=quantity
        db.session.commit()

        return redirect("/movements/")

    else:
        inwarding = Inwarding.query.order_by(Inwarding.inwarding_time).all()
        locations = Location.query.order_by(Location.location_id).all()
        movs = ProductMovement.query \
            .join(Inwarding, ProductMovement.productId == Inwarding.productId) \
            .add_columns(
            ProductMovement.movement_id,
            ProductMovement.quantity,
            ProductMovement.productId,
            ProductMovement.part_id,
            ProductMovement.area,
            ProductMovement.operationperson_id,
            ProductMovement.operationperson_phn,
            ProductMovement.from_location,
            ProductMovement.to_location,
            ProductMovement.movement_time,
        (ProductMovement.area * ProductMovement.quantity).label('Tarea')) \
            .all()
        movements = ProductMovement.query.order_by(ProductMovement.movement_time).all()
        return render_template("movements.html", movements=movs, inwarding=inwarding, locations=locations)
@app.route("/product-balance/", methods=["POST", "GET"])
def productBalanceReport():
    movs = ProductMovement.query. \
        join(Product, ProductMovement.productId == Product.productId). \
        add_columns(
        ProductMovement.productId,
        ProductMovement.quantity,
        ProductMovement.from_location,
        ProductMovement.to_location,
        ProductMovement.movement_time). \
        order_by(ProductMovement.productId). \
        order_by(ProductMovement.movement_id). \
        all()
    balancedDict = defaultdict(lambda: defaultdict(dict))
    tempProduct = ''
    for mov in movs:
        row = mov[0]
        if (tempProduct == row.productId):
            if (row.to_location and not "quantity" in balancedDict[row.productId][row.to_location]):
                balancedDict[row.productId][row.to_location]["quantity"] = 0
            elif (row.from_location and not "quantity" in balancedDict[row.productId][row.from_location]):
                balancedDict[row.productId][row.from_location]["quantity"] = 0
            if (row.to_location and "quantity" in balancedDict[row.productId][row.to_location]):
                balancedDict[row.productId][row.to_location]["quantity"] += row.quantity
            pass
        else:
            tempProduct = row.productId
            if (row.to_location and not row.from_location):
                if (not tempProduct in balancedDict):
                    balancedDict[tempProduct] = defaultdict(dict)
                balancedDict[tempProduct][row.to_location]["quantity"] = row.quantity
            else:
                balancedDict[tempProduct][row.to_location]["quantity"] = row.quantity

    return render_template("product-balance.html", movements=balancedDict)
@app.route("/movements/get-from-locations/", methods=["POST"])
def getLocations():
    product = request.form["productId"]
    location = request.form["location_id"]
    locationDict = defaultdict(lambda: defaultdict(dict))
    locations = Inwarding.query. \
        filter(ProductMovement.productId == product). \
        filter(ProductMovement.to_location != ''). \
        add_columns(ProductMovement.from_location, ProductMovement.to_location, ProductMovement.quantity). \
        all()
    for key, location in enumerate(locations):
        if (locationDict[location.to_location] and locationDict[location.to_location]["quantity"]):
            locationDict[location.to_location]["quantity"] += location.quantity
        else:
            locationDict[location.to_location]["quantity"] = location.quantity
    return locationDict
@app.route("/vendors/", methods=["POST", "GET"])
def viewVendors():
    if (request.method == "POST") and ('vendor_id' in request.form) and ("vendor_address" in request.form) and (
            "vendor_phn" in request.form):
        vendor_id = request.form["vendor_id"]
        vendor_address = request.form["vendor_address"]
        vendor_phn = request.form["vendor_phn"]
        new_vendor = Vendor(vendor_id=vendor_id, vendor_address=vendor_address, vendor_phn=vendor_phn)
        try:
            db.session.add(new_vendor)
            db.session.commit()
            return redirect("/vendors/")

        except:
            vendors = Vendor.query.order_by(Vendor.date_created).all()
            return "There Was an issue while add a new vendor"
    else:
        vendors = Vendor.query.order_by(Vendor.date_created).all()
        return render_template("vendors.html", vendors=vendors)


@app.route('/products/', methods=["POST", "GET"])
def viewProduct():
    if (request.method == "POST") and ('productId' in request.form) and ("part_id" in request.form) and (
            "area" in request.form):
        print(request.form)
        productId = request.form["productId"]
        part_id = request.form["part_id"]
        area = request.form["area"]
        new_product = Product(productId=productId, part_id=part_id, area=area)
        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/products/")

        except:
            products = Product.query.order_by(Product.date_created).all()
            return "There Was an issue while add a new Product"
    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template("products.html", products=products)


@app.route('/underprocess/', methods=["POST", "GET"])
def under():
    return render_template("underprocess.html")


@app.route('/operationperson/', methods=["POST", "GET"])
def viewPerson():
    if (request.method == "POST") and ('operationperson_id' in request.form) and (
            "operationperson_phn" in request.form):
        operationperson_id = request.form["operationperson_id"]
        operationperson_phn = request.form["operationperson_phn"]
        new_person = Person(operationperson_id=operationperson_id, operationperson_phn=operationperson_phn)
        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect("/operationperson/")

        except:
            persons = Person.query.order_by(Person.date_created).all()
            return "There Was an issue while add a new Product"
    else:
        persons = Person.query.order_by(Person.date_created).all()
        return render_template("operationperson.html", persons=persons)



@app.route("/get_part_id", methods=["POST"])
def get_part_id():
    productId = request.form["productId"]
    product = Product.query.filter_by(productId=productId).first()
    if product:
        return {"part_id": product.part_id, "area": product.area}
    else:
        return {"part_id": ""}
@app.route("/get_vend_id", methods=["POST"])
def get_vend_id():
    vendor_id = request.form["vendor_id"]
    vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        return {"vendor_address": vendor.vendor_address, "vendor_phn": vendor.vendor_phn}
    else:
        return {"vendor_address": ""}
@app.route("/get_person_id", methods=["POST"])
def get_person_id():
    operationperson_id = request.form["operationperson_id"]
    person = Person.query.filter_by(operationperson_id=operationperson_id).first()
    if person:
        return {"operationperson_phn": person.operationperson_phn}
    else:
        return {"operationperson_phn": ""}

@app.route("/get_location_area", methods=["POST"])
def get_location_area():
    location_id = request.form["location_id"]
    location = Location.query.filter_by(location_id=location_id).first()

    if location:
        return {"location_area": location.location_area}
    else:
        return {"location_area": ""}

@app.route("/delete-product/<name>")
def deleteProduct(name):
    product = Product.query.get_or_404(name)
    old_product_id = product.productId

    inwardings = Inwarding.query.filter_by(productId=old_product_id).all()
    for inwarding in inwardings:
        db.session.delete(inwarding)
        db.session.delete(product)
        db.session.commit()

    return redirect("/products/")
@app.route("/update-product/<name>", methods=["POST", "GET"])
def updateProduct(name):
    product = Product.query.get_or_404(name)
    old_product = product.productId
    if request.method == "POST":
        print(request.form['productId'])
        product.productId    = request.form['productId']
        product.part_id = request.form['part_id']
        product.area = request.form['area']
        try:
            db.session.commit()
            updateProductInMovements(old_product, request.form['productId'])
            updateProductInMovements(old_product,request.form["productId"])
            return redirect("/products/")

        except:
            return "There was an issue while updating the vendor"
    else:
        part_id = request.args.get('part_id', '')
        area = request.args.get('area', '')
        return render_template("update-product.html", product=product, part_id=part_id, area=area)


@app.route("/delete-person/<name>")
def deletePerson(name):
    person_to_delete = Person.query.get_or_404(name)

    try:
        db.session.delete(person_to_delete)
        db.session.commit()
        return redirect("/operationperson/")
    except:
        return "There was an issue while deleting the Person"


@app.route("/delete-vendor/<name>")
def deleteVendor(name):
    vendor_to_delete = Vendor.query.get_or_404(name)

    try:
        db.session.delete(vendor_to_delete)
        db.session.commit()
        return redirect("/vendors/")
    except:
        return "There was an issue while deleting the Vendor"


@app.route("/dub-products/", methods=["POST", "GET"])
def getPDublicate():
    productId = request.form["productId"]
    products = Product.query. \
        filter(Product.productId == productId). \
        all()
    print(products)
    if products:
        return {"output": False}
    else:
        return {"output": True}


@app.route("/dub-person/", methods=["POST", "GET"])
def getPeDublicate():
    operationperson_id = request.form["operationperson_id"]
    persons = Person.query. \
        filter(Person.operationperson_id == operationperson_id). \
        all()
    print(persons)
    if persons:
        return {"output": False}
    else:
        return {"output": True}


@app.route("/dub-vendors/", methods=["POST", "GET"])
def getVDublicate():
    vendor_id = request.form["vendor_id"]
    vendors = Vendor.query. \
        filter(Vendor.vendor_id == vendor_id). \
        all()
    print(vendors)
    if vendors:
        return {"output": False}
    else:
        return {"output": True}


@app.route("/dub-locations/", methods=["POST", "GET"])
def getDublicate():
    location = request.form["location"]
    locations = Location.query. \
        filter(Location.location_id == location). \
        all()
    print(locations)
    if locations:
        return {"output": False}
    else:
        return {"output": True}


@app.route("/delete-location/<name>")
def deleteLocation(name):
    location_to_delete = Location.query.get_or_404(name)

    try:
        db.session.delete(location_to_delete)
        db.session.commit()
        return redirect("/locations/")
    except:
        return "There was an issue while deleteing the Location"

@app.route('/check_quantity/', methods=['POST'])
def check_quantity():
    
    productId = request.form['productId']
    quantity = request.form['quantity']
    fromLocation = request.form["fromLocation"]
    location_entry = Inwarding.query.filter_by(location_id=fromLocation).first()
    if location_entry is None:
        return 'false'
    location_id = location_entry.location_id
    inwarding_entry = Inwarding.query.filter_by(productId=productId, location_id=location_id).first()
    if inwarding_entry is not None and int(quantity) <= inwarding_entry.quantity:
        return 'true'
    else:
        return 'false'
def updateLocationInMovements(oldLocation, newLocation):
    movement = ProductMovement.query.filter(ProductMovement.from_location == oldLocation).all()
    movement2 = ProductMovement.query.filter(ProductMovement.to_location == oldLocation).all()
    for mov in movement2:
        mov.to_location = newLocation
    for mov in movement:
        mov.from_location = newLocation

    db.session.commit()


def updateProductInMovements(old_product, newProduct):
    movement = ProductMovement.query.filter(ProductMovement.productId == old_product).all()
    inw       = Inwarding.query.filter(Inwarding.productId == old_product).all()
    for inwards in inw:
        inwards.productId =newProduct

    for mov in movement:
        mov.productId = newProduct

    db.session.commit()


if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=3494)
