import os
import subprocess

from env.instance import OpenstackConnect
from volumes_management import Volumes_Management
class ansible_management(Volumes_Management):
    def __init__(self):
        from openstack_images_info import OpenstackImagesInfo
        self.image_info = OpenstackImagesInfo()
        super().__init__()

    def manage_inventory_file(self, targets):
        from volumes_management import Volumes_Management

        image_info_tuple = []
        for node in targets:
            instance_id = node.id
            tupl = lambda x, y, z, t: (x, y, z, t)
            if self.has_attached_volumes(instance_id):
                volume_image = self.get_volume_image_id(instance_id)
                username = self.image_info.usernames_dict.get(volume_image, {}).get("username")
                instance_floating_ip = self.get_floating_ip_of_instance(instance_id)
                image_info_tuple.append(tupl(node.name, volume_image, username, instance_floating_ip))
            else:
                image_id = node.image.get("id")
                username = self.image_info.usernames_dict.get(image_id, {}).get("username")
                instance_floating_ip = self.get_floating_ip_of_instance(instance_id)
                image_info_tuple.append(tupl(node.name, image_id, username, instance_floating_ip))

        return image_info_tuple

    def rewrite_inventory_file(self, file_path, targets):
        if os.path.exists(file_path) is False:
            print("The file {} does not exist!!!".format(file_path))
            return
        target_nodes = self.manage_inventory_file(targets)
        list_of_nodes_with_ip = []

        for prob in target_nodes:
            if prob[3] is None:
                continue
            else:
                list_of_nodes_with_ip.append(prob)

        with open(file_path, 'a+') as file:
            file.write('\n')
            for node in list_of_nodes_with_ip:
                file.write("{} ansible_user={}\n".format(node[3], node[2]))

    def run_ansible_file(self, playbook_path, inventory_path, private_key_path):
        try:
            subprocess.run([
                'ansible-playbook',
                playbook_path,
                '-i', inventory_path,
                '--private-key', private_key_path
            ], check=True)
            print("Ansible playbook executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing Ansible playbook: {e}")

    def delete_file_content(self, input_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        first_line_with_bracket = None
        for line in lines:
            if line.startswith('['):
                first_line_with_bracket = line
                break

        with open(input_file, 'w') as f:
            if first_line_with_bracket:
                f.write(first_line_with_bracket)
        print("The file is clean")

app = ansible_management()

'''
targ=[]
for i in app.list_All_VM():
    targ.append(i)

#app.rewrite_inventory_file('/home/alex/Licenta_2024/python_app/ansible_playbooks/inventory.ini',targ)
#app.delete_file_contnet('/home/alex/Licenta_2024/python_app/ansible_playbooks/inventory.ini')


app.run_ansible_file("/home/alex/Licenta_2024/OpenStack_v2/ansivle_playbooks/testt_2.yml",
                     "/home/alex/Licenta_2024/python_app/ansible_playbooks/inventory.ini",
                     "/home/alex/Licenta_2024/python_app/ansible_playbooks/licenta.pem")
'''
