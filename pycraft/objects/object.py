
class WorldObject:
    pass


class WorldObjectRegistry:

    objects = {}

    def __init__(self, namespace=None):
        self.namespace = namespace

    def register(self, name):
        def register_object(cls):
            path = '%s.%s' % (self.namespace, name)
            WorldObjectRegistry.objects[path] = cls()
        return register_object

    def get(self, path):
        return WorldObjectRegistry.objects[path]
