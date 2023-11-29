from typing import Optional

from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException

from crm.model.models import Customer, Employee, OperationFailed


class CustomerModelMixin:
    """Model Mixin to manage customers data."""

    Session: sessionmaker

    def get_customers(self) -> list[dict]:
        """Retrieve customers from the database and return them as a list of dictionaries."""
        with self.Session() as session:
            result = session.query(Customer).order_by(Customer.fullname)
            return [row.as_dict(full=False) for row in result]

    def detail_customer(self, customer_id: int) -> dict:
        """Retrieve a given customer from the database and return it as a dictionary."""
        with self.Session() as session:
            customer = Customer.get(session, customer_id)
            return customer.as_dict()

    def add_customer(self, fullname: str, company: str, email: str, phone: str, employee_id: int) -> dict:
        """Add a new customer to the database (and return it as a dictionary)."""
        with self.Session() as session:
            connected_employee = Employee.get(session, employee_id=employee_id)
            try:
                customer = Customer(
                    fullname=fullname,
                    email=email,
                    phone=phone,
                    company=company,
                    commercial_contact_id=connected_employee.id,
                )
                session.add(customer)
                session.commit()
                return customer.as_dict()
            except PhoneNumberParseException:
                raise OperationFailed(f"Invalid phone number format ({phone})")

    def update_customer_data(
        self,
        customer_id: int,
        fullname: Optional[str],
        company: Optional[str],
        email: Optional[str],
        phone: Optional[str],
        employee_id: Optional[int],
    ) -> dict:
        """Update customer fields in the database (and return it as a dictionary)."""
        with self.Session() as session:
            connected_employee = Employee.get(session, employee_id=employee_id)
            customer = Customer.get(session, customer_id)
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
            return customer.as_dict()

    def set_customer_commercial(self, customer_id: int, commercial_username: str) -> dict:
        """Update the commercial associated to customer in database (and return the customer as dictionary)."""
        with self.Session() as session:
            commercial = Employee.get(session, username=commercial_username)
            if commercial.role.name.upper() != self.roles.COMMERCIAL.name.upper():  # temp
                raise OperationFailed(
                    f"The employee {commercial} assigned as commercial is not a commercial ({commercial.role})."
                )
            customer = Customer.get(session, customer_id)
            customer.commercial_contact_id = commercial.id
            customer.commercial_contact = commercial
            session.add(customer)
            session.commit()
            return customer.as_dict()
