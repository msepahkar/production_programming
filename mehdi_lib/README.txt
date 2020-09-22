1- 'Prototype' SHOULD be added to the name of thing for its prototype
1- primary key order is always 0
2- primary key initial value is None, and for invalid things (removed things), the value will be -1
3- foreign key for non-existing foreign thing is None in program but -1 in database
4- name order is better to be always 1, in_class_name should be 'name'
5- foreign keys in the __init__ function of Thing, if of the same type, will be assigned to foreign fields of the thing by order of their order field.
    but fetch by foreign key, always fetches by the first found key.
