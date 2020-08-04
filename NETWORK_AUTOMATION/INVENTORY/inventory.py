from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result, print_title
import csv
import getpass

nr = InitNornir(config_file="config.yaml", dry_run=True)
username = input("Please enter domain username: ")
nr.inventory.defaults.username = username
password = getpass.getpass()
nr.inventory.defaults.password = password


def dev_info(task):
    r = task.run(netmiko_send_command, command_string="show version", use_genie=True)
    task.host["facts"] = r.result
    serial = task.host['facts']['version']['chassis_sn']
    host_name = task.host['facts']['version']['hostname']
    interface_no = task.host['facts']['version']['number_of_interfaces']
    image = task.host['facts']['version']['system_image']
    im_type = task.host['facts']['version']['image_type']
    operating = task.host['facts']['version']['os']
    up = task.host['facts']['version']['uptime']
    ver = task.host['facts']['version']['version']
    created = task.host['facts']['version']['compiled_date']

    with open('device_report.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        csvdata = ('myfairmont', task.host.hostname, host_name, serial,
                   interface_no, image, im_type, operating, up, ver, created)
        writer.writerow(csvdata)


def main() -> None:
    nr = InitNornir()
    result = nr.run(task=dev_info)
    print_result(result)


if __name__ == '__main__':
    main()
