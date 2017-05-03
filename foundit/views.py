from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.template import Context

from .models import Queuery

from rq import Queue
from worker import conn
from . import utils
from django.http import JsonResponse

from . import foundit
from . import graph

from collections import Counter

#subreddit=""
q = Queue(connection=conn)
#workercount=5#totalworkercount =workdercount+1, need one to schedule
title=""

workercount=5

def index(request):
	print("@@@@@@@@@@@@@START OF EVERYTHING@@@@@@@@@@@@")
	return render(request, 'foundit/index.html')

def loading(request):
	subreddit = request.GET["subreddit"]
	title = subreddit
	postLimit = request.GET["postLimit"]
	topComs = request.GET["topComs"]
	topReplies = request.GET["topReplies"]
	topWords = request.GET["topWords"]
	topUsers = request.GET["topUsers"]
	oldestPosts = request.GET["oldestPosts"]
	activePosts = request.GET["activePosts"]
	print("%%%%%%%%%%%STARTING SCHEDULING TEST%%%%%%%%%%%%%%%%")
<<<<<<< HEAD
	title=(str(subreddit))
	print("subreddit: "+title)
	job = q.enqueue(foundit.schedule,str(subreddit),int(postLimit),int(topComs),int(topReplies),int(topWords),int(topUsers),int(oldestPosts),int(activePosts), int(wc) timeout=200)
=======
	job = q.enqueue(foundit.schedule,str(subreddit),int(postLimit),int(topComs),int(topReplies),int(topWords),int(topUsers),int(oldestPosts),int(activePosts), timeout=200)
>>>>>>> 2c761673c61bf88828a40bc4801268b466cb1c70
	print("OUT OF SCHEDULER")

	t = loader.get_template('foundit/loading.html')
	c = Context({ 'jobid': job.id , 'subreddit':subreddit})
	return HttpResponse(t.render(c))

def checkJob(request):
	jobid = request.GET['jobid']
	results = q.fetch_job(jobid).result
	if(results):
		return HttpResponse(jobid)
	else:
		return HttpResponse(results)

def testResults(request):
	return HttpResponse("results!")

def results(request):  
	jobid = request.GET['jobid']
	WorkerJobids = q.fetch_job(jobid).result
	WorkerResults = []
	for jid in WorkerJobids:
		WorkerResults.append(q.fetch_job(jid).result)
		
	results = WorkerResults[0]

	topicWordList = results[0]
	topWordList = results[1]
	topUserList = results[2]
	topComList = results[3]
	topRepliesList = results[4]
	oldestPostList = results[5]
	activePostList = results[6]
	postAnalyzed = results[7]
#	avgLengthTop = results[3]
	avgLengthAll = results[8]
	commentsAnalyzed = results[9]
	subreddit = results[10]

#	subreddit=results[9]
	#supportWordList = allList[9]

	#compile graph for topWords
	topWordCounts = [x[1] for x in topWordList]
	topWords = [x[0] for x in topWordList]
	topWordsData = (topWordCounts, "Top Words", "Occurances", topWords)
	topWordsGraph = graph.renderGraph(topWordsData)

	#compile graph for topUsers
	topUserCounts = [x[1] for x in topUserList]
	topUsers = [x[0] for x in topUserList]
	topUsersData = (topUserCounts, "Top Users", "Activity", topUsers)
	topUsersGraph = graph.renderGraph(topUsersData)

	#LUKES TEST GRAPHS

	#Topic Words Graph
	topicWordCounts = [x[1] for x in topicWordList]
	topicWords = [x[0] for x in topicWordList]
	topicWordsData = (topicWordCounts, "Topic Words", "Occurances", topicWords)
	topicWordsGraph = graph.renderGraph(topicWordsData)  

	#data=(topicWordList, supportWordList)
	#supportWordsGraph = graph.urenderGraph(data)

	t = loader.get_template('foundit/results.html')
	c = Context({ 'subreddit': subreddit, 'topComList' : topComList, 'topWordsGraph' : topWordsGraph, 'topUsersGraph' : topUsersGraph, 'topicWordsGraph' : topicWordsGraph,}) #'supportWordsGraph' : supportWordsGraph})
	return HttpResponse(t.render(c))