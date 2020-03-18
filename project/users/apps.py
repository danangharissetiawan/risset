from django.apps import AppConfig
# import signals


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
