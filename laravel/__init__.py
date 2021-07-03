import os

from boilerplate import Boilerplate


class LaravelBoilerplate(Boilerplate):
    type = 'laravel'

    def __init__(self, path, projectName):
        super().__init__(path, projectName)

    def init(self):
        os.chdir(self.path)
        os.system(f"composer create-project laravel/laravel {self.projectName}")

    def dependencies(self):
        os.chdir(os.path.join(self.path, self.projectName))
        adminlte = input('Do you want to use AdminLTE layout? [Y/n] ').lower() != 'n'
        if adminlte:
            os.system("composer require jeroennoten/laravel-adminlte")
            os.system("php artisan adminlte:install")
        os.system("composer require laravel/ui")
        os.system("php artisan ui vue --auth")
        if adminlte:
            os.system("php artisan adminlte:install --only=main_views")
            os.system("php artisan adminlte:install --only=config")

        livewire = input('Do you want to use Livewire? [Y/n] ').lower() != 'n'
        if livewire:
            os.system("composer require livewire/livewire")
            os.system("php artisan livewire:publish --config")
            os.chdir(os.path.join(self.path, self.projectName, "config"))

    def code(self):
        pass
