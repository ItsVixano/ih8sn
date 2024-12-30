#!/usr/bin/env python3

import json
from urllib.error import URLError
from urllib.request import urlopen


def get_build_description(build_fingerprint: str) -> str:
    if not build_fingerprint:
        return ''

    try:
        parts = build_fingerprint.replace(':', '/').split('/')

        if len(parts) < 7:
            return ''

        # Extract components
        device = parts[1]
        build_type = parts[6]
        version = parts[3]
        build_number = parts[4]
        build_id = parts[5]
        keys = parts[7]

        return (
            f'{device}-{build_type} {version} {build_number} {build_id} {keys}'
        )

    except (IndexError, AttributeError):
        return ''


def fetch_and_convert():
    url = 'https://play.leafos.org'
    try:
        with urlopen(url) as response:
            device = json.loads(response.read())

        ih8sn_config = 'system/etc/ih8sn.conf'

        fingerprint = device.get('FINGERPRINT', '')
        build_description = get_build_description(fingerprint)

        config = {
            'BUILD_FINGERPRINT': fingerprint,
            'BUILD_DESCRIPTION': build_description,
            'MANUFACTURER_NAME': device.get('MANUFACTURER', ''),
            'PRODUCT_BRAND': device.get('BRAND', ''),
            'PRODUCT_DEVICE': device.get('DEVICE', ''),
            'PRODUCT_MODEL': device.get('MODEL', ''),
            'PRODUCT_NAME': device.get('PRODUCT', ''),
        }

        with open(ih8sn_config, 'w') as f:
            for key, value in config.items():
                if value:
                    f.write(f'{key}={value}\n')

    except URLError as e:
        print(f'Error fetching data: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON: {e}')


if __name__ == '__main__':
    fetch_and_convert()
