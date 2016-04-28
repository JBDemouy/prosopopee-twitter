import sys
import yaml
import twitter


def get_all_tweets_needed(t, screen_name, tweet_id):
    tweets = list(reversed(t.GetUserTimeline(screen_name=screen_name, since_id=tweet_id, count=200)))

    count = 1

    while count != 10:
        if len(tweets) < count * 200:
            print "I got all the tweets needed \o/"
            break

        count += 1

        tweets = list(reversed(t.GetUserTimeline(screen_name=screen_name, since_id=tweet_id, max_id=tweets[0].id, count=200))) + tweets

    else:
        print "Tried to grab 2000 tweets and couldn't find original tweet, abort."

    return tweets


def get_all_replies(original_tweet, tweets):
    result = [original_tweet.AsDict()]

    replied_to = [original_tweet.id]

    while True:
        next_replied_to = []

        for tweet in tweets:
            if tweet.in_reply_to_status_id in replied_to:
                result.append(tweet.AsDict())
                next_replied_to.append(tweet.id)
                print "Start from: @%s: %s" % (tweet.user.screen_name, tweet.text)

        if len(next_replied_to) == 0:
            print "could not found any other tweets in the reply tree"
            break

        replied_to = next_replied_to

    return result


def main():
    tweet_url = sys.argv[1]
    tweet_id = int(filter(None, tweet_url.split("/"))[-1])
    screen_name = filter(None, tweet_url.split("/"))[-3]


    t = twitter.Api(**yaml.safe_load(open("conf.yaml")))

    original_tweet = t.GetStatus(id=tweet_id)

    print "Start from: @%s: %s" % (original_tweet.user.screen_name, original_tweet.text)


    tweets = get_all_tweets_needed(t, screen_name, tweet_id)

    result = get_all_replies(original_tweet, tweets)

    open("%s_%s.yaml" % (screen_name, tweet_id), "w").write(yaml.dump(result).replace("!!python/unicode ", ""))


if __name__ == '__main__':
    main()
