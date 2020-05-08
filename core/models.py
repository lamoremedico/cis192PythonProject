from django.db import models
from django.contrib.auth.models import User
nltk.download('vader_lexicon')
nltk.download('punkt')
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer



class Entry(models.Model):
	text = models.TextField()
	categories = models.TextField()
	isPinned = models.BooleanField(default=False)
	isFavorited = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="created_by")
	created_at = models.DateTimeField()


	def __get_sentiment__(self):
		return SentimentIntensityAnalyzer().polarity_scores(self.text)


	def __get__all__sentiment(self):
		scores = self.__get_sentiment__()
		neg = scores["neg"]
		neu = scores["neu"]
		pos = scores["pos"]
		return [neg, neu, pos]

