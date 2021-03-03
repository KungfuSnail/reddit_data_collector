This is a reddit data collector.

This reddit data collector program uses PRAW to collect data from Reddit.

There are 2 parts to this program; the first part it collects the data of only one post, the second part of the program it collects the data of 100-300 posts in one subreddit. You can use either.

This program is supposed to be used easily whether you have any coding experience or not. So you only need to run the code.


Part One: To run the program correctly for extracting the data, you need to provide the code with 5 pieces of info: 

1. Url of the post
2. Duration of data collection (ex: For setting the duration for 1 hour, give 60 to the program)
3. Data collection interval (ex: To collect data every 2 minutes, give 2)
4. Whether you want to know if the post is in hot in every data collection interval (true for yes and false for no)
5. The name of the output file (ex: post_332_data.xlsx)

Part Two: For the second part:

1.Name of the Subreddit (no r/xxx just the name)
2.Initial get: At the start, the code gets the first X posts that are already in new. You need to determine how many posts you want to gather.
3.Limit of the list: The code needs to have a limit, because especially in data gatherings that have long durations there will be too many posts to collect data on and that will make the program very slow. So you need to set a limit (ex: 200 posts)
4.Period Length: The time span of the data collection.
5.How long should the data collection intervals be? (Ex collect data for 2 hours: input 120)
6.Check to see if posts are in hot or not every interval. (Ex collect data every 5 minutes of that 2 hour time span: input 5)
7.Output name. (The .xlsx will be added automatically)
