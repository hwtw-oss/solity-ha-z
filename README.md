# Solity LAVO Smart Lock Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant integration for Solity LAVO electronic smart locks.

## Features

- **Lock Control** - Lock and unlock your door remotely
- **Battery Monitoring** - Track battery level of your lock
- **Gateway Status** - Monitor gateway connection status
- **Device Information** - View model, firmware version, and more

## Supported Devices

- Solity LAVO LC-750B/01
- Other Solity smart locks with cloud connectivity

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/hpware/solity-ha` with category "Integration"
6. Click "Add"
7. Search for "Solity" and install

### Manual Installation

1. Download the latest release from GitHub
2. Copy the `custom_components/solity` folder to your `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Solity"
4. Enter your Solity account email and password
5. Your locks will be automatically discovered

## Entities

For each lock, the integration creates:

| Entity | Type | Description |
|--------|------|-------------|
| Lock | `lock` | Control lock/unlock state |
| Battery | `sensor` | Battery level percentage |

## Services

The integration supports standard Home Assistant lock services:

- `lock.lock` - Lock the door
- `lock.unlock` - Unlock the door
- `lock.open` - Open the door (same as unlock)

## API Documentation

This integration uses the Solity Smart Lock cloud API. The API was reverse engineered from the official Android app.

### API Endpoints

- `POST /login` - Authentication
- `GET /myDevice` - List devices
- `PUT /controlDevice/{id}` - Control device (lock/unlock/status)
- `GET /retrieveLog/page/{id}` - Get activity logs

### BLE Support (Future)

The integration is designed to support future BLE (Bluetooth Low Energy) direct control:

- Write UUID: `48400002-B5A3-F393-E0A9-E50E24DCCA9E`
- Notify UUID: `48400003-B5A3-F393-E0A9-E50E24DCCA9E`

## Troubleshooting

### "Unable to connect to Solity servers"

- Check your internet connection
- Verify your credentials in the Solity app
- The Solity servers may be temporarily unavailable

### Lock shows as unavailable

- Ensure your gateway is powered on and connected
- Check the gateway connection status in the Solity app
- The lock may be out of range of the gateway

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not affiliated with or endorsed by Solity. Use at your own risk.

## Credits

- Reverse engineering research: [hpware/reverse_engineering](https://github.com/hpware/reverse_engineering/tree/master/LAVO)
- Integration template: [ludeeus/integration_blueprint](https://github.com/ludeeus/integration_blueprint)
