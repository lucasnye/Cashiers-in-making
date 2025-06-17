from django.shortcuts import render

def index(request):
    return render(request, "edtech/index.html")
def real_time_transcription(request):
    return render(request, "edtech/rtt.html")
