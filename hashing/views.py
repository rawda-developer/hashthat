from django.shortcuts import render, redirect, Http404
from .forms import HashForm
from .models import Hash
from django.http import JsonResponse
import hashlib
def home(request):
    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data['text']
            hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            try:
                Hash.objects.get(hash=hash)
            except Hash.DoesNotExist:
                hash_object = Hash(text=text, hash=hash)
                hash_object.save()
                return redirect('hash', hash=hash)
    form = HashForm()
    return render(request, 'hashing/home.html', {'form': form})


def hash(request, hash):
    try:
        hash_obj = Hash.objects.get(hash=hash)
        return render(request, 'hashing/hash.html', {'hash_obj': hash_obj})
    except Hash.DoesNotExist:
        raise Http404

def quickhash(request):
    text = request.GET['text']
    return JsonResponse({'hash': hashlib.sha256(text.encode('utf-8')).hexdigest()})