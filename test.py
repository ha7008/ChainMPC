from protocol_1_circuit import Protocol_1_circuit            

p = Protocol_1_circuit()
#r = p.create_R(4,4)
z=[1,0,1,1]
z.reverse()
v=[0,1,1,0]
#print(f"R = {r}")
print(f"Z = {z}")
print(f"V = {v}")
p.create(5, bit_size = 4)
p.garble()

input_labels = p.choose_labels(z, v, remove_Z=False)
print(len(input_labels))
result = p.ungarble(input_labels)
print(result.represents)
