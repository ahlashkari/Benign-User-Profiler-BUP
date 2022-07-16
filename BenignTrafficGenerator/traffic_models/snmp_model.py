#!/usr/bin/env python3

from pysnmp import hlapi
from pysnmp.hlapi import *
from .traffic_model import TrafficModel


class SNMPModel(TrafficModel):
    def __init__(self, model_config: dict):
        self.__model_config = model_config

    def generate(self) -> None:
        host = self.__model_config["host"]
        port = self.__model_config["port"] if "port" in self.__model_config else 22
        get_list = self.__model_config["get_list"]
        set_list = self.__model_config["set_list"]

        # credentials
        hlapi.CommunityData('ICTSHORE'))
        # v3
        hlapi.UsmUserData('testuser', authKey='authenticationkey', privKey='encryptionkey',
                authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)

        oid = '1.3.6.1.2.1.74.1.30190.1.1.1.0'
        print(self.get('localhost', [oid], hlapi.CommunityData('private')))
        self.set('localhost', {oid: Unsigned32(10)}, hlapi.CommunityData('private'))

    def construct_object_types(self, list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types


    def fetch(self, handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = self.cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
            except StopIteration:
                break
        return result


    def cast(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value


    def get(self, target, oids, credentials, port=161, engine=hlapi.SnmpEngine(),
            context=hlapi.ContextData()):
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *self.construct_object_types(oids)
        )
        return self.fetch(handler, 1)[0]


    def construct_value_pairs(self, list_of_pairs):
        pairs = []
        for key, value in list_of_pairs.items():
            pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
        return pairs


    def set(self, target, value_pairs, credentials, port=161, engine=hlapi.SnmpEngine(),
            context=hlapi.ContextData()):
        handler = hlapi.setCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *self.construct_value_pairs(value_pairs)
        )
        return self.fetch(handler, 1)[0]
