import datetime

from crm.model import Contract, Customer, Employee, Event, Role


def get_roles():
    roles = {
        "NONE": Role(name="NONE"),
        "COMMERCIAL": Role(name="COMMERCIAL"),
        "SUPPORT": Role(name="SUPPORT"),
        "ADMINISTRATOR": Role(name="ADMINISTRATOR"),
    }
    return roles


def get_employees(roles):
    employees = {
        "caroline": Employee(
            fullname="Caroline Cridouta", username="caroline_c", password="caroline", role_id=roles["COMMERCIAL"].id
        ),
        "christelle": Employee(
            fullname="Christelle Carlou", username="christelle_c", password="christelle", role_id=roles["COMMERCIAL"].id
        ),
        "christophe": Employee(
            fullname="Christophe Criselleau",
            username="christophe_c",
            password="christophe",
            role_id=roles["COMMERCIAL"].id,
        ),
        "amelie": Employee(
            fullname="Amelie Alami", username="amelie_a", password="amelie", role_id=roles["ADMINISTRATOR"].id
        ),
        "amandine": Employee(
            fullname="Amandine Aprani", username="amandine_a", password="amandine", role_id=roles["ADMINISTRATOR"].id
        ),
        "amori": Employee(
            fullname="Amori Aurpière", username="amori_a", password="amori", role_id=roles["ADMINISTRATOR"].id
        ),
        "sebastien": Employee(
            fullname="Sebastien Serbot", username="sebastien_s", password="sebastien", role_id=roles["SUPPORT"].id
        ),
        "sarah": Employee(fullname="Sarah Sergin", username="sarah_s", password="sarah", role_id=roles["SUPPORT"].id),
    }
    return employees


def get_customers(employees):
    customers = {
        "EDF": Customer(
            fullname="Thomas Duval",
            email="thomas@edf.fr",
            phone="+33683680178",
            company="EDF",
            commercial_contact_id=employees["caroline"].id,
        ),
        "Withings": Customer(
            fullname="Céline Karari",
            email="celine@withings.fr",
            phone="+337849900022",
            company="Withings",
            commercial_contact_id=employees["christophe"].id,
        ),
        "BK": Customer(
            fullname="Johanna Baker",
            email="johanna@bk.com",
            phone="+48893890045",
            company="Burger King",
            commercial_contact_id=employees["caroline"].id,
        ),
        "M6": Customer(
            fullname="Inès Pradella",
            email="ines.pradella@gmail.com",
            phone="+33673890044",
            company="M6 Events",
            commercial_contact_id=employees["christelle"].id,
        ),
    }
    return customers


def get_contracts(customers):
    contracts = {
        "BK_announcement": Contract(customer_id=customers["BK"].id, signed=True, total_amount=45000),
        "BK_announcement_2": Contract(customer_id=customers["BK"].id, signed=True, total_amount=1000),
        "EDF_SG": Contract(customer_id=customers["EDF"].id, signed=True),
        "EDF_announcement": Contract(customer_id=customers["EDF"].id, signed=False),
        "Festival": Contract(customer_id=customers["M6"].id, signed=False),
        "Withings_party": Contract(
            customer_id=customers["Withings"].id,
            signed=True,
        ),
    }
    return contracts


def get_events(contracts, employees):
    events = {
        "EDF_SG": Event(
            name="EDF Summer Gathering",
            contract_id=contracts["EDF_SG"].id,
            support_contact_id=employees["sebastien"].id,
            start=datetime.datetime(year=2024, month=8, day=20, hour=14),
            end=datetime.datetime(year=2024, month=8, day=20, hour=14),
            attendees=2000,
            location="Jardin des plantes de Paris",
            note="En cas de pluie, déplacer les chaises dans la salle de projection.",
        ),
        "BK_menu": Event(
            name="Nouveau menu raclette",
            contract_id=contracts["BK_announcement_2"].id,
            support_contact_id=employees["sarah"].id,
            start=datetime.datetime(year=2024, month=10, day=21, hour=20),
            end=datetime.datetime(year=2024, month=10, day=21, hour=21),
            attendees=100,
            location="Salle des fêtes de Nantes",
            note="Événement privé. Organiser la restauration sur place.",
        ),
        "BK_opening": Event(
            name="Inauguration d'un nouveau BK",
            contract_id=contracts["BK_announcement"].id,
            support_contact_id=employees["sarah"].id,
            start=datetime.datetime(year=2024, month=5, day=20, hour=20),
            end=datetime.datetime(year=2024, month=5, day=20, hour=21),
            attendees=300,
            location="Théatre de Nantes",
            note="Événement accessible au public, sur réservation. Prévoir des pancartes.",
        ),
        "Withings_party": Event(
            name="Lancement d'une nouvelle montre",
            contract_id=contracts["Withings_party"].id,
            support_contact_id=employees["sebastien"].id,
            start=datetime.datetime(year=2024, month=12, day=20, hour=20),
            end=datetime.datetime(year=2024, month=12, day=20, hour=22),
            attendees=1000,
            location="Salle des fêtes de Paris 9e",
            note="Des bons d'achats seront distribués aux salariés à la sortie, prévoir plusieurs intervenants."
        )
    }
    return events
