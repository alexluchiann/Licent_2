import openstack


class OpenstackConnect:
    def __init__(self):
        self.conn = openstack.connect(cloud='openstack')
        self.network = self.conn.network.find_network('licenta-alex')
        self.keypair = 'licenta'
        self.list_images=list(self.conn.image.images())
        self.list_flavors=list(self.conn.list_flavors())
        ####
        server = self.conn.compute.find_server('Test_2')
        metadata = server.metadata
        print(self.conn.compute.find_server('Test_2'))

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


    def Add_vm(self, name, flavor_id, image_id):

        list_VM = self.List_All_VM()
        for Vm in list_VM:
            if Vm.name == name:
                print("The name already exists")
                return

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


#app = OpenstackConnect()
#print(app.get_dictionary_of_iamges())
