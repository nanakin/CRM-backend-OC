from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PhoneNumberType
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException

from .common import Base, OperationFailed


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(Unicode(255))
    email: Mapped[str] = mapped_column(EmailType)  # try type
    phone: Mapped[str] = mapped_column(PhoneNumberType)
    company: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    commercial_contact: Mapped["Employee"] = relationship(lazy="subquery")  # noqa: F821
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __str__(self):
        return self.fullname

    def __repr__(self) -> str:
        return (
            f"Customer(id={self.id!r}, fullname={self.fullname!r}, company={self.company!r}, "
            f"commercial={self.commercial_contact_id!r}, email={self.email!r}, phone={self.phone!r}"
            f"creation_date={self.creation_date!r}, last_modified={self.last_modified!r})"
        )

    def as_printable_dict(self, full=False):
        data = {
            "ID": str(self.id),
            "Full name": self.fullname,
            "Company": self.company,
            "Commercial": str(self.commercial_contact)}
        if full:
            data.update({
                "Email": str(self.email),
                "Phone": str(self.phone),
                "Creation date": str(self.creation_date),
                "Last modification": str(self.last_modified)})
        return data


class CustomerModelMixin:
    def _get_customer(self, customer_id=None, missing_ok=False):
        result = None
        with self.Session() as session:
            result = session.query(Customer).filter_by(id=customer_id).one_or_none()
            session.commit()  # necessary ?
        if not missing_ok and result is None:
            raise OperationFailed(f"Cannot find the customer with id {customer_id}")
        return result

    def get_customers(self):
        with self.Session() as session:
            result = session.query(Customer).order_by(Customer.fullname)
            return [row.as_printable_dict(full=False) for row in result]

    def detail_customer(self, customer_id):
        customer = self._get_customer(customer_id)
        return customer.as_printable_dict()

    def add_customer(self, fullname, company, email, phone, employee_id):
        connected_employee = self.get_employee(id=employee_id)
        try:
            with self.Session() as session:
                customer = Customer(
                    fullname=fullname, email=email, phone=phone, company=company, commercial_contact_id=connected_employee.id
                )
                session.add(customer)
                session.commit()
                return customer.as_printable_dict()
        except PhoneNumberParseException:
            raise OperationFailed(f"Invalid phone number format ({phone})")

    def update_customer_data(self, id, fullname, company, email, phone, employee_id):
        connected_employee = self.get_employee(id=employee_id)
        with self.Session() as session:
            customer = (
                session.query(Customer).filter_by(id=id).one_or_none()
            )  # replace by the call to _get_customer to raise not found
            if customer.commercial_contact_id != connected_employee.id:
                raise OperationFailed(
                    f"The employee {connected_employee.fullname} does not have the permission to edit the customer "
                    f"{customer.fullname}."
                )
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
            # session.flush()
            return customer.as_printable_dict()

    def set_customer_commercial(self, id, commercial_username):
        commercial = self.get_employee(username=commercial_username)
        if commercial.role.name.upper() != self.roles.COMMERCIAL.name.upper():  # temp
            raise OperationFailed(
                f"The employee {commercial} assigned as commercial is not a commercial ({commercial.role})."
            )
        with self.Session() as session:
            commercial = session.merge(commercial)
            customer = (
                session.query(Customer).filter_by(id=id).one_or_none()
            )  # replace by the call to _get_customer to raise not found
            customer.commercial_contact_id = commercial.id
            customer.commercial_contact = commercial
            session.add(customer)
            session.commit()
            return customer.as_printable_dict()
