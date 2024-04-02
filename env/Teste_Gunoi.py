from instance import OpenstackConnect
from networks_class import openstack_network_operations

network_operations=openstack_network_operations()

#network_operations.create_network("Test_Vlan_22_444", "Descriereeee", subnet_name="subnet_19", subnet_cidr="10.0.0.0/24")
#network_operations.create_router("Test_Router",external_network_id='18e19f15-951e-4da4-8d83-f60f9de5cdfc')

#for i in network_operations.list_networks():
    #print(str(i.id)+" "+str(i.name) + '\n')

#network_operations.connect_router_to_network("Test_22","Test_Vlan_22_444")
''''
for i in network_operations.list_routers():
    print(str(i.name)+ "        " + str(i.id))
print("___________________________________________________________________________________________")
'''

for i in network_operations.list_networks():
    print("Network name ",i.name ,"   Vlan ID   ",i.provider_segmentation_id)

#network_operations.connect_router_to_network("c74c0794-0550-4f84-b707-0f8fba962a96","18e19f15-951e-4da4-8d83-f60f9de5cdfc")
#network_operations.network.add_gateway_to_router("c74c0794-0550-4f84-b707-0f8fba962a96","18e19f15-951e-4da4-8d83-f60f9de5cdfc")
#network_operations.create_router("Mare_Test")
'''
network_operations.conn.network.add_external_gateways(
    router="7a80c1cc-29b0-4f08-a10c-8131464be1cc",
    network_id="18e19f15-951e-4da4-8d83-f60f9de5cdfc"
)
'''
print("_______________________________________________________________________________")
for i in network_operations.list_routers():
    print(str(i.name)+ "            " + str(i.id))

#network_operations.create_router("Test_1123","18e19f15-951e-4da4-8d83-f60f9de5cdfc")
#network_operations.create_router("Test_1123","18e19f15-951e-4da4-8d83-f60f9de5cdfc")
#network_operations.create_router("Alt test ")
#network_operations.connect_router_to_network("da2c4e8d-6170-4c3a-b310-f0bcc291c7c6","18e19f15-951e-4da4-8d83-f60f9de5cdfc")