
block_types={}

def register_block(block, name):
    if hasattr(blockTypes,name):
        print("block with that name already exists") 
    else:
        blockTypes[name] = block
    return block


