import Tkinter

class MenuBarManager(object):
    
    def __init__(self, menubar):
        self.menubar = menubar
        self.root = _MenuCascade(menubar, '')
    
    def add_menu_command(self, address, command):
        parent = self._find_parent(address)
        parent.add_command(address.address[-1], command, address.alt_key,
                           address.last_group)

    def add_menu_cascade(self, address):
        parent = self._find_parent(address)
        parent.add_cascade(address.address[-1], address.alt_key,
                              address.last_group)
    
    def _find_parent(self, address):
        parent = self.root
        for name in address.address[:-1]:
            parent = parent.get_child(name)
        return parent
            

class MenuAddress(object):
    
    def __init__(self, address, alt_key=None, last_group=None):
        self.address = address
        self.alt_key = alt_key
        self.last_group = last_group


class _MenuItem(object):
    
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name


class _MenuCascade(_MenuItem):
    
    def __init__(self, menu, name):
        super(_MenuCascade, self).__init__(name)
        self.menu = menu
        self.children = []
    
    def add_command(self, name, command, alt_key=None, group=None):
        location = self._find_location(name, group)
        optional_kws = {}
        if self._calculate_underline(name, alt_key) != -1:
            optional_kws['underline'] = self._calculate_underline(name, alt_key)
        self.menu.insert_command(location, label=name, command=command, **optional_kws)
        self.children.insert(location, _MenuCommand(name))

    def add_cascade(self, name, alt_key=None, group=None):
        location = self._find_location(name, group)
        new_menu = Tkinter.Menu(self.menu, tearoff=0, font=("mono", 13, 'bold'))
        optional_kws = {}
        if self._calculate_underline(name, alt_key) != -1:
            optional_kws['underline'] = self._calculate_underline(name, alt_key)
        self.menu.insert_cascade(location + 1, label=name, menu=new_menu, **optional_kws)
        self.children.insert(location, _MenuCascade(new_menu, name))
    
    def _calculate_underline(self, name, key):
        name = name.lower()
        if key is not None and key.lower() in name:
            return name.index(key.lower())
        return -1
    
    def _find_location(self, name, group):
        if group == None:
            group = 0
        index = 0
        current_group = 0
        for child in self.children:
            if isinstance(child, _MenuSeparator):
                current_group += 1
                if group + 1 == current_group:
                    break
            index += 1
        for i in range(group - current_group):
            self.children.append(_MenuSeparator(str(current_group + i)))
            self.menu.add_separator()
            index += 1
        return index
    
    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child


class _MenuSeparator(_MenuItem):
    pass


class _MenuCommand(_MenuItem):
    pass

