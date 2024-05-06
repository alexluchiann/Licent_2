from ansible_playbooks.ansible_management import ansible_management


print("___________________________________________________________________-")
app = ansible_management()
nodes=[]
for nod in app.list_All_VM():
    print(nod.image)
