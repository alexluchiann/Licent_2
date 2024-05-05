import ansible.constants as c
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible import context

from env.instance import OpenstackConnect
from openstack_images_info import openstack_images_info

class ansible_management(OpenstackConnect):

    def __init__(self):
        super().__init__()
        self.image_info=openstack_images_info()

    def manage_inventory_file(self,targets):
        image_info_tuple = []
        for node in targets:
            image_id = node.image['id']

            username=self.image_info.usernames_dict.get(image_id, {}).get("username")

            tupl = lambda x , y , z : (x,y,z)

            image_info_tuple.append(tupl(node.name , image_id , username))
        '''
            username = self.image_info.usernames_dict.get(image_id, {}).get("username")
            if image_id not in image_info_dict:
                image_info_dict[image_id] = username
        print(image_info_dict)
        return image_info_dict
        '''

    def run_ansible_file(self,file_path):

