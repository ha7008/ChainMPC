from protocol_1_circuit import Protocol_1_circuit            

p = Protocol_1_circuit()
r = p.create_R(4)
z=[1,1,1,1]
v=[0,1,0,0]
print(f"R = {r}")
print(f"Z = {z}")
print(f"V = {v}")
p.create(r, bit_size = 4)
p.garble()

input_labels = p.choose_labels(z, v)
result = p.ungarble(input_labels)
print(result.represents)
