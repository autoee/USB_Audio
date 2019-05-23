from universal_serial_bus.orm.usb20.descriptors import *
from .descriptors import *
from .formats.descriptors import *
from .. import UACdevice


int_eq_hex = OrmClassBase.int_eq_hex
int_to_hex = OrmClassBase.int_to_hex



class UACdevice(UACdevice):

    @classmethod
    def _categorize(cls, descriptor, intf_type = None):

        _class = None

        if int_eq_hex(descriptor[1], '01'):  # 如果是 device
            _class = StandardDeviceDescriptor

        if int_eq_hex(descriptor[1], '02'):  # 如果是 config
            _class = StandardConfigurationDescriptor

        if int_eq_hex(descriptor[1], '05'):  # 如果是 endpoint
            if intf_type == "HID":
                _class = StandardEndpointDescriptor

            if intf_type == "AS":
                _class = StandardAsIsochronousAudioDataEndpointDescriptor

        if int_eq_hex(descriptor[1], '04'):  # 如果是 interface

            _class = StandardInterfaceDescriptor

            if int_eq_hex(descriptor[5], '03'):  # 如果是 HID
                intf_type = "HID"

            if int_eq_hex(descriptor[5], '01'):  # 如果是 audio
                if int_eq_hex(descriptor[6], '01'):  # 如果是 AC interface
                    intf_type = "AC"
                if int_eq_hex(descriptor[6], '02'):  # 如果是 AC interface
                    intf_type = "AS"

        if int_eq_hex(descriptor[1], '24'):  # 如果是 CS_INTERFACE
            if intf_type == "AC":
                _classes = {'00': None,
                            '01': ClassSpecificAcInterfaceHeaderDescriptor,
                            '02': InputTerminalDescriptor,
                            '03': OutputTerminalDescriptor,
                            '04': MixerUnitDescriptor,
                            '05': SelectorUnitDescriptor,
                            '06': FeatureUnitDescriptor,
                            '07': 'EFFECT_UNIT',
                            '08': 'PROCESSING_UNIT',
                            '09': ExtensionUnitDescriptor,
                            '0A': ClockSourceDescriptor,
                            '0B': ClockSelectorDescriptor,
                            '0C': ClockMultiplierDescriptor,
                            '0D': SamplingRateConverterUnitDescriptor}

                _class = _classes[int_to_hex(descriptor[2])]

            if intf_type == "AS":
                _classes = {'00': None,
                            '01': ClassSpecificAsInterfaceDescriptor,
                            '02': TypeIFormatTypeDescriptor,
                            '03': EncoderDescriptor,
                            '04': 'DECODER'}

                _class = _classes[int_to_hex(descriptor[2])]

        if int_eq_hex(descriptor[1], '25'):  # 如果是 CS_ENDPOINT
            if intf_type == "AC":
                pass

            if intf_type == "AS":
                _classes = {'00': None,
                            '01': ClassSpecificAsIsochronousAudioDataEndpointDescriptor}

                _class = _classes[int_to_hex(descriptor[2])]

        return _class, intf_type
