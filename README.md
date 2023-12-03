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
  - [Authenticate](#authentication)
  - [Manage employees](#employee)
  - [Manage customers](#customer)
  - [Manage contracts](#contract)
  - [Manage events](#event)
    
## Preamble
This application was designed for a school project with specific requirements and fixed constraints. 
For example, here client-server architecture was not an available option event if it would have been more appropriate for security reason. 
Conversely, CLI was a requirement.
It was developed in a limited period of time and in this context this project is not intended
be perfect and to evolve that much once finished. This project is not open to contribution.
The following need is fictive.

## About the project

<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/d8793335-d6c6-429e-b203-9869ee11eff1" alt="Epic Events logo" width=400>

### Project context
Epic Events is French company specialized in organizing events for professionals. The company has been growing for the past few years and 
the number of events organized has increased. The company has decided to develop an internal CRM (Customer Relationship Management) software to manage its customers and events.
The company gave me the business requirements and I had to design and implement the database and develop the software.


### Screenshots
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/1c14e92f-c601-4143-8fcf-5d3ad7e60de9" alt="crm --help" ><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/b40ed70a-c5df-40ba-b79f-038085734d6a" alt="crm customer list"><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a9f6f306-1a34-43ff-88d2-c3af82be229d" alt="crm event detail">

### About the project design
The application:
- is a **command line** tool,
- displays data with a nice **terminal** user interface (TUI),
- authentications are **session** based: a token is created at login with a limited lifetime,
- permissions are **role** based and **resource** based,
- data are stored in a local **database** (schema available [here](https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/2f656690-18a2-48d6-8e74-8391fcc9e836)),
- subcommands were designed using **DDD** approach (Domain Driven Design) for business efficiency,
- architecture is using pattern **Model-View-Controller** to have a clear separation between the code manipulating data (model) and the one for the user interface (view),
- is following **security** best practices (password hashing, JWT token, etc.),
- errors are **logged** to a monitoring tool,
- code is **tested** with unit tests and integration tests.

Other minor facts about the project:
- compliant flake8,
- documented with docstrings, CLI help and the "How To" part of this README,
- managed by Poetry for virtual environment and dependencies,
- configured using pyproject.toml,
- formatted with black.

## Technology

This application was tested with Python `3.11`  and [Poetry](https://python-poetry.org/) `1.5` (for the virtual environnement and dependencies).
### Main external dependencies:

- Database: [SQLAlchemy ORM](https://pypi.org/project/SQLAlchemy/) using [SQLite](https://www.sqlite.org)
- Command Line Interface: [click](https://pypi.org/project/click/) 
- Terminal User Interface: [rich](https://pypi.org/project/rich/)
- Authentication: [PyJWT](https://pypi.org/project/PyJWT/)
- Error logging and monitoring: [Sentry](https://pypi.org/project/sentry-sdk/)
- Testing: [Pytest](https://pypi.org/project/pytest/)

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

#### Permissions
All authenticated users have - at least - read access to resources (employees, customers, contracts and events).

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
Only administrator employees can perform write operations on employees.

#### Screenshots
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/4d63cd11-f394-4f1c-ba2e-b4db2bd77a36" alt="'crm employee list' output"><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/2150848b-5c8b-4b96-a13b-dc5764d02b5c" alt="'crm employee list' output">

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
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/b40ed70a-c5df-40ba-b79f-038085734d6a" alt="'crm customer list' output"><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/fc7bdfee-55ea-45a8-87a6-35bf22f881a1" alt="'crm customer detail' output">

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
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a2f810f8-5fac-4439-9570-f7365cff3e97" alt="'crm contract list' output"><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/43814769-7454-4f84-8897-dbee614e3188" alt="'crm contract detail' output">

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
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/ad9bcc92-1952-4cb6-8d45-aabcf1e5a06c" alt="'crm event list' output"><br>
<img src="https://github.com/nanakin/OC-P12-CRM-backend/assets/14202917/a9f6f306-1a34-43ff-88d2-c3af82be229d" alt="'crm event detail' output">

## Server configuration 

> **_DISCLAIMER:_**  This file is not supposed to be versioned in a real-life project as a .env file typically wouldn't be.

Configuration is done via `crm.toml` file. It is located in the project root directory.

To enable/disable error tracing with sentry, change `enabled` boolean value, under `error_tracing` category, and set the `dns` key accordingly.

Available configuration options for `database` category are:
- `url`: database url
- `echo`: boolean to enable/disable SQLAlchemy echo mode
- `reset`: boolean to enable/disable database reset on application start

Available option to populate database with fake data: `populate` boolean, under `database_sample`. Note that
the application requires roles to be created before usage.

The JWT secret key is stored in `'authentication_secret_key` option, under `controller` category.
