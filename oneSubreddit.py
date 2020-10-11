
import praw
import time as tttime
from datetime import datetime
import xlsxwriter 

HOW_DEEP_IN_HOT = 200


reddit = praw.Reddit(client_id="9QZ5Vh3VSRXkFA",
                     client_secret="kGWOiF3mLMEyTPE41LC14VhQn3Q",
                     username="bot_for_repl",
                     password="harambeharambe",
                     user_agent="putAnyThingHere"
                     )



def subredditPostsInstance(name, newOrHot, postLimit):
    '''
    :param name: Name of the subreddit.
    :param newOrHot: Should it return the instance with posts in new or hot.
    :param postLimit: Return how many post's instance? Ex: 200
    :return: Instance
    '''
    if newOrHot == "hot":
        return reddit.subreddit(name).hot(limit=postLimit)
    elif newOrHot == "new":
        return reddit.subreddit(name).new(limit=postLimit)


def utcToReal (utcTime):
    return datetime.fromtimestamp(utcTime)


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



def add_new_id(old_array, subs_name, new_or_hot):
    '''

    :param old_array: Old array of ids.
    :param subs_name: Name of the sub.
    :param new_or_hot: Array that we are updating is the array of new posts or hot posts.
    :return: New array of id with new ids.
    '''
    how_far = 1000 # how far to look for for new posts
    subreddit_instance = subredditPostsInstance(subs_name, new_or_hot, how_far)
    all_new_posts_array = get_all_ids(subreddit_instance)

    index = all_new_posts_array.index(old_array[0])
    new_found_post_ids = all_new_posts_array[ : index+1]
    new_found_post_ids.reverse()
    return new_found_post_ids


def time_cleaner(timeStr):
    # Might take too much processing power if I use this func so this is not used
    # takes time format (ex: 4:25:33.124235345235) and gets rid of the second's decimals

    finalTime = ""
    for c in timeStr:
        if c not in ["."]:
            finalTime = finalTime + c
        else:
            return finalTime


def posts_age_giveSubmission(submission):
    # Gets the time from the submission's obj and returns the time difference between
    # now and time the submission was posted and returns it in string format

    # You can use the .ctime() function to turn it into a string while having all the date's data


    timePostedUnix = submission.created_utc
    timePosted = datetime.fromtimestamp(timePostedUnix) # From unix to datetime object type

    now = datetime.now()

    difference = now - timePosted
    #difference = time_cleaner(str(difference)) # My function takes str

    difference = str(difference)
    return difference[0:8]


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



def write_titles(worksheet, id_list, hot_check_or_not):
    '''

    :param worksheet: The worksheet object.
    :param id_list: List of post ids.
    :param hot_check_or_not:                     asldfjal;sfjalsjflasjf;lajkf;.
    :return:
    '''

    jump_for_next_cell = 2
    if hot_check_or_not:
        jump_for_next_cell = jump_for_next_cell + 1

    for item in id_list:
                pos_of_item = id_list.index(item)
                #print(reddit.submission(item).title)
                item_title = reddit.submission(item).title
                worksheet.write(0, (pos_of_item * jump_for_next_cell), item_title)

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


def write_attributes(post_x_in_array, array_of_id, excelSheet, in_hot_or_nope, subs_name):
    '''
    :param post_x_in_array: Xth post in our array that we are going to write in excel
    :param array_of_id: IDs of the posts
    :param excelSheet: The excel sheet to write on
    :param ups: True or false, include upvotes or not
    :param hot_check: Check to see if in hot yet or not
    :param in_hot_or_nope: If you want to see it it is in hot or not, leave a space for it
        so that the next function will put it in the third cell of each posts 3-cell-set
    :return: Nothing
    '''

    # The number of cells needed for each post. Depends how many attributes are included.
    # Two is default for post's age and it's upvotes
    post_size = 2
    if in_hot_or_nope == True:
        post_size = post_size + 1


    for item in array_of_id:
            #print("was here")
            #time = utcToReal(post.created_utc)

            post = reddit.submission(item)
            ups = post.ups
            age_of_post = posts_age_giveId(item)
            item_pos = array_of_id.index(item)

            # item_pos is times 2 so that the age of post n doesn't overwrite post n-1's ups
            excelSheet.write(post_x_in_array, (item_pos*post_size), age_of_post) #Writes the post's age
            excelSheet.write(post_x_in_array, (item_pos*post_size) +1, ups) # The upvotes of the post

    hot_posts = reddit.subreddit(subs_name).hot(limit=HOW_DEEP_IN_HOT)
    hot_ids = get_all_ids(hot_posts)
    # Checks to see if post is in hot section yet and if yes writes true if not writes False
    if in_hot_or_nope:
        for item in array_of_id:
           # print("one")
            #post = reddit.submission(item) # might take lots of time
            item_pos = array_of_id.index(item)
            if post in hot_ids:
                #print("passed me")
                excelSheet.write(post_x_in_array, (item_pos*post_size) +2, "True")
            elif post not in hot_ids:
                #print("passed me2")
                excelSheet.write(post_x_in_array, (item_pos*post_size) +2, "False")

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


def start_func():
    print("Welcome")

    name_of_the_sub = input("What is the name of the sub you would like to gather data on? (no r/xxx just the name) ")
    initial_get = int(input("Take the first X posts that are in new, for the initial get.(Enter X) (Write 20 if in doubt)"))
    limit_of_list = int(input("What is the limit of posts that are added to the list? (adding more than 100 will make it super slow)"))
    period_length = int(input("Time span of data collection? (Ex: 15 minutes, 180 minutes etc) (in minutes)"))
    every_x_min = int(input("Collect data every ___ minutes. (ex every 10 minutes) (in minutes)"))
    check_hot = correct_yes_no()
    output_name = input("The name of the output file? (the .xlsx will be added automatically) ")

    proj(period_length, every_x_min, [name_of_the_sub, "new", initial_get], check_hot, limit_of_list, "{}.xlsx".format(output_name))


def proj(length, everyxMin, instance_attributes,check_posts_if_in_hot,list_max, exportName):
    '''
    Main function. The loop that runs periodically is inside this function.

    '''

    sub_data_list = subredditPostsInstance(instance_attributes[0], instance_attributes[1], instance_attributes[2])
    id_array = get_all_ids(sub_data_list)
    id_array.reverse()


    iterations = length/everyxMin
    iterations = int(iterations)
    print("There will be", iterations, "cycle(s).")


    workbook = xlsxwriter.Workbook(exportName)
    worksheet = workbook.add_worksheet()


    print("Title start at:", tttime.ctime())
    write_titles(worksheet, id_array, check_posts_if_in_hot)
    print("Title done at:",tttime.ctime())

    for i in range(1, iterations+1):
        # Starts from 1 to iterations+1 because i represents the row number in excel
        # and on row 0 the titles are written.
        print("--------------")

        prog_start_time = datetime.now() # For the determine_sleep_time function
        print("Cycle", i, " started at:", tttime.ctime())

        if len(id_array) < list_max:
            id_array = add_new_id(id_array, instance_attributes[0], instance_attributes[1])
            write_titles(worksheet, id_array, check_posts_if_in_hot)

        print("Start writing in excel --", tttime.ctime())
        write_attributes(i, id_array, worksheet, check_posts_if_in_hot, instance_attributes[0])

        prog_finish_time = datetime.now()
        print("Cycle", i, "finished at:", tttime.ctime())


        sleep_x_seconds = determine_sleep_time(everyxMin, prog_finish_time, prog_start_time)


        if i != iterations: # This prevents waiting for x seconds when we're done on the last loop.
            tttime.sleep(sleep_x_seconds)
            print("Next cycle starts in:", sleep_x_seconds, "seconds")

    workbook.close()


start_func()

#Alternatively, just do this:
#proj(1, 1, ["memes","new", 200], True, 200, 'oneLast.xlsx')


