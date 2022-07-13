from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    employee_number = Column(Integer, nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    orders =  menu_items = relationship("Order", back_populates="employee")

class Menu(db.Model):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    menu_items = relationship("MenuItem", back_populates="menu")

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    menu_type_id = Column(Integer, ForeignKey("menu_item_types.id"), nullable=False)

    menu = relationship("Menu", back_populates="menu_items")
    type = relationship("MenuItemType", back_populates="menu_items")
    order_details = relationship("OrderDetail", back_populates="menu_item")


class MenuItemType(db.Model):
    __tablename__ = 'menu_item_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    menu_items = relationship("MenuItem", back_populates="type")

class Table(db.Model):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)

    orders =  menu_items = relationship("Order", back_populates="table")


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"),nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"),nullable=False)
    finished = Column(Boolean, nullable=False)

    employee = relationship("Employee", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"),nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"),nullable=False)

    order = relationship("Order", back_populates="order_details")
    menu_item = relationship("MenuItem", back_populates="order_details")
