import schedule
import time
import os
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace


# login credentials
username = 'hannaaa_travel'
password = 'Insta78622'

# path to your workspace
set_workspace(path=os.getcwd() + '/data/')


def job():

    session = InstaPy(
        username=username,
        password=password,
        headless_browser=False,
    )

    with smart_run(session):

        # session.set_dont_include(["friend1", "friend2", "friend3"])

        # sets the percentage of people you want to follow
        session.set_do_follow(True, percentage=50)
        session.unfollow_users(
            amount=10,
            delay_followbackers=864000
        )

        session.set_dont_unfollow_active_users(True)
        session.set_action_delays(True)

        # sets the percentage of posts you want to comment
        # session.set_do_comment(True, percentage=100)
        # session.set_comments(["hi @{}, have a look", :heart_eyes: :heart_eyes: @{}"])

        # setting quotas for the daily and hourly action
        session.set_action_delays(
            enabled=True,
            randomize=True,
            random_range_from=2,
            random_range_to=10,
        )
        session.set_quota_supervisor(
            enabled=True,
            peak_comments_daily=20,
            peak_comments_hourly=5,
            peak_likes_daily=100,
            peak_likes_hourly=20,
            sleep_after=['likes', 'follows'])

        session.set_relationship_bounds(
            enabled=True,
            delimit_by_numbers=True,
            max_followers=800,
            min_followers=60,
            min_following=400
        )

        session.like_by_tags(['love', 'javascript'], amount=20)


schedule.every().day.at('06:35').do(job)
schedule.every().day.at('23:40').do(job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(10)
