import praw
import time as tttime
from datetime import datetime
import xlsxwriter 


reddit = praw.Reddit(client_id="9QZ5Vh3VSRXkFA",
                     client_secret="kGWOiF3mLMEyTPE41LC14VhQn3Q",
                     username="bot_for_repl",
                     password="harambeharambe",
                     user_agent="putAnyThingHere"
                     )

# GLOBAL VARIABLES
HOW_DEEP_IN_HOT = 120



def get_subreddit_name_from_post_id(the_id):
    '''
    Function name explains it all. Nothing to add.
    But if you want one it gets the submission object from the id and gets the sub's name from the
    submission object.
    :param the_id: Post's id ex: ik7r5f
    :return: The name of the subreddit.
    '''
    post_object = reddit.submission(the_id)
    return post_object.subreddit


def get_all_ids(post_collection_instance):
    '''
    Gets the object containing all the submission objects and get's their ids.
    :param post_collection_instance: The instance object containing x posts.
    :return: List of id's of all the posts.
    '''
    id_array = []
    for submission in post_collection_instance:
        id_array.append(submission.id)
    return id_array


def get_id_from_url(post_url):
    '''
    Gets the url of the post and returns the id of the post.
    :param post_url: The url
    :return: The id of the post

    Ex:https://www.reddit.com/r/HumansAreMetal/comments/ik7py4/badass_woman/
    Output: ik7py4
    '''

    outputString = ""
    nth_slash = 0
    for c in post_url:

        if nth_slash == 6: # After the 6th is the id of the post.
            if c != "/":
                outputString = outputString + c
            elif c == "/": # When c is / again it means we have reached the end of the id, so break.
                break

        elif c == "/": # Adds to the nth until we reach the 6th / which after that is the id.
            nth_slash = nth_slash + 1

        else:
            continue

    return outputString


def posts_age_giveId(id):
    '''
    Returns the time difference between now and time the submission was
    posted and returns it in string format.

    So in other words returns the age of the post.
    '''

    submission = reddit.submission(id)
    timePostedUnix = submission.created_utc
    timePosted = datetime.fromtimestamp(timePostedUnix) # From unix to datetime object type

    now = datetime.now()

    difference = now - timePosted
    #difference = time_cleaner(str(difference)) # My function takes str

    difference = str(difference)
    return difference[0:8]


def correct_yes_no():

    input1 = input("Check to see if in hot or not? (y/n)")

    while   (
            input1.isdigit() == True or
            input1 != "Y" and
            input1 != "y" and
            input1 != "F" and
            input1 != "f"
                        ):

        input1 = input("Please enter y(Y) or n(N) to check to see if in hot or not.")

    if input1 == "y" or input1 == "Y":
        return True
    if input1 == "n" or input1 == "N":
        return False


def determine_sleep_time(everyXmin, last_finish_time, last_start_time):
    '''
    Short one: Determines sleep time, returns sleep time in sec.

    Long one:
    So we want the program start collecting data every 5 minutes.
    If the data collection started at 5pm took 2 minutes, and the cycle duration was set to be
    5 minutes, we'll have to wait 3 minutes so that the next cycle starts at 5:05 pm.

    If the cycle was 5 minutes and data collection took more than 5 minutes, the function's
    output will be set to 0 so that the next cycle starts immediately.
    Data collection might take more than 5 minutes if every time the data of ~200+ posts is
    being collected.


    :param everyXmin: Every x minutes the function will collect data.

    ("THIS loop" is the loop that called the function we are in).
    :param last_finish_time: The time the data collection process of THIS loop ended.
    :param last_start_time: The time the data collection process of THIS loop started.

    :return: int time to wait for the next iteration.
    '''

    period = everyXmin * 60 # Since the function works in seconds we convert minutes to seconds
    time_difference = last_finish_time - last_start_time  # Should be from 2 min to 10 seconds, in date&time form


    # timeObject.seconds will turn the dateTime form into integer form in seconds
    if time_difference.seconds > period:
        return 0
    else:
        return period - (time_difference).seconds


def one_post_analyze(duration, cycle, is_in_hot, post_url, output_name):
    '''

    :param duration: The period's date you want to collect data on. (Ex: 140 minutes)
    :param cycle: Collect data every X minutes.
    :param is_in_hot: Check to see if post is one of the top XXXX* posts of the subreddit's hot section.
    *XXXX = HOW_DEEP_IN_HOT

    :param post_url: The url of the comment's section of the post.
    :param out_name: The excel name which is the output.
    :return: Nothing, output is the excel file.

    To Do:
    1. Should I have add the option to export it into a text file too?
    2. Should I also make another program that graphs that data using R or ggplot or something
    like that? (Learn R first) (How to extract data from excel with R?) (What type of graph?)
    3. Check to see if in top 400 hot posts, then another column for seeing if in top 100 hot posts, etc.
    '''


    id = get_id_from_url(post_url)

    cycle_num = int(duration/cycle)
    print("There will be", cycle_num, "cycle(s)")

    subreddit_name = get_subreddit_name_from_post_id(id)

    # Open workbook
    workbook1 = xlsxwriter.Workbook("{}.xlsx".format(output_name))
    worksheet1 = workbook1.add_worksheet()

    post_title = reddit.submission(id).title
    worksheet1.write(0, 0, "Title: {}".format(post_title))
    worksheet1.write(0, 1, "Upvotes")
    #worksheet1.write(0, 1, "Subreddit's name: {}".format(subreddit_name))
    worksheet1.write(0, 2, "In hot?")

    for i in range(1, cycle_num+1):

        print("Loop:", i, "--", cycle_num - i, "more to go.")

        # Just gets the time the loop started
        prog_start_time = datetime.now()
        print("Cycle start time: ", prog_start_time)

        write_attributes_for_one(i, id, worksheet1, is_in_hot, subreddit_name)

        # Gets the time the process finished
        prog_finish_time = datetime.now()
        print("Cycle finish time:", prog_start_time)

        # Determines how long should it wait so that when it starts it's exactly x minutes apart from
        # when the last loop started.
        sleep_time_in_sec = determine_sleep_time(cycle, prog_finish_time, prog_start_time)
        print("Time until next loop:", sleep_time_in_sec, "seconds...")

        if i != cycle_num: # So that there is no waiting time in the last loop when everything is done.
            tttime.sleep(sleep_time_in_sec)

    workbook1.close()


def write_attributes_for_one(current_cycle_num, post_id, zeWorksheet, check_in_hot, sub_name):
    '''
    The function that writes the attributes of one post.
    :param post_id: Id of the post.
    :param zeWorksheet: The worksheet we are writing on.
    :param check_in_hot: To write if the post is in hot or not. (variable is bool)
    :return: Nothing, just writes the attributes on excel
    '''

    # Change these 3 if you are going to check on more than 1 post.

    ageCoulumn = 0
    upvoteColumn = 1
    hotNotColumn = 2


    # Will be in use if we are going to change this func in the future to check more than 1 post.
    post_size = 2
    if check_in_hot == True:
        post_size = post_size + 1


    post = reddit.submission(post_id)
    ups = post.ups
    age_of_post = posts_age_giveId(post_id)

    # Item_pos is times 2 so that the age of post n doesn't overwrite post n-1's ups
    zeWorksheet.write(current_cycle_num, ageCoulumn, age_of_post) # Writes the post's age
    zeWorksheet.write(current_cycle_num, upvoteColumn, ups) # The upvotes of the post

    if check_in_hot:

        hot_posts = reddit.subreddit(str(sub_name)).hot(limit=HOW_DEEP_IN_HOT)
        hot_ids = get_all_ids(hot_posts)

        if post_id in hot_ids:
            zeWorksheet.write(current_cycle_num, hotNotColumn, "True")
        elif post_id not in hot_ids:
            zeWorksheet.write(current_cycle_num, hotNotColumn, "False")
        else:
            print("Error occured while checking to see if the post is in hot.")
            return -1

#https://www.reddit.com/r/dataisbeautiful/comments/imudp5/oc_weekly_us_deaths_in_the_united_states_first_31/
#Exampleurl1 = "https://www.reddit.com/r/dataisbeautiful/comments/imudp5/oc_weekly_us_deaths_in_the_united_states_first_31/"
#one_post_analyze(10, 2, True, Exampleurl1, "example")

def starter():

    duration = int(input("Collect data for how long? (x minutes)  "))
    cycle = int(input("Collect data every --- minutes.  "))
    check_for_hot = correct_yes_no()
    url = input("Paste the reddit url here please:  ")
    name = input("What name should the output file have?   ")

    one_post_analyze(duration, cycle, check_for_hot, url, name)

starter()
