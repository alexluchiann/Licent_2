import os
import subprocess


from openstack_images_info import openstack_images_info
from volumes_management import volumes_management
from env.instance import OpenstackConnect


class ansible_management(volumes_management):
    def __init__(self):
        self.image_info=openstack_images_info()
        super().__init__()

    def manage_inventory_file(self,targets):

        image_info_tuple = []
        for node in targets:
            instance_id = node.id
            tupl = lambda x, y, z: (x, y, z)
            if self.has_attached_volumes(instance_id):
                volume_image = self.get_volume_image_id(instance_id)
                username = self.image_info.usernames_dict.get(volume_image, {}).get("username")
                image_info_tuple.append(tupl(node.name , volume_image , username))

            else:
                image_id=node.image.get("id")
                username = self.image_info.usernames_dict.get(image_id, {}).get("username")
                image_info_tuple.append(tupl(node.name , image_id , username))

        return image_info_tuple

    def rewrite_inventory_file(self,file_path,targets):

        if os.path.exists(file_path) is False:
            print("The file {} does not exits !!! ".format(file_path))
            return
        target_nodes = self.manage_inventory_file(targets)







    def run_ansible_file(self, playbook_path,inventory_path, private_key_path):
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


app=ansible_management()
targ=[]
for i in app.list_All_VM():
    targ.append(i)


for i in app.manage_inventory_file(targ):
    print(i)


'''
app.run_ansible_file("/home/alex/Licenta_2024/python_app/ansible_playbooks/hello_world.yml",
                     "/home/alex/Licenta_2024/python_app/ansible_playbooks/inventory.ini",
                     "/home/alex/Licenta_2024/python_app/ansible_playbooks/licenta.pem")
'''

