from instance import OpenstackConnect

class openstack_network_operations(OpenstackConnect):
    def __init__(self):
        super().__init__()

    def list_networks(self):
        network = [net for net in self.conn.network.networks()]
        return network

    def create_network(self,net_name,net_description,is_shared=False,is_admi_state_up=True,subnet_name=None,subnet_cidr=None):
        print("Create network ")
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
            print("Failed to create network ",e)

    def create_router(self, router_name, external_network_id=None):
        print("Create Router ")
        try:
            # Create the router
            new_router = self.conn.network.create_router(
                name=router_name,
                external_gateway_info={"network_id": external_network_id} if external_network_id else None
            )
            print("New router created: {}".format(new_router))
        except Exception as e:
            print("Failed to create router ", e)

    def connect_nodes(self):
        pass


network_operations = openstack_network_operations()
#network_operations.create_network("Test_Vlan_22_444", "Descriereeee", subnet_name="subnet_19", subnet_cidr="10.0.0.0/24")
#network_operations.create_router("N")