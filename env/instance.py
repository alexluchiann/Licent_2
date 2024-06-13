import openstack


class OpenstackConnect:
    def __init__(self):

        self.conn = openstack.connect(cloud='openstack')

        self.keypair = 'licenta'
        self.list_images = list(self.conn.image.images())
        self.list_flavors = list(self.conn.list_flavors())
        self.list_networks = list(self.conn.network.networks())

    def list_All_VM(self):
        list_VM = [VM_Info for VM_Info in self.conn.compute.servers()]
        return list_VM

    def number_of_vm(self):
        numb=0
        for i in self.list_All_VM():
            numb=numb+1
        return numb

    def delete_VM(self, name_VM):
        try:
            targ = self.conn.compute.find_server(name_VM)
            self.conn.compute.delete_server(targ, ignore_missing=True)
            print("Deleted {} instance ".format(name_VM))
        except Exception as e:
            print(" Instance {} doesen't exist".format(name_VM))

    def add_node(self, name, flavor_id, image_id, network_name, description=None):
        list_VM = self.list_All_VM()
        existing_names = {vm.name for vm in list_VM}
        network = None

        for net in self.list_networks:
            if net.name == network_name:
                network = net
                break

        if network is None:
            print("Network does not exist")
            return

        def generate_new_name(base_name):
            suffix = 1
            new_name = f"{base_name}_{suffix}"
            while new_name in existing_names:
                suffix += 1
                new_name = f"{base_name}_{suffix}"
            return new_name

        if name in existing_names:
            name = generate_new_name(name)

        try:
            print(network.name)
            server = self.conn.compute.create_server(
                name=name,
                flavor_id=self.conn.compute.find_flavor(flavor_id).id,
                image_id=self.conn.image.find_image(image_id).id,
                networks=[{"uuid": network.id}],
                key_name=self.keypair,
                security_groups=[{"name": "default"}],
                description=description
            )
            print(f"Name of the server is {name}")

        except Exception as e:
            print("An error occurred while creating the server", e)


    def create_floating_ip(self, network_name):
        try:
            network = None
            for net in self.list_networks:
                if net.name == network_name:
                    network = net
                    break

            if network is None:
                print("Network {} not found".format(network_name))
                return

            floating_ip = self.conn.network.create_ip(floating_network_id=network.id)
            print("Floating IP {} created for network {}".format(floating_ip.floating_ip_address, network_name))
            return floating_ip
        except Exception as e:
            print("Failed to create floating IP:", e)

    #
    #   NU merge / NU stiu cum sa fac /
    #
    def associate_floating_ip_(self, instance_name):

        instance = None
        for inst in self.list_All_VM():
            if inst.name == instance_name:
                instance = inst
                break
        print(inst.name)

        ip_avabil=self.conn.network.find_available_ip()
        print("The avalibele network is {} ".format(ip_avabil))

    def get_image_update_date(self, image_name):
        image = self.conn.image.find_image(image_name)
        if image:
            return image.updated_at
        else:
            return "Image not found"

    def list_floating_ips(self):
        floatin_ips=[]
        floating_ips = self.conn.network.ips()
        for ips in floating_ips:
            print(str(ips.floating_ip_address) + "      " + str(ips.fixed_ip_address))
            floatin_ips.append(ips.floating_ip_address)
        return floatin_ips

