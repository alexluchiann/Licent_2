from env.instance import OpenstackConnect

class volumes_management(OpenstackConnect):
    def __init__(self):
        super().__init__()

    def has_attached_volumes(self, instance_id):
        try:
            instance = self.conn.compute.get_server(instance_id)
            return bool(instance.attached_volumes)
        except Exception as e:
            print("Error checking attached volumes:", e)
            return False

    def get_volume_image_id(self, instance_id):
        if instance_id is None:
            print("No instance_id given")
            return None

        try:
            instance = self.conn.get_server(instance_id)
            volumes_list = []

            for attachment in instance.attached_volumes:
                volumes_list.append(attachment.id)

            images_id = None
            for vol_id in volumes_list:
                volume = self.conn.block_storage.get_volume(vol_id)
                images_id = volume.volume_image_metadata.get('image_id')

            return images_id
        except Exception as e:
            print(e)

    def get_floating_ip_of_instance(self, instance_id):
        list_of_node_inst = self.list_All_VM()
        instance = None
        for node in list_of_node_inst:
            if node.id == instance_id:
                instance = self.conn.get_server(instance_id)
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



