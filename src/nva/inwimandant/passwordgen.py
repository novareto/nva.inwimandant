import random

def gen_password():
    large = ['A','B','C','D','E','F','G','H','K','L','M','N','P','Q','R','S','T','U','V''W','X','Y','Z']
    small = ['a','b','c','d','e','f','g','h','i','j','k','m','n','r','s','t','u','v','w','x','y','z']
    numbers = ['1','2','3','4','5','6','7','8','9']
    extra = ['§','$','(',')','#','+','!','.','{','}','[',']']
    
    vorauswahl = [small, small, small, small, small, large, numbers, extra]
    random.shuffle(vorauswahl)
    password = u""
    for i in vorauswahl:
        password += random.choice(i)
    return password
