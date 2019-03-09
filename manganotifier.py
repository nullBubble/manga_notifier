def list_to_array(list):
    f = open(list,"r")
    output = f.read()
    arr = [x.strip() for x in output.split(',')]
    f.close()
    return arr

mlist, clist = [], []
mlist = list_to_array("Mangalist")
clist = list_to_array("Chapterlist")

