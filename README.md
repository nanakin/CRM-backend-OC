# Internal Customer Relationship Management Software

## Table Of Contents

- [Preamble](#preamble)
- [About the project](#about-the-project)
  - [Project context](#project-context)
  - [About the project design](#about-the-project-design)
- [Technology](#technology)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to](#how-to)
  - [Authentication](#authentication)
  - [Employee](#employee)
  - [Customer](#customer)
  - [Contract](#contract)
  - [Event](#event)
    
## Preamble
This application was designed for a school project with specific requirements and fixed constraints.
It was developed in a limited period of time and in this context this project is not intended
to evolve that much once finished. This project is not open to contribution.
The following need is fictive.

## About the project

<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a779a523-3fc2-4d29-b9f1-0329d47cb691" alt="Epic Events logo" width=100>

### Project context

### Screeshots
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/1c14e92f-c601-4143-8fcf-5d3ad7e60de9" alt="crm --help" ><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/b40ed70a-c5df-40ba-b79f-038085734d6a" alt="crm customer list"><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a9f6f306-1a34-43ff-88d2-c3af82be229d" alt="crm event detail">

### About the project design
database schema available [here](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/2f656690-18a2-48d6-8e74-8391fcc9e836)

## Technology

This application was tested with [python](https://www.python.org/) `3.11`  and [poetry](https://python-poetry.org/) `1.5` (for the virtual environnement and dependencies).
### Main dependencies:

- Database: [SQLAlchemy]()
- Command Line Interface: [click]() 
- Terminal User Interface: [rich]()
- Authentication: [Simple JWT]()

## Installation

1. Clone this repository
   ```sh
   git clone https://github.com/nanakin/OC-P12-CRM.git CRM-project
   ```
2. Move to the project directory
   ```sh
   cd CRM-project
   ```
3. Install poetry if not installed yet, by following the official documentation here : https://python-poetry.org/docs/#installation

4. Install project dependencies in a new virtual environment using poetry

   ```sh
   poetry install
   ```
   and use it
   ```sh
   poetry shell
   ```
5. Start using `crm` tool
   ```sh
   crm --help
   ```
6. Don't forget to consult the [How to](#how-to) part

## Configuration

## How To

This application is a command line tool. It is used with the `crm` command.

All available subcommand are:
- `crm auth` : [authentication management](#authentication)
- `crm employee` : [employees management](#employee)
- `crm customer` : [customers management](#customer)
- `crm contract` : [contracts management](#contract)
- `crm event` : [events management](#event)

See `crm --help` for more details, and `crm <subcommand> --help` for subcommand details.


### Authentication

All CRM operation requires authentication. 

- To authenticate:  `crm auth login` <br>
*A 30 minutes session is created.*
- To logout:  `crm auth logout`

See `crm auth --help` for more details.

Note : All authenticated users have a read access to resources (employees, customers, contracts and events).

### Employee

This application is designed to be used by authenticated employees. Depending on their role, they can perform different actions.

- To list all employees:  `crm employee list`<br>
*A filter `--role-filter` is available to list only employees with a specific role.*
- To see employee's details:  `crm employee detail`
- To create a new employee:  `crm employee add`
- To set employee's role:  `crm employee set-role`
- To set employee's password:  `crm employee set-password`
- To update employee's details:  `crm employee update`<br>
*The fullname and the username can be updated by this command.*
- To delete an employee:  `crm employee delete`

See `crm employee <subcommand> --help` for more details.

#### Permissions 
- Only administrator employees can perform write operations on employees.

#### Screenshots
![employee_list](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/4d63cd11-f394-4f1c-ba2e-b4db2bd77a36)
![employee_details](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/2150848b-5c8b-4b96-a13b-dc5764d02b5c)


### Customer
Customers are one of the principal resource of this application. They are the one who order events (and sign/pay contracts) to the company.
Each customer is associated with a commercial employee.

- To list all customers:  `crm customer list`
- To see customer's details:  `crm customer detail`
- To create a new customer:  `crm customer add`
- To set customer's commercial employee:  `crm customer set-commercial`
- To update customer's details (fullname or username):  `crm customer update` <br>
*The fullname, the company, the email and the phone can be updated by this command.*

See `crm customer <subcommand> --help` for more details.

#### Permissions
- Only commercial employees can create customers. They can also modify their own customers.
- Except `set-commercial` operation, which can be performed by an administrator employee.

#### Screenshots
![customer_list](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/b40ed70a-c5df-40ba-b79f-038085734d6a)
![customer_details](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/fc7bdfee-55ea-45a8-87a6-35bf22f881a1)

### Contract
Contracts define the event(s) price and must be signed before organizing them.

- To list all contracts:  `crm contract list` <br>
*Filters `--not-signed-filter` an `--not-paid-filter` are available to list only contracts with a specific status.*
- To see contract's details:  `crm contract detail`
- To create a new contract:  `crm contract add`
- To sign a contract:  `crm contract sign`
- To pay a contract:  `crm contract add-payment`
- To update contract's details:  `crm contract update` <br>
*The contract amount and customer can be updated by this command.*

See `crm contract <subcommand> --help` for more details.

#### Permissions
- Only administrator employees can create a new contract. They can also modify all contracts.
- Commercial employees can only modify contracts associated with their customers.

#### Screenshots
![contract_list](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a2f810f8-5fac-4439-9570-f7365cff3e97)
![contract_details](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/43814769-7454-4f84-8897-dbee614e3188)


### Event
Organizing events is the main purpose of this application. They are defined by many criteria (date, location, type, etc.)
and must be associated with a contract.

- To list all events:  `crm event list` <br>
*A filter `--no-support-assigned` is available to list only events without a support assigned.*
- To see event's details:  `crm event detail`
- To create a new event:  `crm event add` <br>
*The contract associated must be signed to allow this operation.*
- To assign a support to an event:  `crm event set-support`
- To update event's details:  `crm event update` <br>
*The event's name, date, location, attendees and note can be updated by this command.*

See `crm event <subcommand> --help` for more details.

#### Permissions
- Only commercial employees can create new events associated with their customers.
- Only administrator employees can assign a support to an event.
- Only support employees can update events associated with them.

#### Screenshots
![event_list](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/ad9bcc92-1952-4cb6-8d45-aabcf1e5a06c)
![event_details](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a9f6f306-1a34-43ff-88d2-c3af82be229d)
