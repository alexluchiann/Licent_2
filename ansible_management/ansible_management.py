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


    def get_right_path(self):
        target_dir = 'ansible_playbooks'
        current_working_directory = os.getcwd()
        parent_directory = os.path.abspath(os.path.join(current_working_directory, os.pardir))
        abs_target_path = os.path.abspath(os.path.join(parent_directory, target_dir))
        return abs_target_path
    def get_ansible_playbooks_files(self):
        list_file=[]
        list_fil = os.listdir(self.get_right_path())
        for file in list_fil:
            if file.endswith(('.yml', '.yaml')):
                list_file.append(file)
        return list_file

    def get_ansible_playbooks_files_path(self):
        list_file = []
        path = self.get_right_path()
        file_path = None
        list_fil = os.listdir(self.get_right_path())
        for file in list_fil:
            if file.endswith(('.yml', '.yaml')):
                file_path = path + '/'+file
                list_fil.append(file_path)
        return list_file

    def get_inventory(self):
        path = self.get_right_path()
        inv_file = path+'/inventory.ini'
        inventory_path = os.path.join(path,inv_file)
        return inventory_path

    def get_private_key_file(self):
        path = self.get_right_path()
        key_file = path + '/licenta.pem'
        private_key_path = os.path.join(path, key_file)
        return private_key_path

    def delete_file_from_ansible_playbook(self,target):
        abs_target_path=self.get_right_path()
        list_file = os.listdir(self.get_right_path())
        if target in list_file:
            os.remove(os.path.join(abs_target_path, target))
            print(f"File {target} was deleted ")
        else:
            print("Nu functioneaza")

app =ansible_management()
print(app.get_private_key_file())
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