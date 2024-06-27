import os
import subprocess
from volumes_management import Volumes_Management
from openstack_images_info import Openstack_images_info


class ansible_management(Volumes_Management):
    def __init__(self):
        self.image_info = Openstack_images_info()
        super().__init__()

    def manage_inventory_file(self, targets):
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
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist!")
            return

        target_nodes = self.manage_inventory_file(targets)
        list_of_nodes_with_ip = [prob for prob in target_nodes if prob[3] is not None]

        with open(file_path, 'a+') as file:
            file.write('\n')
            for node in list_of_nodes_with_ip:
                file.write(f"{node[3]} ansible_user={node[2]}\n")

    def run_ansible_file(self, playbook_path, inventory_path, private_key_path):
        env = os.environ.copy()
        env['ANSIBLE_HOST_KEY_CHECKING'] = 'False'

        subprocess.run([
            'ansible-playbook',
            playbook_path,
            '-i', inventory_path,
            '--private-key', private_key_path
        ], check=True,env=env)

    def delete_file_content(self, input_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        first_line_with_bracket = next((line for line in lines if line.startswith('[')), None)

        with open(input_file, 'w') as f:
            if first_line_with_bracket:
                f.write(first_line_with_bracket)
            print("The file is clean")

    def get_right_path(self):
        target_dir = 'ansible_playbooks'
        current_working_directory = os.getcwd()
        parent_directory = os.path.abspath(os.path.join(current_working_directory, os.pardir))
        abs_target_path = os.path.abspath(os.path.join(parent_directory, target_dir))
        return abs_target_path

    def get_ansible_playbooks_files(self):
        return [file for file in os.listdir(self.get_right_path()) if file.endswith(('.yml', '.yaml'))]

    def get_ansible_playbooks_files_path(self):
        path = self.get_right_path()
        return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(('.yml', '.yaml'))]

    def get_inventory(self):
        return os.path.join(self.get_right_path(), 'inventory.ini')

    def get_private_key_file(self):
        return os.path.join(self.get_right_path(), 'licenta_2.pem')

    def delete_file_from_ansible_playbook(self, target):
        abs_target_path = self.get_right_path()
        list_file = os.listdir(abs_target_path)
        if target in list_file:
            os.remove(os.path.join(abs_target_path, target))
            print(f"File {target} was deleted ")
        else:
            print("Nu functioneaza")

    def get_scripts_descriptions(self):
        descriptions_path = os.path.join(self.get_right_path(), 'scripts_descriptions.txt')
        scripts_descriptions = []

        if os.path.exists(descriptions_path):
            with open(descriptions_path, 'r') as f:
                for line in f:
                    parts = line.strip().split('   ', 1)
                    if len(parts) == 2:
                        script_name, script_description = parts
                        scripts_descriptions.append((script_name, script_description))

        return scripts_descriptions