from configparser import ConfigParser, NoSectionError, NoOptionError


class config:

    def __init__(self):
        self.path = '/hello/ehall/config.ini'
        self.cp = ConfigParser()
        self.cp.readfp(open(str(self.path)))

    def set(self, section, name, value):
        try:
            self.cp.set(section, name, value)
            self.cp.write(open(str(self.path), "w"))
        except NoSectionError:
            return "NoSection"
        except NoOptionError:
            return "NoOption"

    def get(self, section, name):
        print(self.cp.get(section, name))
        return self.cp.get(section, name)

    def add(self, section):
        self.cp.add_section(section)
        self.cp.write(open(str(self.path), "w"))

    def Odel(self, section, name):
        try:
            self.cp.remove_option(section, name)
            self.cp.write(open(str(self.path), "w"))
        except NoSectionError:
            return "NoSection"
        except NoOptionError:
            return "NoOption"

    def Sdel(self, section):
        try:
            self.cp.remove_section(section)
            self.cp.write(open(str(self.path), "w"))
        except NoSectionError:
            return "NoSection"
        except NoOptionError:
            return "NoOption"
