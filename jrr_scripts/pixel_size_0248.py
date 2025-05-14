import omero
from omero.gateway import BlitzGateway

# Replace with your OMERO connection details
hostname = 'your_omero_server'
port = 4064
username = 'your_username'
password = 'your_password'
dataset_id = 123  # Change to value asked to user of provided in CLI

# Define the new pixel size values (in microns, for example)
new_pixel_size_x = 0.0248
new_pixel_size_y = 0.0248
new_pixel_size_z = 1.0

conn = None
try:
    # Connect to OMERO
    conn = BlitzGateway(username, password, host=hostname, port=port)
    conn.connect()

    # Get the Dataset
    dataset = conn.getObject('Dataset', dataset_id)
    if not dataset:
        print(f"Dataset with ID {dataset_id} not found.")
        exit()

    # Iterate through the Images in the Dataset
    for image in dataset.listChildren():
        print(f"Processing Image: {image.getName()}")
        pixels = image.getPrimaryPixels()
        if pixels:
            # Get the existing PhysicalSizeX, PhysicalSizeY, and PhysicalSizeZ objects
            physical_size_x = pixels.getPhysicalSizeX(unit=None)
            physical_size_y = pixels.getPhysicalSizeY(unit=None)
            physical_size_z = pixels.getPhysicalSizeZ(unit=None)

            # Check if the physical sizes are already set (can be None)
            if physical_size_x is not None:
                physical_size_x.setValue(new_pixel_size_x)
                pixels.setPhysicalSizeX(physical_size_x)
            else:
                pixels.setPhysicalSizeX(new_pixel_size_x)

            if physical_size_y is not None:
                physical_size_y.setValue(new_pixel_size_y)
                pixels.setPhysicalSizeY(physical_size_y)
            else:
                pixels.setPhysicalSizeY(new_pixel_size_y)

            if physical_size_z is not None:
                physical_size_z.setValue(new_pixel_size_z)
                pixels.setPhysicalSizeZ(physical_size_z)
            else:
                pixels.setPhysicalSizeZ(new_pixel_size_z)

            # Save the changes to the Pixels object
            pixels.save()
            print(f"  Pixel size updated for Image: {image.getName()}")
        else:
            print(f"  No Pixels object found for Image: {image.getName()}")

    print("Pixel size update process complete for all images in the dataset.")

except omero.SecurityViolation as sve:
    print(f"Authentication error: {sve}")
except omero.ClientError as ce:
    print(f"OMERO client error: {ce}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the connection
    if conn and conn.isConnected():
        conn.close()