from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_config, netmiko_send_command

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)


def baseconfig(admin):
    admin.run(task=netmiko_send_config, config_file="config_file.txt")
    admin.run(task=netmiko_send_command, command_string="show run")


targets = nr.filter(country="usa", hotel_code="orc")
results = targets.run(task=baseconfig)

print_title("DEPLOYING AUTOMATED BASELINE CONFIGURATIONS")
print_result(results)
