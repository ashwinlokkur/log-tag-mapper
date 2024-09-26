# Flow Log Parser and Tag Mapper for Illumio

## TLDR


```bash
python main.py
```
OR
```bash
python main.py <path_to_flow_logs.txt> <path_to_lookup_table.csv>
```

## Requirements

No external libraries are required for this project, ensuring it can run in any Python environment without additional dependencies.

## Assumptions

- The program only supports flow logs in the default AWS VPC format (version 2).
- The lookup table CSV contains port numbers and protocols, and the protocol names are case-insensitive.
- Protocol numbers in flow logs are mapped to names (e.g., `6 -> tcp`, `17 -> udp`) using the `PROTOCOL_MAP` from `protocol_map.py`.
- Rows in flow logs that don't match the lookup table are assigned the tag "Untagged."
- The flow log file is assumed to be up to 10 MB in size, and the lookup table can have up to 10,000 mappings.
- The `dstport` and `protocol_num` fields in both flow logs and the lookup table are valid integers; entries with non-integer values are skipped with a warning.

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ashwinlokkur/log-tag-mapper.git
    cd illumio-flow-log-parser
    ```

2. **Place the `lookup_table.csv` and `flow_logs.txt` files into the project directory:**
   - The `lookup_table.csv` contains the mapping of port, protocol, and tag.
   - The `flow_logs.txt` contains the flow log data in the default AWS format.

3. **Run the program:**

    ```
    python main.py <path_to_flow_logs> <path_to_lookup_table>
    ```

4. **Check the output files:**
   - `tag_counts.csv`: contains the counts of each tag.
   - `port_protocol_counts.csv`: contains the counts for each port/protocol combination.

## Sample Input

### lookup_table.csv

```csv
dstport,protocol,tag
25,tcp,sv_P1
443,tcp,sv_P2
23,tcp,sv_P1
110,tcp,email
993,tcp,email
143,tcp,email
68,udp,sv_P2
22,tcp,sv_P4
3389,tcp,sv_P5
```

### flow_logs.txt

```yaml
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK
2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 49155 6 10 8000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-7i8j9k0l 172.16.0.101 192.0.2.203 993 49157 6 8 5000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-6m7n8o9p 10.0.2.200 198.51.100.4 143 49158 6 18 14000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-1a2b3c4d 192.168.0.1 203.0.113.12 1024 80 6 10 5000 1620140661 1620140721 ACCEPT OK
2 123456789012 eni-1a2b3c4d 203.0.113.12 192.168.0.1 80 1024 6 12 6000 1620140661 1620140721 ACCEPT OK
2 123456789012 eni-1a2b3c4d 10.0.1.102 172.217.7.228 1030 443 6 8 4000 1620140661 1620140721 ACCEPT OK
```
