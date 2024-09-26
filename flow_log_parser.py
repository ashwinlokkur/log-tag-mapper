import csv
import socket
import sys
from collections import defaultdict
from protocol_map import PROTOCOL_MAP


def load_lookup_table(lookup_file):
    """
    load lookup table from csv
    """
    lookup_dict = {}
    try:
        with open(lookup_file, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dstport = row['dstport'].strip()
                protocol = row['protocol'].strip().lower()
                tag = row['tag'].strip()
                if not dstport or not protocol or not tag:
                    continue
                key = (int(dstport), protocol)
                lookup_dict[key] = tag
    except FileNotFoundError:
        print(f"error: lookup file '{lookup_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"error reading lookup file: {e}")
        sys.exit(1)
    return lookup_dict

def get_protocol_name(protocol_number):
    """
    get protocol name from number using PROTOCOL_MAP
    """
    return PROTOCOL_MAP.get(protocol_number, str(protocol_number).lower())

def process_flow_logs(flow_log_file, lookup_dict):
    """
    process flow logs and count tags and port/protocol
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    try:
        with open(flow_log_file, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 14:
                    print(f"warning: line {line_number} malformed. skipping.")
                    continue
                try:
                    dstport = int(parts[5])
                    protocol_num = int(parts[7])
                    protocol = get_protocol_name(protocol_num)
                except ValueError:
                    print(f"warning: line {line_number} invalid port/protocol. skipping.")
                    continue

                port_protocol_key = (dstport, protocol)
                port_protocol_counts[port_protocol_key] += 1

                tag = lookup_dict.get(port_protocol_key, 'Untagged')
                tag_counts[tag] += 1
    except FileNotFoundError:
        print(f"error: flow log file '{flow_log_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"error processing flow log file: {e}")
        sys.exit(1)

    return tag_counts, port_protocol_counts

def write_tag_counts(output_file, tag_counts):
    """
    write tag counts to csv
    """
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Tag', 'Count'])
            for tag, count in sorted(tag_counts.items()):
                writer.writerow([tag, count])
        print(f"tag counts written to '{output_file}'.")
    except Exception as e:
        print(f"error writing tag counts: {e}")

def write_port_protocol_counts(output_file, port_protocol_counts):
    """
    write port/protocol counts to csv
    """
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Port', 'Protocol', 'Count'])
            for (port, protocol), count in sorted(port_protocol_counts.items(), key=lambda x: (x[0][0], x[0][1])):
                writer.writerow([port, protocol, count])
        print(f"port/protocol counts written to '{output_file}'.")
    except Exception as e:
        print(f"error writing port/protocol counts: {e}")