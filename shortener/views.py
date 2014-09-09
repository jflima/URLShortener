from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from models import ShortenedLink, User
import random, re

# Create your views here.

logged = False

def home(request):
    if logged:
        return render(request,'shortener/index.html')
    else:
        return render(request,'shortener/login.html')

def logout(request):
    global logged
    logged = False
#    template = loader.get_template('shortener/login.html')
    
#    context = RequestContext(request,)
    #return HttpResponse(template.render(context))
    return HttpResponseRedirect(reverse('shortener:home'))
    #return render(request,'shortener/login.html')

def shorten(request):
    
    new_key = generate_key()
    print new_key
    
    olink = request.POST['link']
    
    if re.match('(https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+.*', olink) != None:
        s = ShortenedLink(identifier = new_key, original_link = olink)
        s.save()
    
        template = loader.get_template('shortener/shortened.html')
        context = RequestContext(request, {
                                           'shortenedlink':s
                                           })
        return HttpResponse(template.render(context))
    else:
        
        template = loader.get_template('shortener/index.html')
        context = RequestContext(request,{
                                         'message':'Insira uma URL valida!'
                                         })
        return HttpResponse(template.render(context))
        #return HttpResponseRedirect(reverse('shortener:home'),{
        #                                 'message':'Insira uma URL valida!'
        #                                })
    
    
    

def generate_key():
    keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    result_key = ""
    for i in range(10):
        result_key += keys[random.randint(0,35)]
    
    return result_key

def redirect(request, actual_identifier):
    actual_link = ShortenedLink.objects.filter(identifier = actual_identifier)
    return HttpResponseRedirect(actual_link[0].original_link)

def make_login(request):
    try:
        u = User.objects.get(email=request.POST['emailh'], password=request.POST['passwordh'])
        template = loader.get_template('shortener/index.html')
        context = RequestContext(request, {
                                           'user': u
                                           })
        global logged
        logged = True
        return HttpResponse(template.render(context))
    except User.DoesNotExist:
        template = loader.get_template('shortener/login.html')
        context = RequestContext(request, {'message':'Erro de login'})
        return HttpResponse(template.render(context))

def register(request):
    template = loader.get_template('shortener/register.html')
    
    context = RequestContext(request,)
    return HttpResponse(template.render(context))

# Realiza o cadastro.
def make_register(request):
        try:
            post_password = request.POST['password']
            post_confirm = request.POST['password_confirm']
            post_name=request.POST['name']
            post_email=request.POST['email']
            
            # Testa se as senhas correspodnem 
            if post_password != post_confirm:
                template = loader.get_template('shortener/register.html')
                context = RequestContext(request,{
                                              'message':"As senhas nao correspondem!"
                                              })
                return HttpResponse(template.render(context))
            
            if post_password == "" or post_confirm == "" or post_name == "" or post_email == "":
                template = loader.get_template('shortener/register.html')
                context = RequestContext(request,{
                                              'message':"Preencha os campos!"
                                              })
                return HttpResponse(template.render(context))
            
            u = User(email=post_email, password=post_password, name=post_name)
            u.save()
            
            template = loader.get_template('shortener/login.html')
            context = RequestContext(request,{
                                              'message':"Cadastro realizado com sucesso!"
                                              })
            
            return HttpResponse(template.render(context))
        except:
            # Carrega uma mensagem de erro caso ocorra alguma falha no cadastro.
            
            template = loader.get_template('shortener/register.html')
            context = RequestContext(request,{
                                              'message':"Nao foi possivel realizar o cadastro!"
                                              })
            return HttpResponse(template.render(context))