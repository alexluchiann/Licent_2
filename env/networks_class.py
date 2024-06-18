from instance import OpenstackConnect

class openstack_network_operations(OpenstackConnect):
    def __init__(self):
        super().__init__()

        self.network_list = list(self.conn.network.networks())
    def create_network(self,net_name,net_description,is_shared=False,is_admi_state_up=True,subnet_name=None,subnet_cidr=None):
        #
        try:
            new_network = self.conn.network.create_network(
                name=net_name,
                description = net_description,
                shared=is_shared,
                admin_state_up=is_admi_state_up
            )
            print("New network created: {}".format(new_network))

            if subnet_name and subnet_cidr:
                subnet = self.conn.network.create_subnet(
                    network_id=new_network.id,
                    name=subnet_name,
                    cidr=subnet_cidr,
                    ip_version=4
                )
                print("Subnet created: ",subnet)


        except Exception as e:
            print ("Failed to create network ",e)


    def delete_network(self,network_name):
        target_network=None
        for net in self.network_list:
            if net.name == network_name:
                target_network=net
                break
        print("_____  Checkpoint for delete network _____")
        if target_network:
            try:
                print("_____  Checkpoint  2  for delete network _____")
                self.conn.network.delete_network(target_network)
                print("The network {} was deleted ".format(target_network))
            except:
                print("An error had occurred ")
        else:
            print("It didn't find the network")



    def list_external_netwroks(self):
        external_networks = []
        for network in self.network_list:
            if network.is_router_external:
                external_networks.append(network)
        return external_networks


    def list_routers(self):
         router=[rout for rout in self.conn.network.routers()]
         return router

    def create_router(self, router_name, external_network_id=None):
        for i in self.list_routers():
            if i.name == router_name:
                print("The name {} is already used ".format(router_name))
                return

        try:
            if external_network_id:
                new_router = self.conn.network.create_router(
                name = router_name,
                external_gateway_info={"network_id": external_network_id}
                )
            else:
                new_router = self.conn.network.create_router(
                 name=router_name
                 )

            print("New router created: {}".format(new_router))
        except Exception as e:
            print("Failed to create router ", e)
        print("Create Router ")

    def delete_router(self,router_name):
        target_router=None
        for net in self.conn.list_routers():
            if net.name == router_name:
                target_router = net
                break

        try:
            self.conn.network.delete_router(target_router)
            print(" The router {} was deleted ".format(target_router))
        except Exception as e:
            print(" An error has occourred in delete_router function")


    def connect_router_to_network(self,router_name,network_name):
        router = None
        network = None

        # Find the router
        for rout in self.list_routers():
            if rout.name == router_name:
                router = rout
                break

        # Find the network
        for net in self.network_list:
            if net.name == network_name:
                network = net
                break

        if router and network:
            try:
                # Get subnets associated with the network
                subnets = self.conn.network.subnets(network_id=network.id)
                if subnets:
                    # Get the ID of the first subnet
                    subnet_id = next(subnets).id
                    # Connect the router to the network
                    self.conn.network.add_interface_to_router(router, subnet_id=subnet_id)
                    print("Router '{}' was connected to the '{}' network.".format(router_name, network_name))
                else:
                    print("No subnets found for network '{}'.".format(network_name))
            except Exception as e:
                print("Failed to connect router to network:", e)
        else:
            print("Router '{}' or network '{}' not found.".format(router_name, network_name))


    def disconect_router_from_network(self,router_name,network_name):
        router = None
        network = None

        for rout in self.list_routers():
            if rout.name == router_name:
                router = rout
                break

        for net in self.network_list:
            if net.name == network_name:
                network = net
                break

        if router and network:
            try:
                # Get subnets associated with the network
                subnets = self.conn.network.subnets(network_id=network.id)
                if subnets:
                    # Get the ID of the first subnet
                    subnet_id = next(subnets).id
                    # Disconnect the router from the network
                    self.conn.network.remove_interface_from_router(router, subnet_id=subnet_id)
                    print("Router '{}' was disconnected from the '{}' network.".format(router_name, network_name))
                else:
                    print("No subnets found for network '{}'.".format(network_name))
            except Exception as e:
                print("Failed to disconnect router from network:", e)
        else:
            print("Router '{}' or network '{}' not found.".format(router_name, network_name))

