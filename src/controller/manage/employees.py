#from typing import Any

class EmployeesController:

    #view: Any
    #model: Any

    # allowed_requests

    def list_employees(self):
        data = self.model.get_employees()
        print(data, "employee controller")
        self.view.display_employees(data)

    def get_employee(self):
        pass

    def new_employee(self):
        pass

    def edit_data_employee(self):
        pass

    def set_role_employee(self):
        pass

    def delete_employee(self):
        pass
