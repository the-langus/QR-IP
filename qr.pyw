import qrcode
from tkinter import Button, Entry, Tk, Label
from PIL import ImageTk
import socket

def center_window(root, width=300, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def get_port():
    def set_port(p):
        nonlocal port
        port = p
        root.quit()

    root = Tk()
    root.title("Port Input")
    center_window(root)

    Label(root, text="Choose a port number:", padx=10, pady=10).pack()

    port = None

    Button(root, text="8000", command=lambda: set_port("8000"), padx=10, pady=5).pack()
    Button(root, text="8080", command=lambda: set_port("8080"), padx=10, pady=5).pack()
    Button(root, text="3000", command=lambda: set_port("3000"), padx=10, pady=5).pack()

    # Add an entry for custom port input
    custom_port_entry = Entry(root)
    custom_port_entry.pack(padx=10, pady=5)
    Button(root, text="Set Custom Port", command=lambda: set_port(custom_port_entry.get()), padx=10, pady=5).pack()

    def on_closing():
        nonlocal port
        if port is None:
            port = "8000"  # Default port if none is selected
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
    root.destroy()
    return port

def gen_qr():
    port = get_port()

    # Get the local machine IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # Append http:// to the IP address
    url = f"http://{local_ip}"
    
    # Allow the user to input a port number
    url_with_port = f"{url}:{port}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("%URL%" + url_with_port)
    qr.make(fit=True)

    qr_image = qr.make_image(fill='black', back_color='white')

    # Display the QR code in a Tkinter window
    root = Tk()
    root.title(url_with_port)
    center_window(root, width=400, height=400)

    # Load the image
    qr_photo = ImageTk.PhotoImage(qr_image)

    # Create a label to display the image
    label = Label(root, image=qr_photo)
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    gen_qr()