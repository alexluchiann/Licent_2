import openstack
import subprocess
class OpenstackConnect:
    def __init__(self):

        self.conn = openstack.connect(cloud='openstack')

        self.keypair = 'licenta_2'
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

        flavor = self.conn.compute.find_flavor(flavor_id)
        if flavor is None:
            print(f"Flavor '{flavor_id}' not found")
            return

        image = self.conn.image.find_image(image_id)
        if image is None:
            print(f"Image '{image_id}' not found")
            return

        try:
            server = self.conn.compute.create_server(
                name=name,
                flavor_id=flavor.id,
                image_id=image.id,
                networks=[{"uuid": network.id}],
                key_name=self.keypair,
                security_groups=[{"name": "default"}],
                description=description
            )
            print(f"Server '{name}' created successfully")

        except Exception as e:
            print("An error occurred while creating the server:", e)

    def create_floating_ip(self, network_name='public'):
        try:
            network = next((net for net in self.conn.network.networks()
                            if net.name == network_name and net.is_router_external),None)
            print(network.name)

            if network is None:
                print(f"Network {network_name} not found or is not an external network")
                return None

            floating_ip = self.conn.network.create_ip(floating_network_id=network.id)
            print(f"Floating IP {floating_ip.floating_ip_address} created for network {network_name}")
            return floating_ip
        except Exception as e:
            print("Failed to create floating IP:", e)
            return None

    def associate_floating_ip(self, instance_name):
        instance = next((server for server in self.conn.compute.servers() if server.name == instance_name), None)

        if not instance:
            print(f"Instance {instance_name} not found")
            return None

        floating_ip = next((ip for ip in self.conn.network.ips() if not ip.fixed_ip_address), None)
        if not floating_ip:
            floating_ip = self.create_floating_ip()
            if not floating_ip:
                print("Failed to create or find a floating IP")
                return

        rc_file_path = "/home/alex/Licenta_2024/OpenStack_v2/app-cred-licenta-openrc\\(3\\).sh"
        command = f"source {rc_file_path} && openstack server add floating ip {instance.id} {floating_ip.floating_ip_address}"

        try:
            result = subprocess.run(command, shell=True, check=True, text=True, executable="/bin/bash")
            print(f"Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while associating the floating IP: {e.stderr}")

    def get_image_update_date(self, image_name):
        image = self.conn.image.find_image(image_name)
        if image:
            return image.updated_at
        else:
            return "Image not found"

    def list_floating_ips(self):
        floating_ips = []
        for ip in self.conn.network.ips():
            print(str(ip.floating_ip_address))
            floating_ips.append(ip.floating_ip_address)
        return floating_ips


app = OpenstackConnect()
app.associate_floating_ip('ipipip_1-2')
