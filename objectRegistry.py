
block_types = {}


def register_block(block, name):
    if name in block_types:
        print("block with that name already exists")
    else:
        block_types[name] = block
    return block
