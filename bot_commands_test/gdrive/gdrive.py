from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveManager:

    def __init__(self):
        google_auth = GoogleAuth()
        google_auth.LocalWebserverAuth()
        self.drive = GoogleDrive(google_auth)

        self.file_list = None

    def __get_file_list(self, query_set):

        query_str = "'{}' in parents and trashed=false"
        query = {'q': query_str.format('root')}
        files = self.drive.ListFile(query).GetList()

        while query_set:
            next_file_name = query_set.pop(0)
            for file in files:
                file_name = file.get('title')
                if file_name == next_file_name:
                    query = {'q': query_str.format(file.get('id'))}
                    print('title: {}, id: {}'.format (file_name, file['id']))

            files = self.drive.ListFile(query).GetList()

        self.file_list = files

    def __download_file(self):
        for file in self.file_list:
            print(file['alternateLink'])
            print('title: %s, id: %s' % (file['title'], file['id']))
        return

    def void_arg(self):
        return 

    def google_drive_manager(self):
        query_set = ['IUM', 'dispense']
        self.__get_file_list(query_set)
        self.__download_file()


gdm = GoogleDriveManager()
gdm.google_drive_manager()
