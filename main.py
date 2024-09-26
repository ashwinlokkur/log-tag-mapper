import sys
import flow_log_parser as parser

def main():
    """
    main function
    """
    flow_log_file = sys.argv[1] if len(sys.argv) > 1 else 'flow_logs.txt'
    lookup_csv_file = sys.argv[2] if len(sys.argv) > 2 else 'lookup_table.csv'

    print("loading lookup table...")
    lookup_dict = parser.load_lookup_table(lookup_csv_file)
    
    print("processing flow logs...")
    tag_counts, port_protocol_counts = parser.process_flow_logs(flow_log_file, lookup_dict)

    print("writing output files...")
    parser.write_tag_counts('tag_counts.csv', tag_counts)
    print("tag counts written to 'tag_counts.csv'.")
    parser.write_port_protocol_counts('port_protocol_counts.csv', port_protocol_counts)
    print("port protocol counts written to 'port_protocol_counts.csv' ")

    print("processing completed.")

if __name__ == "__main__":
    main()