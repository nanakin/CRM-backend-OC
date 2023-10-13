class EmployeesControllerMixin:

    #view: Any
    #model: Any

    def list_employees(self, param=None):
        data = self.model.get_employees()
        print(data, "employee controller")
        self.view.display_employees(data)

    def get_employee(self):
        pass

    def new_employee(self):
        pass

    def edit_data_employee(self, id):
        print("employee controller edit", id)

    def set_role_employee(self):
        pass

    def delete_employee(self):
        pass

    def request_to_action(self):
        Request = self.view.Request

        return {
            Request.LIST_EMPLOYEES: self.list_employees,
            Request.EDIT_EMPLOYEE: self.edit_data_employee}

    # def __init__(self):
    #     self.allowed_actions = self.request_to_action()
