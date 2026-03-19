from matplotlib import transforms
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import serial
import time
import webbrowser



# Serial port configuration
SERIAL_PORT = 'COM7'  # Change as needed
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
# Reset train to initial positions
positions = [(0, 3.6, 0), (10.5, 3.6, 0), (21, 3.6, 0)]


# Set up figure and axes
fig, ax = plt.subplots(figsize = (6,6))
ax.set_xlim(0, 130)  # Increased limits to accommodate train before READER1
ax.set_ylim(0, 25)

ax.set_aspect('equal')
mng = plt.get_current_fig_manager()
mng.window.state('zoomed') 

def train_start():
    time.sleep(8)
    positions = [(0, 3.6, 0), (10.5, 3.6, 0), (21, 3.6, 0)]


# Draw U-turn track
#ax.add_patch(patches.Arc((65, 12.5), 20, 15, theta1=90, theta2=180, color='gray', linewidth=6))
#ax.add_patch(patches.Arc((65, 12.5), 16, 11, theta1=90, theta2=180, color='gray', linewidth=6))
ax.add_patch(patches.Arc((20, 15), 60, 30, theta1=336, theta2=350, color='gray', linewidth=6))
ax.add_patch(patches.Arc((26, 13), 60, 30, theta1=336, theta2=352, color='gray', linewidth=6))
ax.add_patch(patches.Arc((51.7, 6.52), 10, 10, theta1=80, theta2=150, color='gray', linewidth=6))
ax.add_patch(patches.Arc((26, 13), 60, 30, theta1=336, theta2=336.1, color='gray', linewidth=6))
ax.add_patch(patches.Arc((56, 8), 3, 3, theta1=90, theta2=170, color='gray', linewidth=6))

# Draw extended straight tracks
ax.plot([0, 90], [11.5, 11.5], color='gray', linewidth=6)
ax.plot([0, 90], [9.5, 9.5], color='gray', linewidth=6)
#ax.plot([0, 15], [5, 5], color='gray', linewidth=6)
ax.plot([0, 90], [3, 3], color='gray', linewidth=6)
ax.plot([0, 90], [5, 5], color='gray', linewidth=6)

# RFID tag positions
rfid_positions = {
    "Reader1": (40, 2),
    "Reader3": (60, 2),
    "Reader2": (60, 14)
}
rfid_tags = {key: patches.Circle(pos, radius=0.5, color='red') for key, pos in rfid_positions.items()}
for tag in rfid_tags.values():
    ax.add_patch(tag)

import numpy as np

#def get_circular_positions(center_x, center_y, radius, start_angle, end_angle, num_cars):
   # angles = np.linspace(np.radians(start_angle), np.radians(end_angle), num_cars)
   # positions = [(radius * np.cos(a) + center_x, radius * np.sin(a) + center_y, np.degrees(a) - 90) for a in angles]
#return positions


# # Train car dimensions
# car_width, car_height = 2.2, 0.7

# # Positions of train cars
# positions = [(2, 3.6), (5, 3.6), (8, 3.6)]

# # Plot train cars
# for x, y in positions:
#     rect = patches.Rectangle((x, y), car_width, car_height, color='blue')
#     ax.add_patch(rect)

# # Plot chains (lines between cars)
# for i in range(len(positions) - 1):
#     x1, y1 = positions[i][0] + car_width, positions[i][1] + car_height / 2
#     x2, y2 = positions[i+1][0], positions[i+1][1] + car_height / 2
#     ax.plot([x1, x2], [y1, y2], color='black', linewidth=2)

# Train car dimensions
car_width, car_height = 10, 0.7  # Increased car width to make train longer

# Positions of train cars before READER1
positions = [(0, 3.6,0), (10.5, 3.6,0), (21, 3.6,0)]  # Shifted train to start before READER1



# Plot train cars
train_parts = []
for x, y,theta in positions:
    rect = patches.Rectangle((x, y), car_width, car_height, color='blue')
    ax.add_patch(rect)
    train_parts.append(rect)

# Plot chains (lines between cars)
chains = []
for i in range(len(positions) - 1):
    x1, y1 = positions[i][0] + car_width, positions[i][1] + car_height / 2
    x2, y2 = positions[i+1][0], positions[i+1][1] + car_height / 2
    line, = ax.plot([x1, x2], [y1, y2], color='black', linewidth=2)
    chains.append(line)

# Labels for RFID readers and train
for name, pos in rfid_positions.items():
    ax.text(pos[0], pos[1] - 1.5, name, fontsize=10, ha='center', color='black')
ax.legend(loc="upper right")
rfid_status = ax.text(0.5, 23, "", fontsize=10, color="green")

# Read RFID data from serial

def read_rfid():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Received: {line}")
        return line
    return ""

# def reset_train():
#     """ Reset train to the starting position after completing a cycle. """
#     global previous_reader, prev_tag
#     print("Restarting cycle... Resetting train to start position.")
    
#     previous_reader = None
#     prev_tag = None

#     # Force update to ensure first detection is displayed
#     rfid_status.set_text("Cycle restarted. Waiting for first detection...")
#     rfid_status.set_color("blue")
#     plt.pause(0.5)  # Small delay for UI update
#         # Reset train to initial positions
#     positions = [(13, 3.6), (23.5, 3.6), (34, 3.6)]
#     chain_positions = [((23, 3.95), (23.5, 3.95)), ((33.5, 3.95), (34, 3.95))]

    
for i, (x, y, theta) in enumerate(positions):
    train_parts[i].set_xy((x, y))
    trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
    train_parts[i].set_transform(trans)



# Update function
# global previous_reader 
# global prev_tag
previous_reader = None
prev_tag=None

def update(detected):
    global previous_reader 
    global prev_tag
   # print(prevreader)
    if detected and ':' in detected:
        reader, tag = detected.split(':')
        reader, tag = reader.strip(), tag.strip()
        print("reader: "+reader+"   tag:"+tag)
        print(f"Current Reader: {reader}, Tag: {tag}, Previous Reader: {previous_reader},prev_tag: {prev_tag}")
        
        # Reset tag colors
        for r in rfid_tags.values():
            r.set_color("red")
        # print(train_parts)  # Check what is actually inside
        for part in train_parts:
            print(f"Type: {type(part)}, Value: {part}")

        for part in train_parts:
            # print(type(part))
            part.set_color("blue")
       
        # # Position the train based on detected tag
        # if reader in rfid_positions and tag in ["Tag1", "Tag2"]:
        #     x, y = rfid_positions[reader]
        #     train_x = x - car_width*2
        #     train_y = y + 1.5 if tag == "Tag1" else y - car_height + 1.5

        #     # Move all train parts
        #     for i, part in enumerate(train_parts):
        #         part.set_xy((train_x + i * car_width, train_y))
        #     # Move all chains
        #     for i, line in enumerate(chains):
        #         x1, y1 = train_parts[i].get_x() + car_width, train_parts[i].get_y() + car_height / 2
        #         x2, y2 = train_parts[i+1].get_x(), train_parts[i+1].get_y() + car_height / 2
        #         line.set_data([x1, x2], [y1, y2])


# Position the train based on detected tag
        if reader == "Reader1" and tag == "Tag1" and (previous_reader is None or prev_tag is None):

            # Assign absolute positions

            positions = [(13, 3.6), (23.5, 3.6), (34, 3.6)]
            chain_positions = [((23, 3.95), (23.5, 3.95)), ((33.5, 3.95), (34, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

            #  # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

        #fs exiting main path
        elif reader == "Reader1" and tag == "Tag2" and previous_reader=="Reader2" and prev_tag=="Tag1":
            # Assign absolute positions
            positions = [(36,3.6 ,0), (45.5, 7.1,40), (55.2, 10.5,0)]
            chain_positions = [((46, 3.95), (46.5, 4.3)), ((54.4, 10.7), (55.2, 10.7))]
            
            # Move all train parts
            for i, (x, y,theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
                trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
                train_parts[i].set_transform(trans)
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center', color='white')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

        #bs 2 step
        elif reader == "Reader1" and tag == "Tag1" and previous_reader=="Reader2" and prev_tag=="Tag1":
            # Assign absolute positions
            positions = [(36,3.6 ,0), (45.5, 7.1,40), (55.2, 10.5,0)]
            chain_positions = [((46, 3.95), (46.5, 4.3)), ((54.4, 10.7), (55.2, 10.7))]
            
            # Move all train parts
            for i, (x, y,theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
                trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
                train_parts[i].set_transform(trans)
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center', color='white')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[0 if tag == "Tag1" else -1].set_color("green")
            train_parts[2 if tag == "Tag2" else -1].set_color("blue")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

        #fs step2
        elif reader == "Reader2" and tag == "Tag1" and previous_reader=="Reader1"and  prev_tag=="Tag1":
            # Assign absolute positions
            #positions = get_circular_positions(55, 12.5, 10, 180, 90, len(train_parts))

            positions = [(34,3.6 ,0), (43.4, 6.8,40), (52.7, 10.2,0)]
            chain_positions = [((44, 3.95), (44.5, 3.95)), ((52.2, 10.4), (52.7, 10.4))]
            
            # Move all train parts
            for i, (x, y,theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
                trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
                train_parts[i].set_transform(trans)
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

#bs 2 step
        elif reader == "Reader2" and tag == "Tag2" and previous_reader == "Reader1" and prev_tag == "Tag1":
            # Assign absolute positions
            positions = [(34, 3.6, 0), (43.4, 6.8, 40), (52.7, 10.2, 0)]
            chain_positions = [((44, 3.95), (44.5, 3.95)), ((52.2, 10.4), (52.7, 10.4))]

            # Move all train parts
            for i, (x, y, theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
                trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
                train_parts[i].set_transform(trans)

            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

            # Update Tag Labels with corrected colors
            # tag_positions = [(train_parts[0].get_x() + car_width / 2, train_parts[0].get_y() + 1),
            #                 (train_parts[2].get_x() + car_width / 2, train_parts[2].get_y() + 1)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center', color='white')

            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            
            # Set correct colors for train boogies
            train_parts[0].set_color("blue")  # First boogie turns green
            train_parts[1].set_color("blue")   # Middle boogie stays blue
            train_parts[2].set_color("green")   # Reset last boogie if necessary

            # Update status text
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")


#bs first step
        elif reader == "Reader2" and tag == "Tag1" and previous_reader is None:
            positions = [(56.4, 10.2,0), (66.9, 10.2,0), (77.4, 10.2,0)]
            chain_positions = [((66.4, 10.6), (66.9, 10.6)), ((76.8, 10.6), (77.3, 10.6))]
            
            # Move all train parts
            for i, (x, y,theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")

            # Ensure the correct train boogie turns green
            if tag == "Tag1":
                train_parts[0].set_color("green")  # Last boogie turns green for Tag1
            elif tag == "Tag2":
                train_parts[2].set_color("green")  # First boogie turns green for Tag2

            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

#bs last step bs last step
        elif reader == "Reader1" and tag == "Tag2" and (previous_reader=="Reader2" or previous_reader=="Reader3") and prev_tag=="Tag2":
            # Assign absolute positions
            positions = [(13, 3.6,0), (23.5, 3.6,0), (34, 3.6,0)]
            chain_positions = [((23, 3.95), (23.5, 3.95)), ((33.5, 3.95), (34, 3.95))]
            
            # Move all train parts
            for i, (x, y, theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
                trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
                train_parts[i].set_transform(trans)
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("green")
            train_parts[0 if tag == "Tag2" else -1].set_color("blue")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")
            

        elif reader == "Reader3" and tag == "Tag1" and previous_reader == "Reader1":
            # Assign absolute positions
            positions = [(34, 3.6), (44.5, 3.6), (55, 3.6)]
            chain_positions = [((44, 3.95), (44.5, 3.95)), ((54.6, 3.95), (54.9, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

        elif reader == "Reader3" and tag == "Tag1" and previous_reader is None and prev_tag is None:
            # Assign absolute positions
            positions = [(56, 3.6), (66.5, 3.6), (77, 3.6)]
            chain_positions = [((66, 3.95), (66.5, 3.95)), ((76.5, 3.95), (77, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
          #  train_parts[2 if tag == "Tag1" else -1].set_color("green")
            train_parts[0].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

        elif reader == "Reader1" and tag == "Tag1" and previous_reader=="Reader3" and prev_tag=="Tag1":
            # Assign absolute positions
            positions = [(36, 3.6), (46.5, 3.6), (57, 3.6)]
            chain_positions = [((46, 3.95), (46.5, 3.95)), ((56.5, 3.95), (57, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
          #  train_parts[2 if tag == "Tag1" else -1].set_color("green")
            train_parts[0].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")

        elif reader == "Reader1" and tag == "Tag2" and previous_reader =="Reader3" and prev_tag=="Tag1":
            # Assign absolute positions
            positions = [(38, 3.6), (48.5, 3.6), (59, 3.6)]
            chain_positions = [((48, 3.95), (48.5, 3.95)), ((58.5, 3.95), (59, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")
        elif reader == "Reader3" and tag == "Tag2" and previous_reader == "Reader1" and prev_tag=="Tag1":
            # Assign absolute positions
            positions = [(32, 3.6), (42.5, 3.6), (53, 3.6)]
            chain_positions = [((42, 3.95), (42.5, 3.95)), ((52.5, 3.95), (53, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("green")
            train_parts[0 if tag == "Tag2" else -1].set_color("blue")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")
        elif reader == "Reader2" and tag == "Tag2" and previous_reader=="Reader1"  and prev_tag=="Tag2":
            # Assign absolute positions
            positions = [(56.4, 10.2,0), (66.9, 10.2,0), (77.4, 10.2,0)]
            chain_positions = [((66.4, 10.6), (66.9, 10.6)), ((76.8, 10.6), (77.3, 10.6))]
            
            
            # Move all train parts
            for i, (x, y, theta) in enumerate(positions):
                train_parts[i].set_xy((x, y))
                trans = transforms.Affine2D().rotate_deg_around(x + car_width / 2, y + car_height / 2, theta) + ax.transData
                train_parts[i].set_transform(trans)
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center', color='white')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")
    

        elif reader == "Reader3" and tag == "Tag2" and previous_reader == "Reader1" and prev_tag=="Tag2":
            # Assign absolute positions
            positions = [(56, 3.6), (66.5, 3.6), (76.9, 3.6)]
            chain_positions = [((66, 3.95), (66.5, 3.95)), ((76.5, 3.95), (76.8, 3.95))]
            
            # Move all train parts
            for i, (x, y) in enumerate(positions):
                train_parts[i].set_xy((x, y))
            
            # Move all chains
            for i, ((x1, y1), (x2, y2)) in enumerate(chain_positions):
                chains[i].set_data([x1, x2], [y1, y2])

             # Update Tag Labels
            # tag_positions = [(9 + car_width / 2, 4.0), (15 + car_width / 2, 4.0)]
            # tag_labels = ["Tag 2", "Tag 1"]
            # for (x, y), label in zip(tag_positions, tag_labels):
            #     ax.text(x, y, label, fontsize=7, ha='center')
            
            # Highlight detected tag and reader
            rfid_tags[reader].set_color("green")
            train_parts[2 if tag == "Tag1" else -1].set_color("blue")
            train_parts[0 if tag == "Tag2" else -1].set_color("green")
            rfid_status.set_text(f"Detected: {reader} -> {tag}")
            rfid_status.set_color("green")
        else:
            rfid_status.set_text("No RFID Detected")
            rfid_status.set_color("red")
        
        # Update previous_reader AFTER processing the current reader
        previous_reader = reader
        prev_tag=tag

gps_mode = False  # Track whether GPS mode is active

# GPS location link
live_location_link = "https://maps.app.goo.gl/LTaC9nbkytEweHUq8"

def open_live_location_link():
    webbrowser.open_new_tab(live_location_link)

def switch_to_gps():
    global gps_mode
    if not gps_mode:  # Only switch once
        print("Switching to GPS control system...")
        gps_mode = True
        open_live_location_link()
    else:
        gps_mode = False
        print("Already in GPS mode")


# Main loop
try:
    ser.reset_input_buffer()  # Clears old data
    # last_response_time = time.time()
    while True:
        try:
            detection=read_rfid();
            if 'Reader' in detection:
                update(detection)
                plt.pause(0.1)

            elif 'X' in detection:  # If Arduino sends failure message
                print("RFID Reader Failure Detected!")
                switch_to_gps()

            elif 'Sequence' in detection:
                previous_reader=None
                prev_tag=None  
                rfid_status.set_text("Cycle restarted. Waiting for first detection...")
                rfid_status.set_color("blue")

        except KeyboardInterrupt:
            print("Stopping program.")
            break
        # while True:
        # try:
        #     if ser.in_waiting > 0:
        #         data = ser.readline().decode('utf-8').strip()
        #         # print("Received:", data)

        #         if "R" in data:  # If we receive any RFID reader output
        #             # last_response_time = time.time()  # Reset timer
        #             continue

        #         elif "X" in data:  # If Arduino sends failure message
        #             print("RFID Reader Failure Detected!")
        #             switch_to_gps()
        #             # while "X" in data:
        #             # # print("Waiting for RFID to recover...")
        #             #     time.sleep(0.5)  # Give some time before rechecking
        #             #     if ser.in_waiting > 0:
        #             #         data = ser.readline().decode('utf-8').strip()  # Read new data


        #         # # Check timeout (5 seconds)
        #         # if time.time() - last_response_time > 5:
        #         #     print("No RFID response for 5 seconds! Switching to GPS...")
        #         #     switch_to_gps()

        #         # time.sleep(0.5)  # Reduce CPU usage

        # except KeyboardInterrupt:
        #     print("Stopping program.")
        #     break

except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
    plt.close()