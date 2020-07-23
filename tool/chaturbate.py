from enum import Enum
from tool.modules.chaturbate_search import ChaturbateSearch, ChatrubateCam, Gender, Tag


if __name__ == '__main__':
    """
    you can search on chaturbate with 2 methods
    
    QUERY
    inside the search method you can specify
    - In search() you can specify a gender
        - gender=Gender.MALE (MALE, FEMALE, TRANS, COUPLE) DEFAULT: Gender.NONE (query all)
    - In search() you can specify a gender
        - tag=Tag.ASIAN (a lot of tags) 
            + to build custom tag use MyTag = Enum('MyTag', {'CUSTOM': 'tag_name/'}) !!--remember the / at the end--!!
            + and then pass MyTag.CUSTOM to the method
        - gender=Gender.MALE (MALE, FEMALE, TRANS, COUPLE) DEFAULT: Gender.NONE (query all)
    
    in both the search you can add this aditional parameters
        query="yumi" a keyword to find in username on the site DEFAULT: ""
        nr_pages: the number of pages where search in (more pages == more time) DEFAULT: 1
        
    FILTER
    ChaturbateSearch().search_tag().filter_by()
    params
    in filters you have to use a lambda
    
        - age=lambda age: True if 18 <= age <= 19 else False
        - gender=Gender.FEMALE
        - uptime=lambda uptime: True if 18 <= uptime <= 19 else False,
        - spectators=lambda spectators: True if 1 <= spectators <= 2000 else False,
    
    WHAT YOU HAVE TO DO
    cams = ChaturbateSearch(...).search_tag(...)
    print(cam.results) to get unfiltered data
    
    cams = ChaturbateSearch().search_tag(...).filter_by(...)
    print(cam.filtered_results) to get filtered data
    print(cam.results) you still get the unfiltered results
        you can filter as many times you want 
        keeping results always untouched
    """
    MyTag = Enum('MyTag', {'CUSTOM': 'asian/'})

    # cams = ChaturbateSearch().search().filter_by(age=18, filter_gender=Gender.COUPLE)

    cams = ChaturbateSearch().search_tag(
        tag=MyTag.CUSTOM,
        gender=Gender.FEMALE
    )

    cams = cams.filter_by(
        age=lambda age: True if 18 <= age <= 22 else False,
        uptime_min=lambda uptime_min: True if 30 <= uptime_min <= 200 else False,
        spectators=lambda spectators: True if 1 <= spectators <= 20 else False,
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
