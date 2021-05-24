v_l_p = [(5, 4)]
max_v = range(8)

v_l_p = [(pose[0], max_v[::-1][pose[1]]) for pose in v_l_p]

print(f"vlp = {v_l_p}")
