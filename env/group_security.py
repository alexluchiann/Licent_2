import openstack.network.v2.network

from networks_class import openstack_network_operations


class security_groups_operations(openstack_network_operations):
    def __init__(self):
        super().__init__()

    def list_all_security_groups(self):
        groups = [group for group in self.conn.network.security_groups()]
        return groups


    def delete_security_groups(self,security_group_name):

        security_group = self.conn.network.find_security_group(name_or_id=security_group_name)
        if security_group:
            self.conn.network.delete_security_group(security_group)
            print("Security group '{}' was deleted.".format(security_group_name))
        else:
            print("Security group '{}' not found.".format(security_group_name))


    def create_security_groups(self,name,description=None):
        for Name in self.list_all_security_groups():
            if Name.name == name:
                print(" The name {} is already used ".format(name))
                return

        security_group=self.conn.network.create_security_group(
            name=name,
            description=description
        )
        print(" Security Group {} was created ".format(name))
        return security_group

