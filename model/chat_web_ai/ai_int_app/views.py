import json
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
import spacy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = {
    "python", "java", "javascript", "react", "node.js", "aws", "azure", "gcp", "sql", "nosql",
    "docker", "kubernetes", "git", "api", "rest", "graphql", "frontend", "backend", "fullstack",
    "machine learning", "ai", "deep learning", "data science", "cloud", "agile", "scrum", "devops",
    "testing", "security", "linux", "windows", "mobile", "web", "database", "design patterns",
    "architecture", "communication", "teamwork", "problem solving", "leadership", "management",
    "analytical", "critical thinking", "collaboration", "mentoring", "debugging", "scalability",
    "performance", "optimization", "microservices", "ci/cd", "data structures", "algorithms", "oop"
}

POSITIVE_REMARKS = [
    "Great explanation!", "Excellent clarity!", "That's a strong answer!",
    "Well said!", "Impressive experience!", "You've demonstrated solid understanding!"
]


def extract_skills_from_jd(text):
    doc = nlp(text.lower())
    found = set()
    for token in doc:
        if token.text in SKILL_KEYWORDS:
            found.add(token.text)
    for chunk in doc.noun_chunks:
        if chunk.text.strip() in SKILL_KEYWORDS:
            found.add(chunk.text.strip())
    return sorted(found)

def generate_question(topic):
    templates = [
        f"Can you explain your experience with {topic}?",
        f"What challenges have you faced while working with {topic}?",
        f"How would you rate your proficiency in {topic} and why?",
        f"Can you share a project where you used {topic}?",
        f"What are some best practices you follow in {topic}?"
    ]
    return random.choice(templates)

def is_response_good(topic, response):
    keywords = topic.split()
    return all(word.lower() in response.lower() for word in keywords)

def provide_feedback(is_good):
    if is_good:
        return random.choice(POSITIVE_REMARKS)
    else:
        return "That's a good start! Consider including more specific details or examples."

@csrf_exempt
@require_POST
def interview_api(request):
    data = json.loads(request.body)
    jd_text = data.get("jd")
    user_response = data.get("response")
    topic = data.get("topic")

    # FIRST CALL: Get all topics
    if jd_text and not topic:
        skills = extract_skills_from_jd(jd_text)
        return JsonResponse({"topics": skills})

    # LATER CALLS: Ask or respond to each topic
    if topic and not user_response:
        question = generate_question(topic)
        return JsonResponse({"question": question})

    if topic and user_response:
        good = is_response_good(topic, user_response)
        feedback = provide_feedback(good)
        return JsonResponse({"feedback": feedback})

    return JsonResponse({"error": "Invalid input."}, status=400)


from django.shortcuts import render

def index(request):
    return render(request, "ai_int_app/index.html")

def personal_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        credentials = {
            'interview_01': '123@interview',
            'interview_02': '122@interview',
            'interview_03': '1222@interview',
            'interview_04': '12222@interview'
        }

        if credentials.get(username) == password:
            return redirect('interview_dashboard')
        else:
            return render(request, 'ai_int_app/branch_login.html', {'error': 'Invalid credentials'})

    return render(request, 'ai_int_app/branch_login.html')

def interview_dashboard(request):
    return render(request, "ai_int_app/index.html")