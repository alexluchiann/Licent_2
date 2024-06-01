from env.instance import OpenstackConnect
from ansible_management import openstack_images_info


class Volumes_Management(openstack_images_info):
    def __init__(self):
        super().__init__()


    def has_attached_volumes(self, instance_id):
        try:
            instance = self.conn_openstack.conn.compute.get_server(instance_id)
            return bool(instance.attached_volumes)
        except Exception as e:
            print("Error checking attached volumes:", e)
            return False

    def get_volume_image_id(self, instance_id):
        if instance_id is None:
            print("No instance_id given")
            return None

        try:
            instance = self.conn_openstack.conn.get_server(instance_id)
            volumes_list = []

            for attachment in instance.attached_volumes:
                volumes_list.append(attachment.id)

            images_id = None
            for vol_id in volumes_list:
                volume = self.conn_openstack.conn.block_storage.get_volume(vol_id)
                images_id = volume.volume_image_metadata.get('image_id')

            return images_id
        except Exception as e:
            print(e)

    def get_floating_ip_of_instance(self, instance_id):
        list_of_node_inst = self.conn_openstack.list_All_VM()
        instance = None
        for node in list_of_node_inst:
            if node.id == instance_id:
                instance = self.conn_openstack.conn.get_server(instance_id)
                break
        if instance is None:
            print("The instance doesn't exist or the ID is incorrect")
            return None

        try:
            get_key = lambda d: next(iter(d))
            addresses = instance.addresses.get(get_key(instance.addresses), [])
            for address in addresses:
                if address['OS-EXT-IPS:type'] == 'floating':
                    return address['addr']
            print("The instance doesn't have a floating IP")
            return None
        except Exception as e:
            print(str(e) + " The instance doesn't have a floating IP")
            return None

    def get_os_with_instance_id(self, vm_id):

        if self.has_attached_volumes(vm_id):
            return self.image_data[self.get_volume_image_id(vm_id)]
        else:
            instance = self.conn_openstack.conn.compute.get_server(vm_id)  #self.conn.compute.get_server(vm_id)
            image_id = instance.image['id']
            return self.image_data[image_id]

app =Volumes_Management()

print(app.get_os_with_instance_id('e2d3fc07-8670-455f-a39f-177f839cf807'))