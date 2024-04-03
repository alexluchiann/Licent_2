import openstack.network.v2.network

from networks_class import openstack_network_operations


class security_groups_operations(openstack_network_operations):
    def __init__(self):
        super().__init__()

    def list_all_security_groups(self):
        groups = [group for group in self.conn.network.security_groups()]
        return groups



app = security_groups_operations()
