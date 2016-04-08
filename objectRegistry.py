
blockTypes={}

def registerBlock(block, name):
    if hasattr(blockTypes,name):
        print("block with that name already exists") 
    else:
        blockTypes[name] = block
    return block


