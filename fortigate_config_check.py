from collections import defaultdict
from pprint import pprint
import sys
import re

f = lambda: defaultdict(f)

def getFromDict(dataDict, mapList):
    return reduce(lambda d, k: d[k], mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value    

class Parser(object):

    def __init__(self):
        self.config_header = []
        self.section_dict = defaultdict(f)

    def parse_config(self, fields): # Create a new section
        self.config_header.append(" ".join(fields))

    def parse_edit(self, line): # Create a new header
        self.config_header.append(line[0])

    def parse_set(self, line): # Key and values
        key = line[0]
        values = " ".join(line[1:])
        headers= self.config_header+[key]
        setInDict(self.section_dict,headers,values)

    def parse_next(self, line): # Close the header
        self.config_header.pop()

    def parse_end(self, line): # Close the section
        self.config_header.pop()

    def parse_file(self, path):          
        with open(path) as f:
            gen_lines = (line.rstrip() for line in f if line.strip())
            for line in gen_lines:
                #pprint(dict(self.section_dict))
                # Clean up the fields and remove unused lines.            
                fields = line.replace('"', '').strip().split(" ")

                valid_fields= ["set","end","edit","config","next"]
                if fields[0] in valid_fields:
                    method = fields[0]
                    # fetch and call method
                    #print("config flag: %s edit flag:  %s  %s " %(self.config_flag, self.edit_flag, fields[1:]))
                    getattr(Parser, "parse_" + method)(self, fields[1:])

        return self.section_dict

class Fortigate_Checks(Parser):
    def __init__(self, Parser):
        self.config = Parser
        self.check_name = ""

    def get_hostname(self):
        self.check_name = "Hostname:"
        return (self.check_name, self.config["system global"]["hostname"])

    def get_strong_crypto(self):
        self.check_name = "Strong Crypto settings:"
        if self.config["system global"]["strong-crypto"] == "enable":
            return (self.check_name, True)
        return (self.check_name, False)

    def get_ips_addresses(self):
        self.check_name = 'IP\'s on "port" interfaces'
        ips = []
        for elem in self.config["system interface"].keys():
            if self.config["system interface"][elem]["ip"]:
                ips.append((elem, self.config["system interface"][elem]["ip"]))
        return (self.check_name, ips)
        
    def get_proto_int_access(self):
        self.check_name = 'Protocols used to access the "port" interfaces'
        ips = []
        for elem in self.config["system interface"].keys():
            if self.config["system interface"][elem]["ip"]:
                ips.append((elem, self.config["system interface"][elem]["allowaccess"]))
        return (self.check_name, ips)

    def get_ha_encryption(self):
        self.check_name = "Encryption of HA packets:"
        if self.config["system ha"]["encryption"] == "enable":
            return (self.check_name, True)
        return (self.check_name, False)

    def get_ha_authentication(self):
        self.check_name = "Authentication of HA packets:"
        if self.config["system ha"]["authentication"] == "enable":
            return (self.check_name, True)
        return (self.check_name, False)


def main():
    #string = re.search('#config-version=.*', text_new)
    #print(string.group(0).split("-")[2])
    config = Parser().parse_file(r'c:\temp\muster_v5.conf')
    forti_check = Fortigate_Checks(config)
    print(forti_check.get_hostname())
    print(forti_check.get_strong_crypto())
    print(forti_check.get_ha_encryption())
    print(forti_check.get_ha_authentication())
    print(forti_check.get_ips_addresses())
    print(forti_check.get_proto_int_access())


if __name__ == "__main__":
    main()

