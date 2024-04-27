import openstack


class OpenstackConnect:
    def __init__(self):

        self.conn = openstack.connect(cloud='openstack')

        self.keypair = 'licenta'
        self.list_images=list(self.conn.image.images())
        self.list_flavors=list(self.conn.list_flavors())
        self.list_networks=self.conn.network.networks()



    def list_All_VM(self):
        list_VM = [VM_Info for VM_Info in self.conn.compute.servers()]
        return list_VM

    def delete_VM(self, name_VM):
        try:
            targ = self.conn.compute.find_server(name_VM)
            self.conn.compute.delete_server(targ, ignore_missing=True)
            print("Deleted {} instance ".format(name_VM))
        except Exception as e:
            print(" Instance {} doesen't exist".format(name_VM))


    def add_node(self, name, flavor_id, image_id,network_name):

        list_VM = self.list_All_VM()
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
                key_name=self.keypair,
                security_groups = [{"name": "default"}]
            )
           print(" Name of the server is {} ".format(name))

        except Exception as e:
            print(" An error ocurred wile creting the server", e)


    def create_floating_ip(self):
        pass
    def associate_floating_ip(self, server_name, floating_ip_address=None, network_id=None):
        try:
            server=None
            for node in self.list_All_VM():
                if node.name == server_name:
                    server=node
                    break


            server = self.conn.compute.find_server(server_name)
            print("Server is {}".format(server.name))

            print("Floating IP {} associated with server {}".format(server.fixed_ip_address, server_name))
        except Exception as e:
            print("Error:", e)


    def list_floating_ips(self):

        floating_ips=self.conn.network.ips()
        for ips in floating_ips:
            print(str(ips.floating_ip_address) + "      " + str(ips.fixed_ip_address))

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



app =OpenstackConnect()
#app.add_node("Notesss_testsss","m1.small","CentOS 7","licenta")


#app.add_node("Test_2","m1.small","Ubuntu Jammy","licenta")
#app.associate_floating_ip("Notesss_testsss","10.0.0.62")
#app.associate_floating_ip("Notesss_testsss")
#app.associate_floating_ip("VM_111122222", "10.0.0.62", "ab451886-9a75-45f8-be57-33b2e4bbe11e")
#app.add_node("Alexx_DevOps_engenir_Top_G","m1.small","Ubuntu Jammy","licenta-alex")
#app.list_floating_ips("Alexx_DevOps_engenir_Top_G")
print("_____________________________________________________")
#app.associate_floating_ip("Alexx_DevOps_engenir_Top_G")
#for i in app.list_All_VM():
#   print(i)
#print(app.get_dictionary_of_iamges())
#print("________________________________________________________________________________________")
#app.create_network("Test_Vlan_22","Descriereeee",subnet_name="subnet_19",subnet_cidr="10.0.0.0/24")
#app.create_router("N")
#print("________________________________________________________________________________________")
#for i in app.list_networks():
    #print(str(i) + '\n')
#2ded1ced-c0bb-4ba3-bcfe-98021a27f281': 'Ubuntu Jammy'