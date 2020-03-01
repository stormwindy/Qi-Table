f = open("d2t2res", "r")
i = 0
tot_time = 0
tot_frame = 0
line = f.readline()
while line:
    if i % 2 == 0:
        tot_frame += int(line[-2])
    else:
        tot_time += float(line[:-1])
    line = f.readline()
    i += 1

assert(i%2 == 0)

tot = i // 2

print("total meaurement =", tot)
print("avg time =", tot_time/tot)
print("avg frame taken =", tot_frame/tot)