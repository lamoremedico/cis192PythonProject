from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Entry
from datetime import datetime
from core.sentiment_analysis import *
import pandas
from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import Scatter, Figure, Layout, Pie

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

def piecharts(request):
	allEntries = Entry.objects.all()
	seasons = split_by_season(allEntries)
	seasons_name = ["spring", "fall", "winter", "summer", "current month"]
	labels = ["negative", "neutral", "positive"]
	chart_list = []
	for i in range(len(seasons)):
		if (seasons[i][0] != 0):
			data = [Pie(labels=labels, values=seasons[i])]
			layout = Layout(title=seasons_name[i])
			chart_list.append(plot(dict(data=data, layout=layout), output_type='div'))
	times = split_by_time(allEntries)
	times_name = ["morning", "afternoon", "evening", "night"]
	for i in range(len(times)):
		if (times[i][0] != 0):
			data = [Pie(labels=labels, values=times[i])]
			layout = Layout(title=times_name[i])
			chart_list.append(plot(dict(data=data, layout=layout), output_type='div'))
	days = split_by_day(allEntries)
	days_name = ["weekday", "weekend"]
	for i in range(len(days)):
		if (days[i][0] != 0):
			data = [Pie(labels=labels, values=days[i])]
			layout = Layout(title=days_name[i])
			chart_list.append(plot(dict(data=data, layout=layout), output_type='div'))
	averages = create_avgs(allEntries)
	return render(request, "piecharts.html", {"all_charts": chart_list})

def homeredirect(request):
	return redirect('/0')

def home(request, typeDeleted):
	if not request.user.is_authenticated:
		return redirect('/login')

	#0, 1, 2, 3, 4 correspond to all, upbeat, peaceful, somber, and tense respectively
	whichTab = 0
	if request.method == "POST":
		newJournalEntry = request.POST["Entry"]
		newCategory = request.POST["Category"]
		if newCategory == "Upbeat":
			whichTab = 1
		elif newCategory == "Peaceful":
			whichTab = 2
		elif newCategory == "Somber":
			whichTab = 3
		elif newCategory == "Tense":
			whichTab = 4
		entryObj = Entry.objects.create(text=newJournalEntry, categories=newCategory, created_by=request.user, created_at=datetime.now())
	elif typeDeleted is not None:
		whichTab = int(typeDeleted)

	allEntries = Entry.objects.all().order_by('-isPinned', '-created_at')
	upbeatEntries = allEntries.filter(categories="Upbeat")
	peacefulEntries = allEntries.filter(categories="Peaceful")
	somberEntries = allEntries.filter(categories="Somber")
	tenseEntries = allEntries.filter(categories="Tense")

	return render(request, "home.html", {"entries": allEntries, "whichTab": whichTab, "upbeatEntries": upbeatEntries, "peacefulEntries": peacefulEntries, "somberEntries": somberEntries, "tenseEntries": tenseEntries})

def favorite(request, theEntry, whichT):
	test = Entry.objects.get(id=theEntry)
	test.isFavorited = not test.isFavorited
	test.save()

	whichTab = int(whichT)

	return redirect("/" + str(whichTab))

def pin(request, theEntry, whichT):
	test = Entry.objects.get(id=theEntry)
	test.isPinned = not test.isPinned
	test.save()

	whichTab = int(whichT)
	return redirect("/" + str(whichTab))

def delete(request, theEntry, whichT):
	t = Entry.objects.filter(id=theEntry)
	thisEntry = t[0]
	whichTab = int(whichT)
	
	thisEntry.delete()
	return redirect("/" + str(whichTab))

def login_(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		print("Our first user: " + str(username) + " " +  str(password))
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("/0")
	return render(request, 'login.html', {})

def signup(request):
	user = User.objects.create_user(username=request.POST['username'],
					email=request.POST['email'],
					password=request.POST['password'])
	login(request, user)
	return redirect("/0")

def logout_(request):
	logout(request)
	return redirect("/login")

