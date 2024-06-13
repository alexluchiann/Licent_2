import openstack
from env.instance import OpenstackConnect

class Openstack_images_info(OpenstackConnect):
    def __init__(self):
        super().__init__()
        self.image_data = {
            "afc098f7-9013-47fc-a73d-a75e31e7d337": "Ubuntu Xenial",
            "e1754e5d-3d67-4a91-bdd9-4f61cbe63ca4": "Fedora CoreOS 35",
            "6fb46d64-319f-430c-aeba-f3aee11c058c": "Sahara Vanilla Ubuntu",
            "f5607735-b75a-434b-a671-33def3564fc1": "Windows 2019 Zabbix Agent",
            "7cbedf53-25f6-4d60-9f77-06c1b04e53d2": "Windows Server 2012",
            "0959c81e-fa77-4ffb-be21-46e7bc4168af": "CentOS 7 Zabbix Agent",
            "f760b718-ded2-468f-9213-c27efc2d499a": "Windows 2019",
            "4b54ac1a-8256-48d6-ad39-be61f8770655": "Ubuntu Zabbix Server",
            "24444ee4-7f0c-4dc9-8c85-4c57a9711e3e": "Fedora 38",
            "0538d06b-ad7e-40c9-bcf4-02737766b44a": "openSUSE-Leap-15.2",
            "92b19b2f-05e7-4af8-ba33-3c9ddcecb727": "Arch Linux",
            "76c062a8-0501-4d0c-8248-ef4278120577": "CentOS 7",
            "6dd603ae-f30c-43ba-8c69-19acc30a5c7d": "CentOS Stream 9",
            "0d8cf877-f45f-4d1d-bfc4-545e4bc4fa0b": "CentOS 8",
            "7f7918ba-1add-40a6-9720-8fcc112984c0": "CirrOS",
            "de4d2912-3cdf-4b23-9608-9133d63212d6": "Debian 11",
            "bcf7e2b7-c274-439b-a4eb-04ba29c66a12": "Ubuntu Jammy",
            "2bb4eb89-c989-4e13-b2a8-eba5af542819": "Ubuntu Focal"
        }

        self.usernames_dict = {
            "afc098f7-9013-47fc-a73d-a75e31e7d337": {"name": "Ubuntu Xenial", "username": "ubuntu"},
            "e1754e5d-3d67-4a91-bdd9-4f61cbe63ca4": {"name": "Fedora CoreOS 35", "username": "core"},
            "6fb46d64-319f-430c-aeba-f3aee11c058c": {"name": "Sahara Vanilla Ubuntu", "username": "ubuntu"},
            "f5607735-b75a-434b-a671-33def3564fc1": {"name": "Windows 2019 Zabbix Agent",
                                                     "username": "Administrator or admin"},
            "7cbedf53-25f6-4d60-9f77-06c1b04e53d2": {"name": "Windows Server 2012",
                                                     "username": "Administrator or admin"},
            "0959c81e-fa77-4ffb-be21-46e7bc4168af": {"name": "CentOS 7 Zabbix Agent", "username": "centos"},
            "f760b718-ded2-468f-9213-c27efc2d499a": {"name": "Windows 2019", "username": "Administrator or admin"},
            "4b54ac1a-8256-48d6-ad39-be61f8770655": {"name": "Ubuntu Zabbix Server", "username": "ubuntu"},
            "24444ee4-7f0c-4dc9-8c85-4c57a9711e3e": {"name": "Fedora 38", "username": "fedora"},
            "0538d06b-ad7e-40c9-bcf4-02737766b44a": {"name": "openSUSE-Leap-15.2", "username": "root"},
            "92b19b2f-05e7-4af8-ba33-3c9ddcecb727": {"name": "Arch Linux", "username": "root"},
            "76c062a8-0501-4d0c-8248-ef4278120577": {"name": "CentOS 7", "username": "centos"},
            "6dd603ae-f30c-43ba-8c69-19acc30a5c7d": {"name": "CentOS Stream 9", "username": "centos"},
            "0d8cf877-f45f-4d1d-bfc4-545e4bc4fa0b": {"name": "CentOS 8", "username": "centos"},
            "7f7918ba-1add-40a6-9720-8fcc112984c0": {"name": "CirrOS", "username": "cirros"},
            "de4d2912-3cdf-4b23-9608-9133d63212d6": {"name": "Debian 11", "username": "debian"},
            "bcf7e2b7-c274-439b-a4eb-04ba29c66a12": {"name": "Ubuntu Jammy", "username": "ubuntu"},
            "2bb4eb89-c989-4e13-b2a8-eba5af542819": {"name": "Ubuntu Focal", "username": "ubuntu"}
        }

        self.os_data = [
    ("Arch Linux", "2.00 GB"),
    ("CentOS 7", "8.00 GB"),
    ("CentOS 7 Zabbix Agent", "10.00 GB"),
    ("CentOS 8", "10.00 GB"),
    ("CentOS Stream 9", "10.00 GB"),
    ("CirrOS", "112.00 MB"),
    ("Debian 11", "2.00 GB"),
    ("Fedora 38", "5.00 GB"),
    ("Fedora CoreOS 35", "10.00 GB"),
    ("fedora-coreos-latest", "1.58 GB"),
    ("openSUSE-Leap-15.2", "10.00 GB"),
    ("Sahara Vanilla Ubuntu", "5.80 GB"),
    ("Ubuntu Focal", "2.20 GB"),
    ("Ubuntu Jammy", "2.20 GB"),
    ("Ubuntu Xenial", "300.75 MB"),
    ("Ubuntu Zabbix Server", "10.00 GB"),
    ("Windows 2019", "15.00 GB"),
    ("Windows 2019 Zabbix Agent", "16.00 GB"),
    ("Windows Server 2012", "12.20 GB"),
    ("Cirros_vbutnaru", "112.00 MB")
    ]

        self.flavors_list = [
    ("m1.tiny", 1, "512 MB"),
    ("m1.small", 1, "2 GB"),
    ("m1.medium", 2, "4 GB"),
    ("g1.1xMedium", 2, "4 GB"),
    ("m1.large", 4, "8 GB"),
    ("m1.xlarge", 8, "16 GB")
    ]


    def get_list_images_info(self):
        imagess = [img for img in self.conn.compute.images()]
        return imagess

    def get_list_of_images_name(self):
        names = []
        for im_name in self.get_list_images_info():
            names.append(im_name.name)
        return names

    def get_list_of_images_id(self):
        names = []
        for im_name in self.get_list_images_info():
            names.append(im_name.id)
        return names

