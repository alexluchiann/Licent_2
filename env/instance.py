import openstack


class OpenstackConnect:
    def __init__(self):
        self.conn = openstack.connect(cloud='openstack')
        self.network = self.conn.network.find_network('licenta-alex')
        self.keypair = 'licenta'
        self.list_images=self.conn.image.images()
        self.list_flavors=self.conn.list_flavors()
        server = self.conn.compute.find_server('Test_2')
        metadata = server.metadata

    def List_All_VM(self):
        for i in self.conn.list_flavors():
            print(i)
        #list_VM = [VM_Info for VM_Info in self.conn.compute.servers()]
        #eturn list_VM

    def Delete_VM(self, name_VM):
        try:
            targ = self.conn.compute.find_server(name_VM)
            self.conn.compute.delete_server(targ, ignore_missing=True)
            print("Deleted {} instance ".format(name_VM))
        except Exception as e:
            print(" Instance {} doesen't exist".format(name_VM))


    def Add_vm(self, name, flavor_id, image_id):

        list_VM = self.List_All_VM()
        for Vm in list_VM:
            if Vm.name == name:
                print("The name already exists")
                return
#AAAAAAAAAAAAAAAA
        try:
            server = self.conn.compute.create_server(
                name=name,
                flavor_id=self.conn.compute.find_flavor(flavor_id).id,
                image_id=self.conn.image.find_image(image_id).id,
                networks=[{"uuid": self.network.id}],
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
app.List_All_VM()
#print(app.get_dictionary_of_iamges())
#print("________________________________________________________________________________________")
#app.create_network("Test_Vlan_22","Descriereeee",subnet_name="subnet_19",subnet_cidr="10.0.0.0/24")
#app.create_router("N")
#print("________________________________________________________________________________________")
#for i in app.list_networks():
    #print(str(i) + '\n')
#2ded1ced-c0bb-4ba3-bcfe-98021a27f281': 'Ubuntu Jammy'