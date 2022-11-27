from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, EmailField, TextAreaField, RadioField, \
    DateField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
import json
import sql_credentials
import pdfkit
import os, sys, subprocess, platform
from datetime import datetime


# Flask app Start
app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY_12312312312"
bcrypt = Bcrypt(app)

# CORS settings
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# MYSQL connection
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{sql_credentials.user}:{sql_credentials.password}@{sql_credentials.host}:{sql_credentials.port}/users'
db = SQLAlchemy(app)

# login manager
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# pdfkit stuff
if platform.system() == "Windows":
    pdfkit_config = pdfkit.configuration(
        wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
else:
    os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable)
    WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
                                       stdout=subprocess.PIPE).communicate()[0].strip()
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


Base = declarative_base()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    userType = db.Column(db.String(50), nullable=False)

    # userTypes:
    # admin- full access
    # employee- create customers/products/orders
    # customer- view only

    # Return as a dict for easy processing
    # https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r>' % self.email


class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=4, max=80)])
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=4, max=80)])
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Register")


class SearchUserForm(FlaskForm):
    searchQuery = StringField(validators=[InputRequired()])
    submitSearch = SubmitField("Search")


class CreateUserForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=4, max=80)])
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    userType = SelectField('User Type',
                           choices=[("admin", "Admin"), ("employee", "Employee"), ("customer", "Customer")])
    searchQuery = StringField()
    submitCreate = SubmitField("Create")


class Products(db.Model):
    customerID = db.Column(db.Integer)
    oemID = db.Column(db.Integer, primary_key=True)
    productType = db.Column(db.String)
    title = db.Column(db.String)
    productDescription = db.Column(db.String)
    colorNotes = db.Column(db.String)
    packagingNotes = db.Column(db.String)
    productNotes = db.Column(db.String)
    serviceNotes = db.Column(db.String)
    insert = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r>' % self.oemID


class ProductForm(FlaskForm):
    customerID = SelectField(choices=[])
    productType = StringField(validators=[InputRequired()])
    title = StringField(validators=[InputRequired()])
    productDescription = TextAreaField()
    colorNotes = TextAreaField()
    packagingNotes = TextAreaField()
    productNotes = TextAreaField()
    serviceNotes = TextAreaField()
    insert = TextAreaField()
    submit = SubmitField("Submit Product")


class SearchProductForm(FlaskForm):
    productSearchOptions = SelectField('Search By',
                                       choices=[("customerID", "Customer ID"), ("oemID", "OEM ID"),
                                                ("productType", "Product Type"), ("title", "Title")])
    productSearchQuery = StringField()
    submitProductSearch = SubmitField("Search")


class Customer(db.Model):
    customerID = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String)
    title = db.Column(db.String)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    billingAddress1 = db.Column(db.String)
    billingAddress2 = db.Column(db.String)
    billingCity = db.Column(db.String)
    billingState = db.Column(db.String)
    billingZip = db.Column(db.Integer)
    billingCountry = db.Column(db.String)
    shippingAddress1 = db.Column(db.String)
    shippingAddress2 = db.Column(db.String)
    shippingCity = db.Column(db.String)
    shippingState = db.Column(db.String)
    shippingZip = db.Column(db.String)
    shippingCountry = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Customer %r>' % self.customerID


class SearchCustomerForm(FlaskForm):
    searchOption = SelectField('Search Option',
                               choices=[("firstName", "First Name"), ("lastName", "Last Name"), ("email", "Email"),
                                        ("phone", "Phone Number")])
    searchQuery = StringField()
    submit = SubmitField("Search Customer")
    removeCustomer = SubmitField("Delete")


class CreateCustomerForm(FlaskForm):
    # customerID = StringField() # Customer ID should be generated when user is created, not a user input.
    company = StringField()
    title = StringField()
    firstName = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    lastName = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    email = EmailField()
    phone = StringField()
    billingAddress1 = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    billingAddress2 = StringField()
    billingCity = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    billingState = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    billingZip = IntegerField(validators=[InputRequired()])
    billingCountry = StringField(validators=[InputRequired(), Length(min=3, max=80)])
    shippingAddress1 = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    shippingAddress2 = StringField()
    shippingCity = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    shippingState = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    shippingZip = IntegerField(validators=[InputRequired()])
    shippingCountry = StringField(validators=[InputRequired(), Length(min=3, max=80)])
    submit = SubmitField("Create Customer")


class Inventory(db.Model):
    inventoryID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer)
    providedByCustomer = db.Column(db.String)
    descriptionOfItem = db.Column(db.String)
    inventoryItem = db.Column(db.String)
    materialOfItem = db.Column(db.String)
    inventoryDateObtained = db.Column(db.DateTime)
    inventoryDateReleased = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)
    carrier = db.Column(db.String)
    manufacturerPN = db.Column(db.Integer)
    signedBy = db.Column(db.String)


class InventoryForm(FlaskForm):
    customerID = IntegerField(validators=[InputRequired()])
    providedByCustomer = StringField("Yes or No", validators=[InputRequired()])
    materialOfItem = StringField("Material", validators=[InputRequired()])
    descriptionOfItem = StringField("Description", validators=[InputRequired()])
    inventoryItem = StringField("Inventory Item", validators=[InputRequired()])
    inventoryDateObtained = DateField()
    inventoryDateReleased = DateField()
    quantity = IntegerField("0-X", validators=[InputRequired()])
    carrier = StringField("UPS", validators=[InputRequired()])
    manufacturerPN = IntegerField("12345", validators=[InputRequired()])
    signedBy = StringField("Signature", validators=[InputRequired()])
    submit = SubmitField("Submit Inventory Item")
    ID = IntegerField(validators=[InputRequired()])


class SearchInventoryForm(FlaskForm):
    inventorySearchOptions = SelectField('Search By',
                                         choices=[("inventoryID", "Inventory ID"),
                                                  ("providedByCustomer", "Provided By Customer"),
                                                  ("manufacturerPN", "Manufacturer PN"), ("signedBy", "Sign By"),
                                                  ("inventoryDateObtained", "Date Obtained")])
    inventSearchQuery = StringField()
    submitInventorySearch = SubmitField("Search Inventory")


class ShippingAccounts(db.Model):
    shippingAccountNumber = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer)
    nameOfShippingAccount = db.Column(db.String)
    carrier = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    companyID = db.Column(db.Integer)
    companyName = db.Column(db.String)
    phoneNumber = db.Column(db.Integer)
    address2 = db.Column(db.Integer)


class MultipleShippingForm(FlaskForm):
    shippingAccountNum = IntegerField(validators=[InputRequired()])
    customerID = IntegerField(validators=[InputRequired()])
    nameOfShippingAccount = StringField(validators=[InputRequired()])
    companyID = IntegerField(validators=[InputRequired()])
    carrier = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    address2 = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired()])
    phoneNumber = IntegerField(validators=[InputRequired()])
    companyName = StringField(validators=[InputRequired()])
    submit = SubmitField("Submit New Shipping Account")


class Quotes(db.Model):
    quoteID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer)
    # item = db.Column(db.String)
    prefer = db.Column(db.String)

    # quantity = db.Column(db.Integer)
    # productID = db.Column(db.Integer)
    # quotePrice = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Customer %r>' % self.customerID


class Quote_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, primary_key=True)


class Items(db.Model):
    itemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float)
    itemDesc = db.Column(db.String)
    itemName = db.Column(db.String)
    quantity = db.Column(db.Integer)


class QuoteForm(FlaskForm):
    customerID = SelectField(choices=[])
    productID = SelectField(choices=[])
    preferred = RadioField('preferred contact', choices=[('email', 'E-mail'), ('phone', 'Phone')], default='email')
    # item = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    # quantity = IntegerField(validators=[InputRequired()])
    # price = IntegerField(validators=[InputRequired()])
    submit = SubmitField("Create Quote")


class EditQuoteForm(FlaskForm):
    customerID = SelectField(choices=[])
    productID = SelectField(choices=[])
    preferred = RadioField('preferred contact', choices=[('email', 'E-mail'), ('phone', 'Phone')])
    item = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    quantity = IntegerField(validators=[InputRequired()])
    price = IntegerField(validators=[InputRequired()])
    submitEdit = SubmitField("Edit Quote")


# class EditQuoteForm(FlaskForm):
#     customerID = SelectField(choices=[])
#     productID = SelectField(choices=[])
#     preferred = RadioField('preferred contact', choices=[('email', 'E-mail'), ('phone', 'Phone')])
#     item = StringField(validators=[InputRequired(), Length(min=1, max=200)])
#     quantity = IntegerField(validators=[InputRequired()])
#     price = IntegerField(validators=[InputRequired()])
#     submitEdit = SubmitField("Edit Quote")


class SearchQuoteForm(FlaskForm):
    searchQuoteOptions = SelectField('Search Option',
                                     choices=[("id", "Quote ID"), ("customerID", "Customer ID"),
                                              ("item", "Item")])
    searchQuoteQuery = StringField()
    submitQuoteSearch = SubmitField("Search Quote")


class EditCustomerForm(FlaskForm):
    customerIDEdit = IntegerField()
    companyEdit = StringField()
    titleEdit = StringField()
    firstNameEdit = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    lastNameEdit = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    emailEdit = EmailField()
    phoneEdit = StringField()
    billingAddress1Edit = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    billingAddress2Edit = StringField()
    billingCityEdit = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    billingStateEdit = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    billingZipEdit = IntegerField(validators=[InputRequired()])
    billingCountryEdit = StringField(validators=[InputRequired(), Length(min=3, max=80)])
    shippingAddress1Edit = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    shippingAddress2Edit = StringField()
    shippingCityEdit = StringField(validators=[InputRequired(), Length(min=4, max=80)])
    shippingStateEdit = StringField(validators=[InputRequired(), Length(min=2, max=80)])
    shippingZipEdit = IntegerField(validators=[InputRequired()])
    shippingCountryEdit = StringField(validators=[InputRequired(), Length(min=3, max=80)])
    submitEdit = SubmitField("Edit Customer")


class EditProductForm(FlaskForm):
    customerIDEdit = IntegerField(validators=[InputRequired()])
    oemIDEdit = IntegerField(validators=[InputRequired()])
    productTypeEdit = StringField(validators=[InputRequired()])
    titleEdit = StringField(validators=[InputRequired()])
    productDescriptionEdit = TextAreaField()
    colorNotesEdit = TextAreaField()
    packagingNotesEdit = TextAreaField()
    productNotesEdit = TextAreaField()
    serviceNotesEdit = TextAreaField()
    insertEdit = TextAreaField()
    submitEdit = SubmitField("Edit Product")


class orders(db.Model):
    customerID = db.Column(db.Integer, primary_key = True)
    salesperson = db.Column(db.String)
    requestor = db.Column(db.String)
    customercontact = db.Column(db.String)
    reorder = db.Column(db.Boolean, default=False, nullable=False)
    factoryOrderQuantity = db.Column(db.Integer)
    cpInvoice = db.Column(db.Boolean, default=False, nullable=False)
    cpPackingSlip = db.Column(db.String)
    cpQuantity = db.Column(db.Integer)
    cpUnitPrice = db.Column(db.Integer)
    cpTotalPrice = db.Column(db.Integer)
    niName = db.Column(db.String)
    niInvoice = db.Column(db.String)
    niPackingSlip = db.Column(db.String)
    niQuantity = db.Column(db.Integer)
    niUnitPrice = db.Column(db.Integer)
    niTotalPrice = db.Column(db.Integer)
    iInvoice = db.Column(db.String)
    iPackingSlip = db.Column(db.String)
    iQuantity = db.Column(db.Integer)
    iUnitPrice = db.Column(db.Integer)
    iTotalPrice = db.Column(db.Integer)
    assemblyCha = db.Column(db.Integer)
    acUnitPrice = db.Column(db.Integer)
    acTotalPrice = db.Column(db.Integer)
    dcPrintCharge = db.Column(db.Integer)
    dcSetCharge = db.Column(db.Integer)
    numOfScreen = db.Column(db.Integer)
    nosQuantity = db.Column(db.Integer)
    nosTotalPrice = db.Column(db.Integer)
    subTotal = db.Column(db.Integer)
    taxable = db.Column(db.Boolean, default=False, nullable=False)
    taxRate = db.Column(db.Integer)
    taxMoney = db.Column(db.Integer)
    freightCharges = db.Column(db.String)
    ordPriceTotal = db.Column(db.Integer)
    iiInvoiceDate = db.Column(db.String)
    iiDatePaid = db.Column(db.Integer)
    iiNotes = db.Column(db.String)
    salesOrdDate = db.Column(db.String)
    custOrdDate = db.Column(db.String)
    custPODate = db.Column(db.String)
    custPONum = db.Column(db.String)
    creditChecked = db.Column(db.Boolean, default=False, nullable=False)
    daysTurn = db.Column(db.Integer)
    dateCodePrint = db.Column(db.Integer)
    assemBy = db.Column(db.String)
    discManBy = db.Column(db.String)
    cdrDVD = db.Column(db.String)
    custProvMat = db.Column(db.String)
    custMatETA = db.Column(db.String)
    custNotes = db.Column(db.String)
    vendorNotes = db.Column(db.String)
    orderNotes = db.Column(db.String)
    orderStatusSub = db.Column(db.Boolean, default=False, nullable=False)


class OrdersForm(FlaskForm):
    customerID = SelectField(choices=[])
    salesperson = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    requestor = IntegerField(validators=[InputRequired()])
    customercontact = IntegerField(validators=[InputRequired()])
    reorder = IntegerField(validators=[InputRequired()])
    factoryOrderQuantity = IntegerField(validators=[InputRequired()])
    cpInvoice = IntegerField(validators=[InputRequired()])
    cpPackingSlip = IntegerField(validators=[InputRequired()])
    cpQuantity = IntegerField(validators=[InputRequired()])
    cpUnitPrice = IntegerField(validators=[InputRequired()])
    cpTotalPrice = IntegerField(validators=[InputRequired()])
    niName = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    niInvoice = IntegerField(validators=[InputRequired()])
    niPackingSlip = IntegerField(validators=[InputRequired()])
    niQuantity = IntegerField(validators=[InputRequired()])
    niUnitPrice = IntegerField(validators=[InputRequired()])
    niTotalPrice = IntegerField(validators=[InputRequired()])
    iInvoice = IntegerField(validators=[InputRequired()])
    iPackingSlip = IntegerField(validators=[InputRequired()])
    iQuantity = IntegerField(validators=[InputRequired()])
    iUnitPrice = IntegerField(validators=[InputRequired()])
    iTotalPrice = IntegerField(validators=[InputRequired()])
    assemblyCha = IntegerField(validators=[InputRequired()])
    acUnitPrice = IntegerField(validators=[InputRequired()])
    acTotalPrice = IntegerField(validators=[InputRequired()])
    dcPrintCharge = IntegerField(validators=[InputRequired()])
    dcSetCharge = IntegerField(validators=[InputRequired()])
    numOfScreen = IntegerField(validators=[InputRequired()])
    nosQuantity = IntegerField(validators=[InputRequired()])
    nosTotalPrice = IntegerField(validators=[InputRequired()])
    subTotal = IntegerField(validators=[InputRequired()])
    taxable = IntegerField(validators=[InputRequired()])
    taxRate = IntegerField(validators=[InputRequired()])
    taxMoney = IntegerField(validators=[InputRequired()])
    freightCharges = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    ordPriceTotal = IntegerField(validators=[InputRequired()])
    iiInvoiceDate = DateField()
    iiDatePaid = DateField()
    iiNotes = TextAreaField()
    salesOrdDate = DateField()
    custOrdDate = DateField()
    custPODate = DateField()
    custPONum = IntegerField(validators=[InputRequired()])
    creditChecked = DateField()
    daysTurn = IntegerField(validators=[InputRequired()])
    dateCodePrint = DateField()
    assemBy = IntegerField(validators=[InputRequired()])
    discManBy = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    cdrDVD = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    custProvMat = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    custMatETA = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    custNotes = TextAreaField()
    vendorNotes = TextAreaField()
    orderNotes = TextAreaField()
    orderStatusSub = IntegerField(validators=[InputRequired()])
    submit = SubmitField("Create Order")

class EditOrderForm(FlaskForm):
    customerIDEdit = SelectField(choices=[])
    salespersonEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    requestorEdit = IntegerField(validators=[InputRequired()])
    customercontactEdit = IntegerField(validators=[InputRequired()])
    reorderEdit = IntegerField(validators=[InputRequired()])
    factoryOrderQuantityEdit = IntegerField(validators=[InputRequired()])
    cpInvoiceEdit = IntegerField(validators=[InputRequired()])
    cpPackingSlipEdit = IntegerField(validators=[InputRequired()])
    cpQuantityEdit = IntegerField(validators=[InputRequired()])
    cpUnitPriceEdit = IntegerField(validators=[InputRequired()])
    cpTotalPriceEdit = IntegerField(validators=[InputRequired()])
    niNameEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    niInvoiceEdit = IntegerField(validators=[InputRequired()])
    niPackingSlipEdit = IntegerField(validators=[InputRequired()])
    niQuantityEdit = IntegerField(validators=[InputRequired()])
    niUnitPriceEdit = IntegerField(validators=[InputRequired()])
    niTotalPriceEdit = IntegerField(validators=[InputRequired()])
    iInvoiceEdit = IntegerField(validators=[InputRequired()])
    iPackingSlipEdit = IntegerField(validators=[InputRequired()])
    iQuantityEdit = IntegerField(validators=[InputRequired()])
    iUnitPriceEdit = IntegerField(validators=[InputRequired()])
    iTotalPriceEdit = IntegerField(validators=[InputRequired()])
    assemblyChaEdit = IntegerField(validators=[InputRequired()])
    acUnitPriceEdit = IntegerField(validators=[InputRequired()])
    acTotalPriceEdit = IntegerField(validators=[InputRequired()])
    dcPrintChargeEdit = IntegerField(validators=[InputRequired()])
    dcSetChargeEdit = IntegerField(validators=[InputRequired()])
    numOfScreenEdit = IntegerField(validators=[InputRequired()])
    nosQuantityEdit = IntegerField(validators=[InputRequired()])
    nosTotalPriceEdit = IntegerField(validators=[InputRequired()])
    subTotalEdit = IntegerField(validators=[InputRequired()])
    taxableEdit = IntegerField(validators=[InputRequired()])
    taxRateEdit = IntegerField(validators=[InputRequired()])
    taxMoneyEdit = IntegerField(validators=[InputRequired()])
    freightChargesEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    ordPriceTotalEdit = IntegerField(validators=[InputRequired()])
    iiInvoiceDateEdit = DateField()
    iiDatePaidEdit = DateField()
    iiNotesEdit = TextAreaField()
    salesOrdDateEdit = DateField()
    custOrdDateEdit = DateField()
    custPODateEdit = DateField()
    custPONumEdit = IntegerField(validators=[InputRequired()])
    creditCheckedEdit = DateField()
    daysTurnEdit = IntegerField(validators=[InputRequired()])
    dateCodePrintEdit = DateField()
    assemByEdit = IntegerField(validators=[InputRequired()])
    discManByEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    cdrDVDEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    custProvMatEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    custMatETAEdit = StringField(validators=[InputRequired(), Length(min=1, max=200)])
    custNotesEdit = TextAreaField()
    vendorNotesEdit = TextAreaField()
    orderNotesEdit = TextAreaField()
    orderStatusSubEdit = IntegerField(validators=[InputRequired()])
    submitEdit = SubmitField("Edit Order")

class SearchOrderForm(FlaskForm):
    searchQuoteOptions = SelectField('Search Option',
                                     choices=[("id", "Customer ID")])
    searchOrderQuery = StringField()
    submitOrderSearch = SubmitField("Search Orders")


@app.route("/")
@login_required
def home_page():
    return render_template("dashboard.html", user=current_user.as_dict())


@app.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html", user=current_user.as_dict())


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():  # check form on submit
        # fetch user from email
        user = Users.query.filter_by(email=login_form.email.data).first()
        # if user with email found
        if user:
            # check password
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                # send to dashboard page
                return redirect(url_for('dashboard_page'))
            else:
                error = 'Invalid login'
        else:
            error = 'Invalid User'

    # return login page with error
    return render_template("login.html", form=login_form, error=error)


@app.route("/register", methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    error = None
    if register_form.validate_on_submit():  # check form on submit
        # fetch user from email
        user = Users.query.filter_by(email=register_form.email.data).first()
        # if user with email found
        if user:
            error = 'Email Exists'
            return render_template("register.html", form=register_form, error=error)
        else:
            # hash password
            hashed_pw = bcrypt.generate_password_hash(register_form.password.data)

            # New user object
            new_user = Users()
            # populate user object with data
            new_user.email = register_form.email.data
            new_user.password = hashed_pw
            new_user.userType = "customer"

            # add/commit to database
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('dashboard_page'))

    # return login page with error
    return render_template("register.html", form=register_form, error=error)


# PDF Invoice Generator
@app.route('/test')
@login_required
def pdf_template():
    # rendered = render_template('invoiced.html', name=name, location=location)
    # # pdf = pdfkit.from_string(rendered, False)
    # pdf = pdfkit.from_string(rendered, False,  configuration=pdfkit_config)
    #
    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'

    result = db.session.execute(
        'SELECT q.quoteID, i.itemName, i.itemDesc, i.price FROM quotes q INNER JOIN quote_items qi ON qi.id = q.quoteID INNER JOIN items i ON i.itemID = qi.itemID WHERE quoteID = 36').all()

    return f'{result}'


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    error = None
    message = None
    create_user_form = CreateUserForm()
    search_user_form = SearchUserForm()
    users = Users.query.all()

    if create_user_form.validate_on_submit():
        if create_user_form.searchQuery.data:
            print("Searching for user")
            user_search_result = Users.query.filter_by(email=create_user_form.searchQuery.data).first()
            return render_template("admin.html", error=error, create_user_form=create_user_form,
                                   user_search_results=user_search_result,
                                   search_user_form=search_user_form,
                                   user=current_user.as_dict(),
                                   message=message)
        else:
            user = Users.query.filter_by(email=create_user_form.email.data).first()
            # if user with email found
            if user:
                error = 'Email Exists'
                return render_template("admin.html", error=error, create_user_form=create_user_form,
                                       search_user_form=search_user_form, user_search_results=users,
                                       user=current_user.as_dict(),
                                       message=message)
            else:
                # hash password
                hashed_pw = bcrypt.generate_password_hash(create_user_form.password.data)

                # New user object
                new_user = Users()
                # populate user object with data
                new_user.email = create_user_form.email.data
                new_user.password = hashed_pw
                new_user.userType = create_user_form.userType.data

                # add/commit to database
                db.session.add(new_user)
                db.session.commit()
                message = f'New user {create_user_form.email.data} added ({create_user_form.userType.data})'
                return render_template("admin.html", error=error, create_user_form=create_user_form,
                                       search_user_form=search_user_form, user_search_results=users,
                                       user=current_user.as_dict(),
                                       message=message)

    if search_user_form.validate_on_submit():
        if search_user_form.searchQuery.data:
            print("Searching for user")
            user_search_result = Users.query.filter_by(email=search_user_form.searchQuery.data).all()
            return render_template("admin.html", error=error, create_user_form=create_user_form,
                                   user_search_results=user_search_result,
                                   search_user_form=search_user_form,
                                   user=current_user.as_dict(),
                                   message=message)

    # return login page with error
    return render_template("admin.html", error=error, create_user_form=create_user_form,
                           search_user_form=search_user_form, user=current_user.as_dict(), user_search_results=users)


@app.route("/deleteuser/<user_id>", methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    user = Users.query.filter_by(id=user_id)
    _user = user.first().as_dict().copy()
    if user:
        user.delete()
        db.session.commit()

        flash(f'Deleted user {_user["email"]} ({_user["id"]})')

    return redirect(url_for('admin'))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/fillableform", methods=['GET'])
def fillableform_page():
    return render_template('fillableform.html')


@app.route("/dash-track", methods=['GET'])
def dashtrack_page():
    return render_template('dash-track.html')


@app.route("/createquote", methods=['POST', 'GET'])
@login_required
def quotes_page():
    error = None
    message = None
    new_quote_form = QuoteForm()
    query_quote_form = SearchQuoteForm()
    edit_quote_form = EditQuoteForm()
    customers = Customer.query.all()
    products = Products.query.all()

    new_quote_form.customerID.choices = [(c.customerID, f"{c.customerID} - {c.firstName.title()} {c.lastName.title()}")
                                         for c in customers]
    new_quote_form.productID.choices = [(p.oemID, f"{p.productType.title()}") for p in products]

    if new_quote_form.validate_on_submit():
        print("Creating new quote for", new_quote_form.customerID.data)
        print("prioduct id", request.form.getlist('productID'))
        print(request.form.getlist('itemDesc[]'))
        new_quote = Quotes()

        new_quote.customerID = new_quote_form.customerID.data
        # new_quote.item = new_quote_form.item.data.lower()
        new_quote.prefer = new_quote_form.preferred.data.lower()
        # new_quote.quantity = new_quote_form.quantity.data
        new_quote.productID = new_quote_form.productID.data
        # new_quote.quotePrice = new_quote_form.price.data

        # add/commit to database
        db.session.add(new_quote)
        db.session.commit()

        for i, p in enumerate(request.form.getlist('productID')):
            new_item = Items()
            new_quote_items = Quote_items()
            print("item name", Products.query.filter_by(oemID=p).first().productType,
                  request.form.getlist('quantities[]')[i])
            new_item.itemName = Products.query.filter_by(oemID=p).first().productType
            new_item.price = request.form.getlist('prices[]')[i]
            new_item.itemDesc = request.form.getlist('itemDesc[]')[i]
            new_item.quantity = request.form.getlist('quantities[]')[i]

            db.session.add(new_item)
            db.session.commit()
            print(new_quote.quoteID, new_item.itemID)
            new_quote_items.id = new_quote.quoteID
            new_quote_items.itemID = new_item.itemID

            db.session.add(new_quote_items)
            db.session.commit()

        # # add/commit to database
        # db.session.add(new_quote)
        # db.session.commit()

        message = f'New quote # {new_quote.quoteID} created ({len(request.form.getlist("productID"))} items)'

        return render_template('createquote.html', new_quote_form=new_quote_form,
                               query_quote_form=query_quote_form,
                               edit_quote_form=edit_quote_form,
                               customers=customers,
                               message=message,
                               user=current_user.as_dict())
    else:
        print("New quote Form is not valid", new_quote_form.errors)
        error = "Form invalid"

    if query_quote_form.validate_on_submit():
        searchQuoteOption = query_quote_form.searchQuoteOptions.data

        if searchQuoteOption == "id":
            # search_result = Quotes.query.filter_by(quoteID=query_quote_form.searchQuoteQuery.data.lower()).all()
            search_result = Quotes.query.filter_by(quoteID=query_quote_form.searchQuoteQuery.data.lower()).all()
            sr = []
            for s in search_result:
                result = db.session.execute(
                    f'SELECT q.quoteID, i.itemName, i.itemDesc, i.price, i.quantity FROM quotes q INNER JOIN quote_items qi ON qi.id = q.quoteID INNER JOIN items i ON i.itemID = qi.itemID WHERE quoteID = {query_quote_form.searchQuoteQuery.data}').all()
                print(len(result), "items found")
                _s = s.as_dict().copy()
                _s['item'] = len(result)
                sr.append(_s)

            return render_template('createquote.html', new_quote_form=new_quote_form,
                                   query_quote_form=query_quote_form,
                                   edit_quote_form=edit_quote_form,
                                   quote_search_results=sr,
                                   user=current_user.as_dict())

        if searchQuoteOption == "customerID":
            search_result = Quotes.query.filter_by(customerID=query_quote_form.searchQuoteQuery.data.lower()).all()

            sr = []

            for s in search_result:
                result = db.session.execute(
                    f'SELECT q.quoteID, i.itemName, i.itemDesc, i.price, i.quantity FROM quotes q INNER JOIN quote_items qi ON qi.id = q.quoteID INNER JOIN items i ON i.itemID = qi.itemID WHERE quoteID = {s.quoteID}').all()
                print(len(result), "items found")
                _s = s.as_dict().copy()
                _s['item'] = len(result)
                sr.append(_s)


            return render_template('createquote.html', new_quote_form=new_quote_form,
                                   query_quote_form=query_quote_form,
                                   edit_quote_form=edit_quote_form,
                                   quote_search_results=sr,
                                   user=current_user.as_dict())

    else:
        print("search quote form not valid", query_quote_form.errors)

    return render_template('createquote.html', new_quote_form=new_quote_form,
                           customers=customers,
                           query_quote_form=query_quote_form,
                           edit_quote_form=edit_quote_form,
                           user=current_user.as_dict())


@app.route("/createquote/pdf", methods=['POST'])
@login_required
def quote_pdf():
    print("pdf args:", request.get_json())
    args = request.get_json()

    result = db.session.execute(
        f'SELECT q.quoteID, i.itemName, i.itemDesc, i.price, i.quantity FROM quotes q INNER JOIN quote_items qi ON qi.id = q.quoteID INNER JOIN items i ON i.itemID = qi.itemID WHERE quoteID = {args["quoteID"]}').all()
    print(len(result), "items found")
    sr = []
    for i in result:
        sr.append({
            "itemName": i['itemName'],
            "itemDesc": i['itemDesc'],
            "price": i['price'],
            "quantity": i['quantity'],
            "priceSum:": int(i['quantity']) * float(i['price'])
        })

    args['quoteItems'] = sr

    customer = Customer.query.filter_by(customerID=args['customerID']).first().as_dict()
    args['name'] = f'{customer["firstName"].title()} {customer["lastName"].title()}'
    args['customer'] = customer
    args['date'] = datetime.today().strftime('%m/%d/%Y')
    args['total'] = 0
    for i in result:
        for j in range(i['quantity']):
            args['total'] += i.price

    print("generating pdf for", args)
    rendered = render_template('Invoice.html', data=args)
    pdf = pdfkit.from_string(rendered, False, configuration=pdfkit_config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'

    return response


@app.route("/products", methods=['POST', 'GET'])
@login_required
def products():
    error = None
    message = None
    new_product_form = ProductForm()
    query_product_form = SearchProductForm()
    edit_product_form = EditProductForm()

    customers = Customer.query.all()

    new_product_form.customerID.choices = [
        (c.customerID, f"{c.customerID} - {c.firstName.title()} {c.lastName.title()}") for c in customers]

    if new_product_form.validate_on_submit():
        print("Adding a new product")
        new_product = Products()

        new_product.customerID = new_product_form.customerID.data
        new_product.productType = new_product_form.productType.data.lower()
        new_product.title = new_product_form.title.data.lower()
        new_product.productDescription = new_product_form.productDescription.data.lower()
        new_product.colorNotes = new_product_form.colorNotes.data.lower()
        new_product.packagingNotes = new_product_form.packagingNotes.data.lower()
        new_product.productNotes = new_product_form.productNotes.data.lower()
        new_product.serviceNotes = new_product_form.serviceNotes.data.lower()
        new_product.insert = new_product_form.insert.data.lower()

        db.session.add(new_product)
        db.session.commit()

        message = f'{new_product_form.title.data} added'
        print("submitted product form", new_product_form.title.data)
        return render_template('products.html',
                               new_product_form=new_product_form,
                               query_product_form=query_product_form,
                               edit_product_form=edit_product_form,
                               error=error,
                               message=message,
                               user=current_user.as_dict())
    elif new_product_form.errors:
        print("New product Form is not valid", new_product_form.errors)
        error = "Form invalid"

    if query_product_form.validate_on_submit():
        productSearchOption = query_product_form.productSearchOptions.data

        if productSearchOption == "customerID":
            productSearchResult = Products.query.filter_by(customerID=query_product_form.productSearchQuery.data)
            return render_template('products.html', new_product_form=new_product_form,
                                   query_product_form=query_product_form,
                                   edit_product_form=edit_product_form,
                                   productSearchResults=productSearchResult.all(),
                                   user=current_user.as_dict())

        if productSearchOption == "oemID":
            productSearchResult = Products.query.filter_by(oemID=query_product_form.productSearchQuery.data)
            return render_template('products.html', new_product_form=new_product_form,
                                   query_product_form=query_product_form,
                                   edit_product_form=edit_product_form,
                                   productSearchResults=productSearchResult.all(),
                                   user=current_user.as_dict())

        if productSearchOption == "productType":
            productSearchResult = Products.query.filter_by(
                productType=query_product_form.productSearchQuery.data.lower())
            return render_template('products.html', new_product_form=new_product_form,
                                   query_product_form=query_product_form,
                                   edit_product_form=edit_product_form,
                                   productSearchResults=productSearchResult.all(),
                                   user=current_user.as_dict())

        if productSearchOption == "title":
            productSearchResult = Products.query.filter_by(title=query_product_form.productSearchQuery.data.lower())
            return render_template('products.html', new_product_form=new_product_form,
                                   query_product_form=query_product_form,
                                   edit_product_form=edit_product_form,
                                   productSearchResults=productSearchResult.all(),
                                   user=current_user.as_dict())

    elif query_product_form.errors:
        print("Search product form not valid ", query_product_form.errors)

    if edit_product_form.validate_on_submit():
        target_product = Products.query.filter_by(oemID=edit_product_form.oemIDEdit.data).first()
        print("Editing", target_product, edit_product_form.customerIDEdit.data)
        target_product.productType = edit_product_form.productTypeEdit.data.lower()
        target_product.title = edit_product_form.titleEdit.data.lower()
        target_product.productDescription = edit_product_form.productDescriptionEdit.data.lower()
        target_product.colorNotes = edit_product_form.colorNotesEdit.data.lower()
        target_product.packagingNotes = edit_product_form.packagingNotesEdit.data
        target_product.productDescription = edit_product_form.productDescriptionEdit.data.lower()
        target_product.serviceNotes = edit_product_form.serviceNotesEdit.data.lower()
        target_product.insert = edit_product_form.insertEdit.data.lower()

        # add/commit to database
        db.session.add(target_product)
        db.session.commit()
        message = f'Product {target_product.title.title()} (OEM ID:{edit_product_form.oemIDEdit.data}) Updated'
        return render_template('products.html', new_product_form=new_product_form,
                               query_product_form=query_product_form,
                               edit_product_form=edit_product_form,
                               message=message,
                               user=current_user.as_dict())

    elif edit_product_form.errors:
        print("edit customer form not valid", edit_product_form.errors)

    return render_template('products.html',
                           new_product_form=new_product_form,
                           query_product_form=query_product_form,
                           edit_product_form=edit_product_form,
                           user=current_user.as_dict())


@app.route("/deleteproduct/<oem_id>", methods=['POST', 'GET'])
@login_required
def delete_product(oem_id):
    product = Products.query.filter_by(oemID=oem_id)
    _product = product.first().as_dict().copy()
    if product:
        product.delete()
        db.session.commit()

        flash(f'Deleted product {_product["title"]} (OEM ID: {_product["oemID"]})')

    return redirect(url_for('products'))


@app.route("/customers", methods=['POST', 'GET'])
@app.route("/customers/<cid>", methods=['POST', 'GET'])
@app.route("/editcustomer/<cid>", methods=['POST', 'GET'])
@login_required
def customers(cid=None):
    error = None
    message = None
    new_customer_form = CreateCustomerForm()
    query_customer_form = SearchCustomerForm()
    edit_customer_form = EditCustomerForm()

    if cid:
        print("editing", cid)

    if new_customer_form.validate_on_submit() and new_customer_form.firstName.data:
        print("Adding a new customer")
        # create a new customer
        new_customer = Customer()

        new_customer.title = new_customer_form.title.data.lower()
        new_customer.company = new_customer_form.company.data.lower()
        new_customer.firstName = new_customer_form.firstName.data.lower()
        new_customer.lastName = new_customer_form.lastName.data.lower()
        new_customer.email = new_customer_form.email.data.lower()
        new_customer.phone = new_customer_form.phone.data
        new_customer.billingAddress1 = new_customer_form.billingAddress1.data.lower()
        new_customer.billingAddress2 = new_customer_form.billingAddress2.data.lower()
        new_customer.billingCity = new_customer_form.billingCity.data.lower()
        new_customer.billingState = new_customer_form.billingState.data.lower()
        new_customer.billingZip = new_customer_form.billingZip.data
        new_customer.billingCountry = new_customer_form.billingCountry.data.lower()
        new_customer.shippingAddress1 = new_customer_form.shippingAddress1.data.lower()
        new_customer.shippingAddress2 = new_customer_form.shippingAddress2.data.lower()
        new_customer.shippingCity = new_customer_form.shippingCity.data.lower()
        new_customer.shippingState = new_customer_form.shippingState.data.lower()
        new_customer.shippingZip = new_customer_form.shippingZip.data
        new_customer.shippingCountry = new_customer_form.shippingCountry.data.lower()

        # add/commit to database
        db.session.add(new_customer)
        db.session.commit()

        message = f'New customer {new_customer_form.firstName.data.title()} (ID: {new_customer.customerID}) added'

        return render_template('createCustomer.html', new_customer_form=new_customer_form,
                               query_customer_form=query_customer_form,
                               edit_customer_form=edit_customer_form,
                               message=message,
                               user=current_user.as_dict())
    elif new_customer_form.errors:
        print("New customer Form is not valid", new_customer_form.errors)
        error = "Form invalid"

    if query_customer_form.validate_on_submit():
        searchOption = query_customer_form.searchOption.data

        if searchOption == "firstName":
            search_result = Customer.query.filter_by(firstName=query_customer_form.searchQuery.data.lower())
            # print(search_result.all())
            return render_template('createCustomer.html', new_customer_form=new_customer_form,
                                   query_customer_form=query_customer_form,
                                   edit_customer_form=edit_customer_form,
                                   customer_search_results=search_result.all(),
                                   user=current_user.as_dict())

        if searchOption == "lastName":
            search_result = Customer.query.filter_by(lastName=query_customer_form.searchQuery.data.lower())
            # print(search_result.all())
            return render_template('createCustomer.html', new_customer_form=new_customer_form,
                                   query_customer_form=query_customer_form,
                                   edit_customer_form=edit_customer_form,
                                   customer_search_results=search_result.all(),
                                   user=current_user.as_dict())

        if searchOption == "email":
            search_result = Customer.query.filter_by(email=query_customer_form.searchQuery.data.lower())
            # print(search_result.all())
            return render_template('createCustomer.html', new_customer_form=new_customer_form,
                                   query_customer_form=query_customer_form,
                                   edit_customer_form=edit_customer_form,
                                   customer_search_results=search_result.all(),
                                   user=current_user.as_dict())

        if searchOption == "phone":
            search_result = Customer.query.filter_by(phone=query_customer_form.searchQuery.data)
            # print(search_result.all())
            return render_template('createCustomer.html', new_customer_form=new_customer_form,
                                   query_customer_form=query_customer_form,
                                   edit_customer_form=edit_customer_form,
                                   customer_search_results=search_result.all(),
                                   user=current_user.as_dict())
    elif query_customer_form.errors:
        print("search customer form not valid ", query_customer_form.errors)

    if edit_customer_form.validate_on_submit():
        target_customer = Customer.query.filter_by(customerID=edit_customer_form.customerIDEdit.data).first()
        print("Editing", target_customer, edit_customer_form.firstNameEdit.data.lower())
        target_customer.title = edit_customer_form.titleEdit.data.lower()
        target_customer.company = edit_customer_form.companyEdit.data.lower()
        target_customer.firstName = edit_customer_form.firstNameEdit.data.lower()
        target_customer.lastName = edit_customer_form.lastNameEdit.data.lower()
        target_customer.email = edit_customer_form.emailEdit.data.lower()
        target_customer.phone = edit_customer_form.phoneEdit.data
        target_customer.billingAddress1 = edit_customer_form.billingAddress1Edit.data.lower()
        target_customer.billingAddress2 = edit_customer_form.billingAddress2Edit.data.lower()
        target_customer.billingCity = edit_customer_form.billingCityEdit.data.lower()
        target_customer.billingState = edit_customer_form.billingStateEdit.data.lower()
        target_customer.billingZip = edit_customer_form.billingZipEdit.data
        target_customer.billingCountry = edit_customer_form.billingCountryEdit.data.lower()
        target_customer.shippingAddress1 = edit_customer_form.shippingAddress1Edit.data.lower()
        target_customer.shippingAddress2 = edit_customer_form.shippingAddress2Edit.data.lower()
        target_customer.shippingCity = edit_customer_form.shippingCityEdit.data.lower()
        target_customer.shippingState = edit_customer_form.shippingStateEdit.data.lower()
        target_customer.shippingZip = edit_customer_form.shippingZipEdit.data
        target_customer.shippingCountry = edit_customer_form.shippingCountryEdit.data.lower()

        # add/commit to database
        db.session.add(target_customer)
        db.session.commit()
        message = f'Customer {target_customer.firstName.title()} {target_customer.lastName.title()} (CID:{edit_customer_form.customerIDEdit.data}) Updated'
        return render_template('createCustomer.html', new_customer_form=new_customer_form,
                               query_customer_form=query_customer_form,
                               edit_customer_form=edit_customer_form,
                               message=message,
                               user=current_user.as_dict())

    elif edit_customer_form.errors:
        print("edit customer form not valid", edit_customer_form.errors)

    return render_template('createCustomer.html',
                           new_customer_form=new_customer_form,
                           query_customer_form=query_customer_form,
                           edit_customer_form=edit_customer_form,
                           user=current_user.as_dict())


@app.route("/deletecustomer/<customer_id>", methods=['POST', 'GET'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.filter_by(customerID=customer_id)
    _customer = customer.first().as_dict().copy()
    if customer:
        customer.delete()
        db.session.commit()

        flash(f'Deleted user {_customer["firstName"]} {_customer["lastName"]} (User ID: {_customer["customerID"]})')

    return redirect(url_for('customers'))


@app.route("/deletequote/<quote_id>", methods=['POST', 'GET'])
@login_required
def delete_quote(quote_id):
    quote = Quotes.query.filter_by(quoteID=quote_id)
    _quote = quote.first().as_dict().copy()
    if quote:
        quote.delete()
        db.session.commit()

        flash(f'Deleted quote: {_quote["quoteID"]}')

    return redirect(url_for('quotes_page'))

@app.route("/createorder", methods=['POST', 'GET'])
@app.route("/orders/<cid>", methods=['POST', 'GET'])
@app.route("/editorder/<cid>", methods=['POST', 'GET'])
@login_required
def orders_page(cid = None):
    error = None
    message = None
    new_order_form = OrdersForm()
    query_order_form = SearchOrderForm()
    edit_order_form = EditOrderForm()
    customers = Customer.query.all()

    if cid:
        print("editing", cid)

    new_order_form.customerID.choices = [(c.customerID, f"{c.customerID} - {c.firstName.title()} {c.lastName.title()}") for c in customers]

    if new_order_form.validate_on_submit():
        print("Creating new order for", new_order_form.customerID.data)
        new_order = Orders()

        new_order.customerID = new_order_form.customerID.data

        # add/commit to database
        db.session.add(new_order)
        db.session.commit()

        message = f'New order # {new_order.orderID} created'

        return render_template('salesorders.html', new_order_form=new_order_form,
                               query_order_form=query_order_form,
                               edit_order_form=edit_order_form,
                               customers=customers,
                               message=message,
                               user=current_user.as_dict())
    else:
        print("New order Form is not valid", new_order_form.errors)
        error = "Form invalid"

    if query_order_form.validate_on_submit():
        searchOrderOption = query_order_form.searchOrderOptions.data

        if searchOrderOption == "id":
            search_result = orders.query.filter_by(orderID=query_order_form.searchOrderQuery.data.lower())
            # print(search_result.all())
            return render_template('salesorders.html', new_order_form=new_order_form,
                                   query_order_form=query_order_form,
                                   edit_order_form=edit_order_form,
                                   order_search_results=search_result.all(),
                                   user=current_user.as_dict())

    else:
        print("search order form not valid", query_order_form.errors)

    if edit_order_form.validate_on_submit():
        target_edit = orders.query.filter_by(customerID=edit_order_form.customerIDEdit.data).first()
        print("Editing", target_edit, edit_order_form.customerIDEdit.data.lower())
        target_edit.customerID = edit_order_form.customerIDEdit.data
        target_edit.salesperson = edit_order_form.salespersonEdit.data.lower()
        target_edit.requestor = edit_order_form.requestorEdit.data.lower()
        target_edit.customercontact = edit_order_form.customercontactEdit.data.lower()
        target_edit.reorder = edit_order_form.reorderEdit.data.lower()
        target_edit.factoryOrderQuantity = edit_order_form.factoryOrderQuantityEdit.data
        target_edit.cpInvoice = edit_order_form.cpInvoiceEdit.data.lower()
        target_edit.cpPackingSlip = edit_order_form.cpPackingSlipEdit.data.lower()
        target_edit.cpQuantity = edit_order_form.cpQuantityEdit.data
        target_edit.cpUnitPrice = edit_order_form.cpUnitPriceEdit.data
        target_edit.cpTotalPrice = edit_order_form.cpTotalPriceEdit.data
        target_edit.niName = edit_order_form.niNameEdit.data.lower()
        target_edit.niInvoice = edit_order_form.niInvoiceEdit.data.lower()
        target_edit.niPackingSlip = edit_order_form.niPackingSlipEdit.data.lower()
        target_edit.niQuantity = edit_order_form.niQuantityEdit.data
        target_edit.niUnitPrice = edit_order_form.niUnitPriceEdit.data
        target_edit.niTotalPrice = edit_order_form.niTotalPriceEdit.data
        target_edit.iInvoice = edit_order_form.iInvoiceEdit.data.lower()
        target_edit.iPackingSlip = edit_order_form.iPackingSlipEdit.data.lower()
        target_edit.iQuantity = edit_order_form.iQuantityEdit.data
        target_edit.iUnitPrice = edit_order_form.iUnitPriceEdit.data
        target_edit.iTotalPrice = edit_order_form.iTotalPriceEdit.data
        target_edit.assemblyCha = edit_order_form.assemblyChaEdit.data.lower()
        target_edit.acUnitPrice = edit_order_form.acUnitPriceEdit.data
        target_edit.acTotalPrice = edit_order_form.acTotalPriceEdit.data
        target_edit.dcPrintCharge = edit_order_form.dcPrintChargeEdit.data.lower()
        target_edit.dcSetCharge = edit_order_form.dcSetChargeEdit.data.lower()
        target_edit.numOfScreen = edit_order_form.numOfScreenEdit.data
        target_edit.nosQuantity = edit_order_form.nosQuantityEdit.data
        target_edit.nosTotalPrice = edit_order_form.nosTotalPriceEdit.data
        target_edit.subTotal = edit_order_form.subTotalEdit.data.lower()
        target_edit.taxable = edit_order_form.taxableEdit.data.lower()
        target_edit.taxRate = edit_order_form.taxRateEdit.data.lower()
        target_edit.taxMoney = edit_order_form.taxMoneyEdit.data.lower()
        target_edit.freightCharges = edit_order_form.freightChargesEdit.data.lower()
        target_edit.ordPriceTotal = edit_order_form.ordPriceTotalEdit.data.lower()
        target_edit.iiInvoiceDate = edit_order_form.iiInvoiceDateEdit.data.lower()
        target_edit.iiDatePaid = edit_order_form.iiDatePaidEdit.data.lower()
        target_edit.iiNotes = edit_order_form.iiNotesEdit.data.lower()
        target_edit.salesOrdDate = edit_order_form.salesOrdDateEdit.data.lower()
        target_edit.custOrdDate = edit_order_form.custOrdDateEdit.data.lower()
        target_edit.custPODate = edit_order_form.custPODateEdit.data.lower()
        target_edit.custPONum = edit_order_form.custPONumEdit.data.lower()
        target_edit.creditChecked = edit_order_form.creditCheckedEdit.data.lower()
        target_edit.daysTurn = edit_order_form.daysTurnEdit.data.lower()
        target_edit.dateCodePrint = edit_order_form.dateCodePrintEdit.data.lower()
        target_edit.assemBy = edit_order_form.assemByEdit.data.lower()
        target_edit.discManBy = edit_order_form.discManByEdit.data.lower()
        target_edit.cdrDVD = edit_order_form.cdrDVDEdit.data.lower()
        target_edit.custProvMat = edit_order_form.custProvMatEdit.data.lower()
        target_edit.custMatETA = edit_order_form.custMatETAEdit.data.lower()
        target_edit.custNotes = edit_order_form.custNotesEdit.data.lower()
        target_edit.vendorNotes = edit_order_form.vendorNotesEdit.data.lower()
        target_edit.orderNotes = edit_order_form.orderNotesEdit.data.lower()
        target_edit.orderStatusSub = edit_order_form.orderStatusSubEdit.data.lower()
        target_edit.submitEdit = edit_order_form.submitEdit.data.lower()



        # add/commit to database
        db.session.add(target_edit)
        db.session.commit()
        return render_template('salesorders.html', new_order_form=new_order_form,
                               query_order_form=query_order_form,
                               edit_order_form=edit_order_form,
                               message=message,
                               user=current_user.as_dict())

    elif edit_order_form.errors:
        print("edit order form not valid", edit_order_form.errors)


    return render_template('salesorders.html', new_order_form=new_order_form,
                           customers=customers,
                           query_order_form=query_order_form,
                           edit_order_form=edit_order_form,
                           user=current_user.as_dict())

@app.route("/createorder/pdf", methods=['POST'])
@login_required
def order_pdf():
    print("pdf args:", request.get_json())
    args = request.get_json()
    rendered = render_template('salesorders.html', name=args['name'], location=args['price'])
    # pdf = pdfkit.from_string(rendered, False)
    pdf = pdfkit.from_string(rendered, False, configuration=pdfkit_config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=.JobOrderpdf'

    return response

@app.route("/deleteorder/<order_id>", methods=['POST', 'GET'])
@login_required
def delete_order(order_id):
    order = Orders.query.filter_by(orderID=order_id)
    _order = order.first().as_dict().copy()
    if order:
        order.delete()
        db.session.commit()

        flash(f'Deleted order: {_order["orderID"]}')

    return redirect(url_for('orders_page'))




@app.route("/inventory", methods=['POST', 'GET'])
@login_required
def inventorySystem():
    error = None
    message = None
    new_inventorySystem_form = InventoryForm()
    query_SearchInventory_form = SearchInventoryForm()

    if new_inventorySystem_form.validate_on_submit():
        print("Adding a new Inventory Item")
        # create a new inventoryItem
        new_inventoryItems = Inventory()

        new_inventoryItems.inventoryID = new_inventorySystem_form.ID.data
        new_inventoryItems.inventoryItem = new_inventorySystem_form.inventoryItem.data.lower()
        new_inventoryItems.providedByCustomer = new_inventorySystem_form.providedByCustomer.data.lower()
        new_inventoryItems.customerID = new_inventorySystem_form.customerID.data
        new_inventoryItems.descriptionOfItem = new_inventorySystem_form.descriptionOfItem.data.lower()
        new_inventoryItems.materialOfItem = new_inventorySystem_form.materialOfItem.data.lower()
        new_inventoryItems.inventoryDateObtained = new_inventorySystem_form.inventoryDateObtained.data
        new_inventoryItems.inventoryDateReleased = new_inventorySystem_form.inventoryDateReleased.data
        new_inventoryItems.quantity = new_inventorySystem_form.quantity.data
        new_inventoryItems.carrier = new_inventorySystem_form.inventoryDateReleased.data.lower()
        new_inventoryItems.manufacturerPN = new_inventorySystem_form.manufacturerPN.data
        new_inventoryItems.signedBy = new_inventorySystem_form.signedBy.data.lower()

        # add/commit to database
        db.session.add(new_inventoryItems)
        db.session.commit()

        message = f'New inventoryItem {new_inventorySystem_form.inventoryItem.data} added'

        return render_template('inventorySystem.html', new_inventorySystem_form=new_inventorySystem_form,
                               query_SearchInventory_form=query_SearchInventory_form,
                               message=message,
                               user=current_user.as_dict())
    else:
        print("New inventory Form is not valid", new_inventorySystem_form.errors)
        error = "Form invalid"

    if query_SearchInventory_form.validate_on_submit():
        inventorySearchOptions = query_SearchInventory_form.inventorySearchOptions.data

        if inventorySearchOptions == "inventoryID":
            search_result = Inventory.query.filter_by(inventoryID=query_SearchInventory_form.inventSearchQuery.data)
            # print(inventorysearchresult.all())
            return render_template('inventorySystem.html', new_inventorySystem_form=new_inventorySystem_form,
                                   query_SearchInventory_form=query_SearchInventory_form,
                                   inventorysearchresult=search_result.all(),
                                   user=current_user.as_dict())

        if inventorySearchOptions == "inventoryItem":
            search_result = Inventory.query.filter_by(
                inventoryItem=query_SearchInventory_form.inventSearchQuery.data.lower())
            # print(inventorysearchresult.all())
            return render_template('inventorySystem.html', new_inventorySystem_form=new_inventorySystem_form,
                                   query_SearchInventory_form=query_SearchInventory_form,
                                   inventorysearchresult=search_result.all(),
                                   user=current_user.as_dict())

        if inventorySearchOptions == "customerID":
            search_result = Inventory.query.filter_by(
                customerID=query_SearchInventory_form.inventSearchQuery.data.lower())
            # print(inventorysearchresult.all())
            return render_template('inventorySystem.html', new_inventorySystem_form=new_inventorySystem_form,
                                   query_SearchInventory_form=query_SearchInventory_form,
                                   inventorysearchresult=search_result.all(),
                                   user=current_user.as_dict())

        if inventorySearchOptions == "signedBy":
            search_result = Inventory.query.filter_by(
                signedBy=query_SearchInventory_form.inventSearchQuery.data.lower())
            # print(inventorysearchresult.all())
            return render_template('inventorySystem.html', new_inventorySystem_form=new_inventorySystem_form,
                                   query_SearchInventory_form=query_SearchInventory_form,
                                   inventorysearchresult=search_result.all(),
                                   user=current_user.as_dict())

    elif query_SearchInventory_form:
        print("search inventory form not valid", query_SearchInventory_form.errors)

    return render_template('inventorySystem.html', new_inventorySystem_form=new_inventorySystem_form,
                           query_SearchInventory_form=query_SearchInventory_form,
                           user=current_user.as_dict())


@app.route("/MultipleShippingAccs", methods=['POST', 'GET'])
@login_required
def add_Accounts():
    error = None
    message = None
    new_ship_acc_form = MultipleShippingForm()

    if new_ship_acc_form.validate_on_submit():
        print("Adding a new Shipping Account")
        new_shippingAcc = ShippingAccounts()

        new_shippingAcc.nameOfShippingAccountNum = new_shippingAcc.nameOfShippingAccountNum.data.lower()
        new_shippingAcc.nameOfShippingAccount = new_shippingAcc.nameOfShippingAccount.data.lower()
        new_shippingAcc.customerID = new_shippingAcc.customerID.data
        new_shippingAcc.companyID = new_shippingAcc.companyID.data
        new_shippingAcc.carrier = new_shippingAcc.carrier.data.lower()
        new_shippingAcc.email = new_shippingAcc.email.data.lower()
        new_shippingAcc.address = new_shippingAcc.address.data.lower()
        new_shippingAcc.address2 = new_shippingAcc.address.data.lower()
        new_shippingAcc.companyName = new_shippingAcc.companyName.data.lower()
        new_shippingAcc.phoneNumber = new_shippingAcc.contactMethod.data

        # add/commit to database
        db.session.add(new_shippingAcc)
        db.session.commit()
        message = f'New shipping account {new_shippingAcc.nameofShippingAccount.data} added'
        print("Added")
        return render_template('MultipleShippingAccs.html', new_ship_acc_form=new_ship_acc_form,
                               message=message,
                               user=current_user.as_dict())

    else:
        print("New Shipping Form is not valid", new_ship_acc_form.errors)
        error = "Form invalid"

    return render_template('MultipleShippingAccs.html', new_ship_acc_form=new_ship_acc_form,
                           message=message, user=current_user.as_dict())


if __name__ == '__main__':
    app.run(debug=True)
