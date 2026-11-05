import sounddevice as sd

print("AVAILABLE AUDIO DEVICES")
print("=" * 40)

for i, device in enumerate(sd.query_devices()):
    if device["max_input_channels"] > 0:
        print(f"Device {i}: {device['name']}")
        print(f"Input channels: {device['max_input_channels']}")
        print("-" * 40)