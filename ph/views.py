from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from posts.models import BlogPost
from django.db.models import Q

def index(request):
	blogposts = BlogPost.objects.all().order_by("-create_date")
	tags = []

	for blogpost in blogposts:
		currTags = blogpost.tags.all()
		for currTag in currTags:
			tags.append(currTag)

	bptop = BlogPost.objects.all().order_by("likes")

	return render(request, 'index.html', {"blogposts" : blogposts, "tags": tags, "top" : bptop})

def search_results(request):
	if request.method == "POST":
		query = request.POST['query']
		query_list = query.split(' ')

		bp = BlogPost.objects.all()
		ppl = User.objects.all()

		## for blogpost query
		query_object = Q(content__icontains=query_list[0]) | Q(title__icontains=query_list[0])

		for query in query_list[1:]:
			query_object.add( (Q(content__icontains=query) | Q(title__icontains=query)), query_object.connector )

		blogposts = bp.filter(query_object).order_by("-likes")

		## for users query
		query_object = Q(first_name__icontains=query_list[0]) | Q(last_name__icontains=query_list[0]) | Q(username__icontains=query_list[0])

		for query in query_list[1:]:
			query_object.add( (Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)), query_object.connector )

		people = ppl.filter(query_object)

		######### for tags ##########
		bptags = BlogPost.objects.all().order_by("-create_date")
		tags = []

		query_object = Q(name__icontains=query_list[0])

		for query in query_list[1:]:
			query_object.add(Q(tags__name__icontains=query))

		for bptag in bptags:
			currTags = bptag.tags.all()
			currTags = currTags.filter(query_object)
			for currTag in currTags:
				tags.append(currTag)

		print tags
		######### for tags ##########

	# people = User.objects.all()
	# blogposts = BlogPost.objects.all().order_by("-create_date")
		return render(request, 'search-results.html', {"people": people, "blogposts" : blogposts, "tags": tags})

def search_from_tags(request, tags):
	query_list = tags.split(' ')

	bp = BlogPost.objects.all()
	ppl = User.objects.all()

	## for blogpost query
	query_object = Q(content__icontains=query_list[0]) | Q(title__icontains=query_list[0])

	for query in query_list[1:]:
		query_object.add( (Q(content__icontains=query) | Q(title__icontains=query)), query_object.connector )

	blogposts = bp.filter(query_object).order_by("-likes")

	## for users query
	query_object = Q(first_name__icontains=query_list[0]) | Q(last_name__icontains=query_list[0]) | Q(username__icontains=query_list[0])

	for query in query_list[1:]:
		query_object.add( (Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)), query_object.connector )

	people = ppl.filter(query_object)

	######### for tags ##########
	bptags = BlogPost.objects.all().order_by("-create_date")
	tags = []

	query_object = Q(name__icontains=query_list[0])

	for query in query_list[1:]:
		query_object.add(Q(name__icontains=query))

	for bptag in bptags:
		currTags = bptag.tags.all()
		currTags = currTags.filter(query_object)
		for currTag in currTags:
			tags.append(currTag)

	print tags
	######### for tags ##########

# people = User.objects.all()
# blogposts = BlogPost.objects.all().order_by("-create_date")
	return render(request, 'search-results-tags.html', {"people": people, "blogposts" : blogposts, "tags": tags})