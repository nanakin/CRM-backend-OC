# Internal Customer Relationship Management Software

## Table Of Contents

- [Preamble](#preamble)
- [About the project](#about-the-project)
  - [Project context](#project-context)
  - [About the project design and compliance](#about-the-project-design-and-compliance)
- [Technology](#technology)
- [Installation](#installation)
    
## Preamble
This application was designed for a school project with specific requirements and fixed constraints.
It was developed in a limited period of time and in this context this project is not intended
to evolve that much once finished. This project is not open to contribution.
The following need is fictive.

## About the project

<img src="" alt="Epic Events logo" width=100>

### Project context


### About the project design and compliance


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
