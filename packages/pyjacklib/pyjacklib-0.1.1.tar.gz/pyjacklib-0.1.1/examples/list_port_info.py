#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import jacklib
from jacklib.helpers import c_char_p_p_to_list, get_jack_status_error_string


status = jacklib.jack_status_t()
client = jacklib.client_open("list-port-info", jacklib.JackNoStartServer, status)
err = get_jack_status_error_string(status)

if status.value:
    if status.value & jacklib.JackNameNotUnique:
        print("Non-fatal JACK status: %s" % err, file=sys.stderr)
    elif status.value & jacklib.JackServerStarted:
        # Should not happen, since we use the JackNoStartServer option
        print("Unexpected JACK status: %s" % err, file=sys.stderr)
    else:
        sys.exit("Error connecting to JACK server: %s" % err)

for portname in c_char_p_p_to_list(jacklib.get_ports(client)):
    port = jacklib.port_by_name(client, portname)
    uuid = jacklib.port_uuid(port)

    print("Port name: %s\nUUID: %s" % (portname, uuid))
    num_aliases, *aliases = jacklib.port_get_aliases(port)
    if num_aliases:
        print("Aliases: %s" % ", ".join(aliases[:num_aliases]))

    pretty_name = jacklib.get_port_pretty_name(client, portname)
    if pretty_name:
        print("Pretty-name: {}".format(pretty_name))

    props = jacklib.get_port_properties(client, portname)
    if props:
        print("Properties:")
        for prop in props:
            print(" * {}: {} (type: {})".format(prop.key, prop.value, prop.type))

    print('')

jacklib.client_close(client)
