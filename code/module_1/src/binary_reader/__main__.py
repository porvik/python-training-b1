import argparse
import sys
import binary_reader.configuration as configuration
import binary_reader.inp as inp
import pprint
import binary_reader.output as output


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--config', help='Data config / structure spec')
    arg_parser.add_argument('-i', '--input-data', help='Input data')
    args = arg_parser.parse_args(sys.argv[1:])

    print('args: config {}: input_data: {}'.format(args.config, args.input_data))

    inp.Debug.global_log_level = 1

    if args.config.endswith(".json"):
        conf = configuration.JsonConfiguration(args.config)
    else:
        conf = configuration.XmlConfiguration(args.config)
    print('config {}'.format(conf.get_root().packet.header.attribute))

    reader_data = inp.Reader().read_files(args.input_data, conf.get_root().packet)
    pprint.pprint(reader_data)

    visualizer = output.Visualizer().print_text(reader_data)

    output.Exporter.export_to_xlsx(reader_data)

if __name__ == '__main__':
    main()