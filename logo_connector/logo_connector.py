import snap7

plc = snap7.client.Client()
plc.set_connection_params("192.168.1.2", 0x0300, 0x0200)

plc.connect("192.168.1.2", 0, 1)
c = plc.get_connected()
print(c)

print(plc.get_cpu_info())
print(plc.get_cpu_state())


