def logCrawlProgress(info):
    with open('GetId.log','at') as file:
        file.write(info)