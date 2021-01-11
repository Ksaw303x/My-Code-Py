from enum import Enum
from chaturbate_api import ChaturbateSearch, ChatrubateCam, Type, Tag


if __name__ == '__main__':

    MyTag = Enum('MyTag', {'CUSTOM': '18/'})

    # cams = ChaturbateSearch().search().filter_by(age=18, filter_gender=Gender.COUPLE)

    cams = ChaturbateSearch().search_tag(
        tag=MyTag.CUSTOM,
        gender=Type.FEMALE
    )

    cams = cams.filter_by(
        age=lambda age: True if 19 <= age <= 19else False,
        uptime_min=lambda uptime_min: True if 30 <= uptime_min <= 200 else False,
        # spectators=lambda spectators: True if 1 <= spectators <= 20 else False,
    )

    if cams.filtered_results:
        for cam in cams.filtered_results:
            cam: ChatrubateCam
            print(
                cam.gender.name.title(),
                cam.age,
                cam.url,
                'location:"{}" uptime: {} spectators: {}'.format(cam.location, cam.uptime_min, cam.spectators)
            )
    else:
        print('No Results')
