from analysis.sentiment import Sentiment


def analysis(sentiment):
    sentiment.analysis()
    sentiment.update()


def show(sentiment):
    points = sentiment.get()
    print(points)


if __name__ == '__main__':
    senti = Sentiment()
    analysis(sentiment=senti)
    show(sentiment=senti)
