import omero
from omero.gateway import BlitzGateway

import yaml
import sys

# OMERO connection details
hostname = 'localhost'
port = 4064
with open('/home/jrr/Documents/docker-example-omero/jrr_scripts/secret.yaml', 'r') as file:
    credentials = yaml.safe_load(file)
username = credentials.get('USER1')
password = credentials.get('PASSWORD1')

# Read dataset ID from stdin
try:
    dataset_id = int(input("Enter the Dataset ID: "))
except ValueError:
    print("Invalid input. Please enter a numeric Dataset ID.")
    sys.exit(1)

# Define the new pixel size 
new_pixel_size = omero.model.LengthI(24.8, omero.model.enums.UnitsLength.NANOMETER)

conn = None
try:
    # Connect to OMERO
    conn = BlitzGateway(username, password, host=hostname, port=port)
    conn.connect()

    # Get the dataset
    dataset = conn.getObject('Dataset', dataset_id)
    if not dataset:
        print(f"Dataset with ID {dataset_id} not found.")
        exit()

    # Show dataset info
    print(f'User: {conn.getUser().getFullName()}')
    print(f'Dataset group: {dataset.getDetails().getGroup().getName()}')
    project = dataset.getParent()
    if project:
        print(f'Dataset project: {project.getName()}')
    else:
        print('Dataset is not associated with any project.')
    print(f'Dataset name: {dataset.getName()}')
    
    # Warn the user about the pixel size modification
    confirmation = input(f"Warning: The pixel size for Dataset ID {dataset_id} will be modified to 24.8 nm. Continue? [y,N]: ").strip().lower()
    if confirmation != 'y':
        print("Operation canceled by the user.")
        sys.exit(0)


    # Change pixel size in all the dataset
    for image in dataset.listChildren():
        print(f"Processing Image: {image.getName()}")
        pixels = image.getPrimaryPixels()
        if pixels:
            # Get the existing PhysicalSizeX
            physical_size_x = pixels.getPhysicalSizeX()
            physical_size_y = pixels.getPhysicalSizeY()

            # Update the values to 24.8 nm       
            pixels.setPhysicalSizeX(new_pixel_size)
            pixels.setPhysicalSizeY(new_pixel_size)

            # Save the changes
            pixels.save()
            

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