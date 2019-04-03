#!/usr/bin/env python3
"""Query ASF catalog with SNWE bounds or vector file.

Author: Scott Henderson
Date: 10/2017
"""

import argparse
import dinosar.archive.asf as asf
import sys


def cmdLineParse():
    """Command line parser."""
    parser = argparse.ArgumentParser(description='get_inventory_asf.py')
    parser.add_argument('-r', type=float, nargs=4, dest='roi', required=False,
                        metavar=('S', 'N', 'W', 'E'),
                        help='Region of interest bbox [S,N,W,E]')
    parser.add_argument('-i', type=str, dest='input', required=False,
                        help='Polygon vector file defining region of interest')
    parser.add_argument('-b', type=float, dest='buffer', required=False,
                        help='Add buffer [in degrees]')
    parser.add_argument('-f', action='store_true', default=False,
                        dest='footprints', required=False,
                        help='Create subfolders with geojson footprints')
    parser.add_argument('-o', type=str, dest='orbit', required=False, default=None,
                        help='relativeOrbit number')
    parser.add_argument('-k', action='store_true', default=False, dest='kmls',
                        required=False,
                        help='Download kmls from ASF API')
    parser.add_argument('-c', action='store_true', default=False, dest='csvs',
                        required=False,
                        help='Download csvs from ASF API')
    parser.add_argument('-m', action='store_true', default=False, dest='meta',
                        required=False,
                        help='Download metalink from ASF API')
    parser.add_argument('-L', '--processingLevel', default='L1.0',
                        help='Processing level for search (L1.0 is raw not SLC)')

    return parser


def main(parser):
    """Run as a script with args coming from argparse."""
    args = parser.parse_args()
    if not (args.roi or args.input):
        print("ERROR: requires '-r' or '-i' argument")
        parser.print_help()
        sys.exit(1)

    if args.input:
        args.roi = asf.ogr2snwe(args.input, args.buffer)

    asf.snwe2file(args.roi)
    asf.query_asf(args.roi, 'ALOS', orbit=args.orbit, processingLevel=args.processingLevel, beam=None)
    gf = asf.load_asf_json('query_ALOS.json')
    asf.summarize_inventory(gf)
    asf.summarize_orbits(gf)
    asf.save_inventory(gf)
    if args.csvs:
        asf.query_asf(args.roi, 'ALOS', 'csv', orbit=args.orbit)
    if args.kmls:
        asf.query_asf(args.roi, 'ALOS', 'kml', orbit=args.orbit)
    if args.meta:
        asf.query_asf(args.roi, 'ALOS', 'metalink', orbit=args.orbit)
    if args.footprints:
        asf.save_geojson_footprints(gf)


if __name__ == '__main__':
    parser = cmdLineParse()
    main(parser)
