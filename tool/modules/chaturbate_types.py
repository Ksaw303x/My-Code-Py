from enum import Enum


class Tag(Enum):
    ASIAN = 'asian'
    PETITE = 'petite'
    TEEN = 'teen'
    CUTE = 'cute'
    SHY = 'shy'

    @staticmethod
    def tag_url(tag):
        return 'tag/{}/'.format(tag)


class Gender(Enum):
    NONE = '', '', ''
    MALE = 'genderm', 'male-cams/', 'm/'
    FEMALE = 'genderf', 'female-cams/', 'f/'
    COUPLE = 'genderc', 'couple-cams/', 'c/'
    TRANS = 'gendert', 'trans-cams/', 't/'

    @staticmethod
    def gender_by_id(gender_id: str):
        """
        Check if the GenderItem is in Gender
        evaluate by ITEM[1] : [genderm, genderf, genderc, gendert]
        :param gender_id:
        :return:
        """
        items_list = [attr for attr in dir(Gender) if not callable(getattr(Gender, attr)) and not attr.startswith("__")]
        for attr in items_list:
            if gender_id == getattr(Gender, attr).value[0]:
                return getattr(Gender, attr)
        return Gender.NONE


class ChatrubateCam:
    def __init__(self, username: str):
        self.username: str = username.replace('/', '')
        self.__url: str = ''
        self.__age: int = 20
        self.gender: Gender = Gender.NONE
        self.location: str = ''
        self.uptime_min: int = 0
        self.spectators: int = 0

    def __eq__(self, other):
        if not isinstance(other, ChatrubateCam):
            return NotImplemented
        return self.url == other.url

    @property
    def url(self):
        return self.__url

    def build_url(self, url):
        self.__url = url + self.username

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        try:
            self.__age = int(value)
        except ValueError:
            self.__age = 0

    def build_info(self, info):
        reverse_info = info[::-1]
        s = reverse_info.split(',', 1)
        """
        s[0] = 'irotatteps 021' 
        - split on space --> .split(' ', 1)
        - take the number --> [1]
        - revert the number --> [::-1]
        """
        self.spectators = int(s[0].split(' ', 1)[1][::-1])
        """
        s[1]
            - snim 24
            - srh 5,4
        - revert --> time_info = s[1][::-1]
        - split --> .split() '['6,0', 'hrs']'
        
        if 'hrs' 
            time_info[0].split(',') '['6', '0']'
            int(t[0])*60 + int(t[1]) convert in min 6*60 + 0
        else
            save directly
        
        """
        time_info = s[1][::-1].split()
        if time_info[1] == 'hrs':
            t = time_info[0].split(',')
            self.uptime_min = int(t[0])*60 + int(t[1])
        else:
            self.uptime_min = int(time_info[0])
