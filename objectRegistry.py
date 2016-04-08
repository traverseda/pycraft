
block_types = {}


def register_block(block, name):
    if hasattr(block_types, name):
        print("block with that name already exists") 
    else:
        block_types[name] = block
    return block
