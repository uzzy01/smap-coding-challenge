from django.core.management.base import BaseCommand
from consumption.models import user_data, consumption_data
from django.conf import settings
from datetime import datetime
import csv, os, sys, pytz

class Command(BaseCommand):
    help = 'import data'

    def __init__(self):
        self.user_data_array = []
        self.consumption_data_dir = settings.CONSUMPTION_DATA_DIR
        self.user_data_path = os.path.join(settings.USER_DATA_DIR, 
                                           settings.USER_DATA_FN)

    def add_arguments(self, parser):
        parser.add_argument('folder', nargs='?')

    def handle(self, *args, **options):
        custom_folder_from_cmd = options['folder']

        if custom_folder_from_cmd:
            self.user_data_path = custom_folder_from_cmd

        try:
            self.run_import()
        except Exception as e:
            # roll back
            self.delete_data()
            sys.exit(str(e))

    def run_import(self):
        current_user_data = user_data.objects.all()
        current_consumption_data = consumption_data.objects.all()
        
        if current_user_data or current_consumption_data:
            ans = input('Current data exists, would you like to delete & import [y/n]? ')
            if ans.lower() == 'y':
                print('* Deleting data..')
                self.delete_data()
            else:
                sys.exit(str(e))

        self.user_data_import()
        self.consumption_data_import()

    def delete_data(self):
        user_data.objects.all().delete()
        consumption_data.objects.all().delete()

    def user_data_import(self):
        check_path = os.path.exists(self.user_data_path)

        if check_path:
            print('* Importing new user data..')
            with open(self.user_data_path, 'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                objArr = []

                for row in reader:
                    #build list for user id
                    self.user_data_array.append(row['id'])
                    objQuery = user_data(
                                user_id=row['id'], 
                                area=row['area'], 
                                tariff=row['tariff']
                            )
                    objArr.append(objQuery)  
            result = user_data.objects.bulk_create(objArr)
            f.close()
            print('* User data has successfully imported.')
        else:
            sys.exit('* File path: ' + self.user_data_path + ' doesn''t exist, please check settings')

    def consumption_data_import(self):
        print('* Importing consumption data, please wait..')
        objArr = []
        
        for user_id in self.user_data_array:
            user = user_data.objects.get(user_id=user_id)
            filename = user_id+'.csv'
            directory = os.path.join(self.consumption_data_dir, filename)
            check_path = os.path.exists(directory)

            if not check_path:
                print('* File path:', directory, 'doesn''t exist')
                continue

            with open(directory, 'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    objQuery = consumption_data(
                                user_id = user,
                                datetime = pytz.utc.localize(datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')),
                                consumption = row['consumption']
                            )
                    objArr.append(objQuery)
            f.close()

        consumption_data.objects.bulk_create(objArr)
        print('* Consumption data successfully imported.')