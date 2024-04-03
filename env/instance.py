import openstack


class OpenstackConnect:
    def __init__(self):

        self.conn = openstack.connect(cloud='openstack')

        self.keypair = 'licenta'
        self.list_images=list(self.conn.image.images())
        self.list_flavors=list(self.conn.list_flavors())
        self.list_networks=self.conn.network.networks()



    def List_All_VM(self):
        list_VM = [VM_Info for VM_Info in self.conn.compute.servers()]
        return list_VM

    def Delete_VM(self, name_VM):
        try:
            targ = self.conn.compute.find_server(name_VM)
            self.conn.compute.delete_server(targ, ignore_missing=True)
            print("Deleted {} instance ".format(name_VM))
        except Exception as e:
            print(" Instance {} doesen't exist".format(name_VM))


    def Add_vm(self, name, flavor_id, image_id,network_name):

        list_VM = self.List_All_VM()
        network = None
        for VM in list_VM:
            if VM.name == name:
                print(" The name is already used ")
                return

        for net in self.list_networks:
            if net.name == network_name:
                network=net
                break

        if network is None:
            print("Nu exista netwrokul dat")
            return

        try:
           print(network.name)
           server = self.conn.compute.create_server(
                name=name,
                flavor_id=self.conn.compute.find_flavor(flavor_id).id,
                image_id=self.conn.image.find_image(image_id).id,
                networks=[{"uuid": network.id}],
                key_name=self.keypair
            )
           print(" Name of the server id {} ".format(name))
        except Exception as e:
            print(e)

    def get_dictionary_of_iamges(self):
        dict_images={}
        for image in self.list_images:
            dict_images[image.id] = image.name
        return dict_images

    def get_dictionary_of_flavors(self):
        dict_flavors={}
        for image in self.list_images:
            dict_flavors[image.id] = image.list_flavors
        return dict_flavors



app = OpenstackConnect()
#app.Add_vm("VM_1","m1.small","CentOS 7","Test_Vlan_22_444")
#app.Add_vm("Alexx_Gunoi","m1.small","Ubuntu Jammy")
#for i in app.List_All_VM():
#   print(i)
#print(app.get_dictionary_of_iamges())
#print("________________________________________________________________________________________")
#app.create_network("Test_Vlan_22","Descriereeee",subnet_name="subnet_19",subnet_cidr="10.0.0.0/24")
#app.create_router("N")
#print("________________________________________________________________________________________")
#for i in app.list_networks():
    #print(str(i) + '\n')
#2ded1ced-c0bb-4ba3-bcfe-98021a27f281': 'Ubuntu Jammy'