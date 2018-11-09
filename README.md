# fa-statistics

This is a statistics script for furaffinity art. It's needed when you have really many subscriptions and thousands
submissions and want to check if some artists can be removed from the subscriptions list.

Usage: launch script and give it an address to the directory with downloaded furaffinity art before checking it.
Script will gather statistics about artists represented there and put it in text file called "_"
After watching art and removing art you don't like, launch script again and give it an address second time.
Script will gather new statistics, compare it with what was before and put new statistics in text file "__"

Overall statistics you can gather with time will be put in text file "stats" in the parent directory.
Main information you will get from this statistics is how much of some artist's images you liked and how much percent
of all downloaded art so you can decide if you really want to be subscribed to an artist which has less than 10% of
art you like but makes more than 10% of all art you watch.
