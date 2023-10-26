from datetime import datetime
import  phonenumbers
from sqlalchemy import DateTime, ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PhoneNumberType

from .common import Base, OperationFailed


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(Unicode(255))
    email: Mapped[str] = mapped_column(EmailType)  # try type
    phone: Mapped[str] = mapped_column(PhoneNumberType)
    company: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, fullname={self.fullname!r}, company={self.company!r})"

    def as_printable_dict(self):
        return {"ID": str(self.id), "Full name": self.fullname, "Company": self.company,  "Commercial contact": str(self.commercial_contact_id),
                "Email": str(self.email), "Phone": str(self.phone), "Creation date": str(self.creation_date),
                "Last modification": str(self.last_modified)}

    def as_printable_tuple(self):
        return str(self.id), self.fullname, self.company, str(self.commercial_contact_id)


class CustomerModelMixin:

    def _get_customer(self, id=None, missing_ok=True):
        result = None
        with self.Session() as session:
            result = session.query(Customer).filter_by(id=id).one_or_none()
        if not missing_ok and result is None:
            raise OperationFailed(f"Cannot find the customer with id {id}")
        return result

    def get_customers(self):
        with self.Session() as session:
            result = session.query(Customer).all()
        return result

    def detail_customer(self, id):
        customer = self._get_customer(id)
        return customer.as_printable_dict()

    def add_customer(self, fullname, company, email, phone, commercial):
        print("phone", phone)
        valide_phone = phonenumbers.parse(phone, None)
        customer = Customer(fullname=fullname, email=email, phone=phone, company=company, commercial_contact_id=1)  # to change
        with self.Session() as session:
            session.add(customer)
            session.commit()
        return customer.as_printable_dict()

    def update_customer_data(self, id, fullname, company, email, phone):
        customer = self._get_customer(id=id)
        with self.Session() as session:
            if fullname:
                customer.fullname = fullname
            if email:
                customer.email = email
            if phone:
                customer.phone = phone
            if company:
                customer.company = company
            session.add(customer)
            session.commit()

    def set_customer_commercial(self, id, commercial_username):
        employee = self._get_employee(username=commercial_username)
        customer = self._get_customer(id=id)
        with self.Session() as session:
            customer.commercial_contact_id = employee.id
            session.add(customer)
            session.commit()
