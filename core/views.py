from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Entry
from datetime import datetime

def splash(request):
	return render(request, "splash.html", {})

def journal_stats(request):
	return render(request, "journalstats.html", {})

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

