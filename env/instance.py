import openstack
import subprocess
from PyQt5.QtWidgets import QMessageBox

class OpenstackConnect:
    def __init__(self):
        self.conn = openstack.connect(cloud='openstack')
        self.keypair = 'licenta_2'
        self.list_images = list(self.conn.image.images())
        self.list_networks = list(self.conn.network.networks())

    def list_All_VM(self):
        return [VM_Info for VM_Info in self.conn.compute.servers()]

    def number_of_vm(self):
        return len(self.list_All_VM())

    def delete_VM(self, name_VM):
        try:
            targ = self.conn.compute.find_server(name_VM)
            self.conn.compute.delete_server(targ, ignore_missing=True)
            print(f"Deleted {name_VM} instance")
        except Exception as e:
            print(f"Instance {name_VM} doesn't exist: {e}")

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
            return None

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
            return None

        image = self.conn.image.find_image(image_id)
        if image is None:
            print(f"Image '{image_id}' not found")
            return None

        try:
            server = self.conn.compute.create_server(
                name=name,
                flavor_id=flavor.id,
                image_id=image.id,
                networks=[{"uuid": network.id}],
                key_name=self.keypair,
                security_groups=[{"name": "default"}],
                description=description,

            )
            self.conn.compute.wait_for_server(server)
            print(f"Server '{name}' created successfully")
            return server
        except Exception as e:
            print(f"An error occurred while creating the server: {e}")
            return None

    def create_floating_ip(self, network_name='public'):
        try:
            network = next((net for net in self.conn.network.networks()
                            if net.name == network_name and net.is_router_external), None)

            if network is None:
                print(f"Network {network_name} not found or is not an external network")
                return None

            floating_ip = self.conn.network.create_ip(floating_network_id=network.id)
            print(f"Floating IP {floating_ip.floating_ip_address} created for network {network_name}")
            return floating_ip
        except Exception as e:
            print(f"Failed to create floating IP: {e}")
            return None

    def associate_floating_ip(self, instance):
        instance_name = instance.name
        instance = next((server for server in self.conn.compute.servers() if server.name == instance_name), None)

        if not instance:
            print(f"Instance {instance_name} not found")
            return None

        private_ip = None
        for network_name, addresses in instance.addresses.items():
            for address in addresses:
                if address['OS-EXT-IPS:type'] == 'fixed':
                    private_ip = address['addr']
                    break
            if private_ip:
                break

        if not private_ip:
            print(f"Instance {instance_name} does not have a private IP address.")
            return None

        existing_floating_ip = None
        for ip in self.conn.network.ips():
            if ip.fixed_ip_address == private_ip:
                existing_floating_ip = ip
                break

        if existing_floating_ip:
            print(f"Instance {instance_name} already has a floating IP: {existing_floating_ip.floating_ip_address}")
            return existing_floating_ip.floating_ip_address

        floating_ip = self.create_floating_ip()
        if not floating_ip:
            print("Failed to create or find a floating IP")
            return None

        rc_file_path = "/home/alex/Licenta_2024/OpenStack_v2/app-cred-licenta-openrc\\(3\\).sh"
        command = f"source {rc_file_path} && openstack server add floating ip {instance.id} {floating_ip.floating_ip_address}"

        try:
            result = subprocess.run(command, shell=True, check=True, text=True, executable="/bin/bash")
            print(f"Output: {result.stdout}")
            return floating_ip.floating_ip_address
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while associating the floating IP: {e.stderr}")
            return None

    def get_image_update_date(self, image_name):
        image = self.conn.image.find_image(image_name)
        if image:
            return image.updated_at
        else:
            return "Image not found"

    def list_floating_ips(self):
        floating_ips = [ip.floating_ip_address for ip in self.conn.network.ips()]
        for ip in floating_ips:
            print(ip)
        return floating_ips
