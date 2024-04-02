from instance import OpenstackConnect

class openstack_network_operations(OpenstackConnect):
    def __init__(self):
        super().__init__()

    def list_networks(self):
        network = [net for net in self.conn.network.networks()]
        return network

    def create_network(self,net_name,net_description,is_shared=False,is_admi_state_up=True,subnet_name=None,subnet_cidr=None):
        print("Create network ")
        for network in self.list_networks():
            if network.name == net_name:
                print("The name Already exists ,pick another one ")
                return
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


    def create_router(self, router_name, external_network_id=None):
        print("Create Router ")

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

    def connect_router_to_network(self,router_id,network_id):
        self.conn.network.add_gateway(router_id, network_id)


    def list_routers(self):
         router=[rout for rout in self.conn.network.routers()]
         return router


network_operations = openstack_network_operations()
