# def simulate(intra, extra, L):
#     # we might need to convert trans_V is not a sheet 
#     orig_intra, orig_extra = intra, extra
#     stepper = 0
#     while stepper < 10:
#         #TODO check if + or - for the shift
#         trans_V = np.add(flat(intra)-flat(extra), 70.0)
#         # trans_V = (flat(intra)- flat(extra)) + 70
#         val = 30.0
#         if stepper < 5:
#             trans_V[0] = -70+val
#             trans_V[1] = -70+val
#             # trans_V[2] = -70+val
#             trans_V[-1] = -70+val
#             trans_V[-2] = -70+val
#             # trans_V[-3] = -70+val
#         # print(generate_ionic_current(trans_V))
#         new_V = np.linalg.solve(L, generate_ionic_current(trans_V))
#         intra, extra = split_list(new_V)
#         intra = unflatten(intra, len(orig_intra), len(orig_intra[0]))
#         extra = unflatten(extra, len(orig_extra), len(orig_extra[0]))
#         #display stuff
#         display_heat_map(intra - extra)
        
#         # trans_V = np.add(intra - extra, 70.0) 
#         stepper += 1