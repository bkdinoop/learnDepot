import yaml
# instead you can also use ruamel.yaml

file_path = "./sample.yaml"
accDetail = {
    "account_id": "111111111",
    "name": "sampleAcc",
    "default_region": "us-east-1",
    "regions_enabled": ["us-east-1", "us-east-2"],
    "tags": ["type:prod", "partition:us", "scope:pci"],
    "parameters": {
        "foo": {
            "default": "account_foo"
        }
    }
}


class MyDumper(yaml.Dumper):
    # https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def addNewAccount(accDetail):
    """
    New Account will be added to sample.yaml
    """
    contents = readFile()
    contents["accounts"].append(accDetail)    
    overwritefile(contents)


def readFile():
    # Read the yaml file and convert to a python datastructure
    with open(file_path, 'r') as confFile:
        try:
            content = yaml.safe_load(confFile)
            return content
        except yaml.YAMLError as e:
            raise e


def overwritefile(contents):
    # Write to yaml file
    with open(file_path, 'w') as confFile:
        try:
            # Add the comment first to file if needed
            content = yaml.dump(contents, confFile, Dumper=MyDumper, default_flow_style=False)            
            return content
        except yaml.YAMLError as e:
            raise e

if __name__ == "__main__":
    # Function take new account details to be part of
    # sample.yaml
    addNewAccount(accDetail)
