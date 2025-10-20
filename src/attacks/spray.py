def create_namelist():
    pass

def create_pwlist():
    pass

def load_wordlists():
    pass

def ssh_spray(usernames,passwords):
    for un in usernames:
        for pw in passwords:
            print(f"{un}:{pw}")

def http_spray(usernames,passwords):
    pass

def smb_spray(usernames,passwords):
    pass

'''
I wonder if it makes more sense to combine all spray attacks into a single function that has an additional arg that accepts the protocol?
'''
