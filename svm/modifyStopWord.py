from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
stops.remove(u'don')
stops.remove(u'not')
stops.remove(u'all')
stops.remove(u'any')
stops.remove(u"aren't")
stops.remove(u'because')
stops.remove(u'been')
stops.remove(u'before')
stops.remove(u'but')
stops.remove(u"can't")
stops.remove(u'cannot')
stops.remove(u'could')
stops.remove(u"couldn't")
stops.remove(u'did')
stops.remove(u"didn't")
stops.remove(u'does')
stops.remove(u"doesn't")
stops.remove(u"don't")
stops.remove(u'down')




