import os
import json

defect_class_dsc = []
list_defect_class_dsc = []
defect_class_dsc_path = '/media/user/26C2BC47C2BC1CCD/D_projects/prct/dipl2/img2/NEU_Metal_Surface_Defects_Data/test/'
class_list = sorted(os.listdir(defect_class_dsc_path))

for class_name in class_list:    
    defect_class_dsc.append(class_name)
    info = os.getxattr(defect_class_dsc_path + class_name,'user.description' ,follow_symlinks=True)
    info = info.decode("utf-8")
    defect_class_dsc.append(info)
    list_defect_class_dsc.append(defect_class_dsc)
    defect_class_dsc = []
print(list_defect_class_dsc)

to_json = {
    "GOST_list_defect": list_defect_class_dsc
}
with open('GOST_list_defect.json', 'w') as f:
    f.write(json.dumps(to_json, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))
f.close()


# # filename = ['gost_21014_2022_non_metallic_inclusion_test(In) = ',
# #          'gost_21014_2022_pitted_surface_test(Ps) = ',
# #          'gost_21014_2022_rippled_surface_test(Cr) = ', 
# #          'gost_21014_2022_rolled_in_scale_test(RS) = ', 
# #          'gost_21014_2022_scratch_test(Sc) = ', 
# #          'gost_21014_2022_sticker_patches_test(Pa) = ']

# 
# 
# print(info)
# for i in range(len(filename)):
#     j_objct = {
#         f'defect_{i}': {
#             'defect_class': filename,
#             'description': info,
#             'threshold value': '95'
#         }   
#     }
