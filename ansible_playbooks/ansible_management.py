import os.path
import shutil
import subprocess
import ansible_runner
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager
import ansible.constants as C
import yaml  # Add this import statement


from env.instance import OpenstackConnect
class ansible_management(OpenstackConnect):

    def __init__(self):
        super().__init__()

    def manage_inventory_file(self,targets):
        image_info_tuple = []
        for node in targets:
            image_id = node.image['id']

            username=self.usernames_dict.get(image_id, {}).get("username")

            tupl = lambda x , y , z : (x,y,z)

            image_info_tuple.append(tupl(node.name , image_id , username))
        '''
            username = self.image_info.usernames_dict.get(image_id, {}).get("username")
            if image_id not in image_info_dict:
                image_info_dict[image_id] = username
        print(image_info_dict)
        return image_info_dict
        '''

    def run_ansible_file(self, playbook_path,inventory_path, private_key_path):
        try:
            # Run the Ansible playbook using subprocess
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

app.run_ansible_file("/home/alex/Licenta_2024/python_app/ansible_playbooks/hello_world.yml",
                     "/home/alex/Licenta_2024/python_app/ansible_playbooks/inventory.ini",
                     "/home/alex/Licenta_2024/python_app/ansible_playbooks/licenta.pem")