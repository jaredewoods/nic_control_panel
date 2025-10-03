from model.network import ensure_admin
from controller.controller import AppController
from view.app_view import AppView

if __name__ == "__main__":
    ensure_admin()
    controller = AppController()
    AppView(controller).mainloop()
