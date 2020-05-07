from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Entry
from datetime import datetime
from core.sentiment_analysis import *
from plotly.offline import plot
from plotly.graph_objs import Scatter, Figure, Layout
# make sure to pip install plotly

def splash(request):
	return render(request, "splash.html", {})

def journal_stats(request):
	allEntries = Entry.objects.all()
	time_x, time_y = create_by_time(allEntries)
	day_x, day_y = create_by_day(allEntries)
	month_x, month_y = create_by_month(allEntries)
	all_x, all_y, all_tick = create_all(allEntries)

	data_day = [Scatter(x=day_x, y=day_y,
                        mode='lines', name='Sentiment by Day of Week',
                        opacity=0.8, marker_color='green')]
	layout_day = Layout(title='Sentiment by Day of Week',
    					xaxis_title="day of week",
    					yaxis_title="mood")
	chart_day = plot(dict(data=data_day, layout=layout_day), output_type='div')

	data_time = [Scatter(x=time_x, y=time_y,
                        mode='lines', name='Sentiment by Time of Day',
                        opacity=0.8, marker_color='green')]
	layout_time = Layout(title='Sentiment by Time of Day',
    					xaxis_title="time of day",
    					yaxis_title="mood")
	chart_time = plot(dict(data=data_time, layout=layout_time), output_type='div')

	data_month = [Scatter(x=month_x, y=month_y,
                        mode='lines', name='Sentiment by Month',
                        opacity=0.8, marker_color='green')]
	layout_month = Layout(title='Sentiment by Month',
    					xaxis_title="month",
    					yaxis_title="mood")
	chart_month = plot(dict(data=data_month, layout=layout_month), output_type='div')

	data_all = [Scatter(x=all_x, y=all_y,
                        mode='lines', name='Sentiment by Month',
                        opacity=0.8, marker_color='green')]
	tick_vals = []
	tick_names = []
	for i in range(len(all_tick)):
		if all_tick[i] not in tick_names:
			tick_names.append(all_tick[i])
			tick_vals.append(all_x[i])

	layout_all = Layout(title='All Previous Posts',
    					xaxis_title="time",
    					yaxis_title="mood",
						xaxis = dict(
        				tickmode = 'array',
        				tickvals = tick_vals,
        				ticktext = tick_names))
	chart_all = plot(dict(data=data_all, layout=layout_all), output_type='div')
	return render(request, "journalstats.html", {"all_charts": [chart_day, chart_time, chart_month, chart_all]})

def home(request):
	if not request.user.is_authenticated:
		return redirect('/login')
	if request.method == "POST":
		newJournalEntry = request.POST["Entry"]
		#Request category fields here
		entryObj = Entry.objects.create(text=newJournalEntry, categories="placeholder", created_by=request.user, created_at=datetime.now())
	#TODO - order by  pinned
	allEntries = Entry.objects.all().order_by('-isPinned', '-created_at')
	#allEntries = Entry.objects.all().order_by('isPinned').order_by('-created_at')
	#CAN  USE something like below to filter starred or pinned entries
		#tweetsWeLike = Tweet.objects.filter(liked_by__username=request.user.username)
	return render(request, "home.html", {"entries": allEntries})

def favorite(request, theEntry, typeofpage, whatpage):
	test = Entry.objects.get(id=theEntry)
	test.isFavorited = not test.isFavorited
	test.save()
	#Will later need the below branching in order to get back to the right page
	if typeofpage == "h":
		return redirect("/hashtag/" + str(whatpage))
	elif typeofpage == "home":
		return redirect("/")
	else:
		return redirect("/profile/" + str(whatpage))

def pin(request, theEntry, typeofpage, whatpage):
	test = Entry.objects.get(id=theEntry)
	test.isPinned = not test.isPinned
	test.save()
	#Will later need the below branching in order to get back to the right page
	if typeofpage == "h":
		return redirect("/hashtag/" + str(whatpage))
	elif typeofpage == "home":
		return redirect("/")
	else:
		return redirect("/profile/" + str(whatpage))

def delete(request, theEntry, typeofpage, whatpage):
	t = Entry.objects.filter(id=theEntry)
	thisEntry = t[0]
	thisEntry.delete()
	if typeofpage == "h":
		return redirect("/hashtag/" + str(whatpage))
	elif typeofpage == "home":
		return redirect("/")
	else:
		return redirect("/profile/" + str(whatpage))

def login_(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		print("Our first user: " + str(username) + " " +  str(password))
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("/")
	return render(request, 'login.html', {})

def signup(request):
	user = User.objects.create_user(username=request.POST['username'],
					email=request.POST['email'],
					password=request.POST['password'])
	login(request, user)
	return redirect("/")

def logout_(request):
	logout(request)
	return redirect("/login")

