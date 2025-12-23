import os
import datetime
import subprocess
import yadisk
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Создает дамп PostgreSQL и загружает его на Яндекс.Диск'

    def handle(self, *args, **options):
        YANDEX_TOKEN = 'y0__xDO3uKvCBjblgMg_vGg5RUw497irwgHtdfwNNIoidz48RjGUwxYabGJ7g'
        REMOTE_FOLDER = '/backups/' 
        
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings.get('HOST', 'localhost')
        db_port = db_settings.get('PORT', '5432')

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f'backup_{db_name}_{timestamp}.sql'
        backup_path = os.path.join(settings.BASE_DIR, backup_filename)

        self.stdout.write(f"--- Запуск бэкапа для {db_name} на Яндекс.Диск ---")

        # 1. СОЗДАНИЕ ДАМПА (pg_dump)
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        try:
            dump_command = [
                'pg_dump',
                '-h', db_host,
                '-p', db_port,
                '-U', db_user,
                '-f', backup_path,
                db_name
            ]
            subprocess.run(dump_command, env=env, check=True)
            self.stdout.write(self.style.SUCCESS(f"Локальный дамп создан: {backup_filename}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при создании дампа: {e}"))
            return

        # 2. ЗАГРУЗКА НА ЯНДЕКС.ДИСК
        try:
            y = yadisk.YaDisk(token=YANDEX_TOKEN)

            # Проверяем токен
            if not y.check_token():
                self.stdout.write(self.style.ERROR("Ошибка: Токен Яндекс.Диска недействителен!"))
                return

            # Создаем папку, если её нет (опционально)
            if not y.exists(REMOTE_FOLDER):
                y.mkdir(REMOTE_FOLDER)
                self.stdout.write(f"Создана новая папка {REMOTE_FOLDER}")

            # Путь к файлу на Диске
            remote_path = os.path.join(REMOTE_FOLDER, backup_filename).replace('\\', '/')
            
            self.stdout.write(f"Загружаю файл в {remote_path}...")
            
            with open(backup_path, "rb") as f:
                y.upload(f, remote_path)

            self.stdout.write(self.style.SUCCESS(f"Успешно! Файл {backup_filename} теперь в облаке Яндекс."))

            # 3. УДАЛЕНИЕ ВРЕМЕННОГО ФАЙЛА
            if os.path.exists(backup_path):
                os.remove(backup_path)
                self.stdout.write("Локальная копия удалена.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка Яндекс.Диска: {e}"))