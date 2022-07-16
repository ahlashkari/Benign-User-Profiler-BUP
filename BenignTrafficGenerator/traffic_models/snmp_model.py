#!/usr/bin/env python3

from pysnmp import hlapi
from pysnmp.hlapi import *
from .traffic_model import TrafficModel


class SNMPModel(TrafficModel):
    def __init__(self, model_config: dict):
        self.__model_config = model_config

    def generate(self) -> None:
        host = self.__model_config["host"]
        credential = self.__model_config["credential"] if "credential" in self.__model_config else None
        get_list = self.__model_config["get_list"]
        set_list = self.__model_config["set_list"]

        # TODO: check for deleting other version than v3
        if credential is not None:
            if credential["version"] == "v3":
                hlapi.UsmUserData(credential["username"],
                                  authKey=credential["auth_key"],
                                  privKey=credential["private_key"],
                                  authProtocol=hlapi.usmHMACSHAAuthProtocol,
                                  privProtocol=hlapi.usmAesCfb128Protocol)
            else:
                hlapi.CommunityData(credential["community"]))

        for get_command in get_list:
            self.get(get_command["host"],
                    [get_command["oid"]],
                    hlapi.CommunityData(get_command["community"]))

        for set_command in set_list:
            self.set(set_command["host"],
                    {set_command["oid"]: self.get_ASN_value(set_command["type"],
                                                            set_command["value"])},
                    hlapi.CommunityData(set_command["community"]))

    def get_ASN_value(self, str_type, value):
        if str_type == "Unsigned32":
            return Unsigned32(value)

        if str_type == "Integer32":
            return Integer32(value)

        if str_type == "DisplayString":
            return DisplayString(value)

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
