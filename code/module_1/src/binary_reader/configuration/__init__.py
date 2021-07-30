import lxml.objectify
import json

def interface_method():
    print("interface_method locals {}".format(locals()))
    def not_implmented_decorator(func, *args2, **kargs2):
        print("not_implmented_decorator locals {}".format(locals()))
        raise NotImplementedError('A subclass must implement this!')
    return not_implmented_decorator


class Configuration():
    def __init__(self, file_name):
        with open(file_name, 'r') as self._file:
            self._root = self._parse()

    def _parse(self):
        pass

    def get_root(self):
        """
        Our public method
        """
        return self._root


class XmlConfiguration(Configuration):
    def _parse(self):
        return lxml.objectify.parse(self._file).getroot()


class JsonConfiguration(Configuration):
    class EmptyObj:
        pass

    def __create_recursive_obj(self, children):
        obj = JsonConfiguration.EmptyObj()
        for child_key in children:
            if isinstance(children[child_key], dict):
                child_obj = self.__create_recursive_obj(children[child_key])
                setattr(obj, child_key, child_obj)
            elif isinstance(children[child_key], list):
                child_objs = []
                for child_in_list in children[child_key]:
                    child_obj = self.__create_recursive_obj(child_in_list)
                    child_objs.append(child_obj)
                setattr(obj, child_key, child_objs)
            else:
                setattr(obj, child_key, children[child_key])
        return obj

    def _parse(self):
        obj = self.__create_recursive_obj(json.load(self._file))

        class ElementWithAttributes:
            def __init__(self, obj):
                self.attrib = {public_attr: getattr(obj, public_attr) for public_attr in dir(obj) if
                               not public_attr.startswith("__")}

        header_attibutes = [ElementWithAttributes(attribute) for attribute in obj.packet.header]
        delattr(obj.packet, 'header')
        setattr(obj.packet, 'header', JsonConfiguration.EmptyObj())
        setattr(obj.packet.header, 'attribute', header_attibutes)

        payload_variables = [ElementWithAttributes(variable) for variable in obj.packet.payload]
        delattr(obj.packet, 'payload')
        setattr(obj.packet, 'payload', JsonConfiguration.EmptyObj())
        setattr(obj.packet.payload, 'variable', payload_variables)
        return obj