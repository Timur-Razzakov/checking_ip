n_list =  [{"key1": "value1"}, {"k1": "v1", "k2": "v2", "k3": "v3"}, {}, {}, {"key1": "value1"},
           {"key1": "value1"}, {"key2": "value2"}]
copy = sorted(n_list)
print(copy)
# new_data = set(n_list)
#
# # new_data = [ set(frozenset(d.items()) for d in  n_list)]
# print(type(new_data))
# print((new_data))

# def is_unique(alist):
#     copy = sorted(alist)
#     print(copy)
#
#
# is_unique(n_list)