from datetime import datetime

import customtkinter as ctk
import serial
import serial.tools.list_ports
from serial.serialutil import SerialBase


class App(ctk.CTk):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    ctk.deactivate_automatic_dpi_awareness()

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.min_angle: int = 180
        self.max_angle: int = 0
        self.current_angle: int = 0

        self._label_font_size = 16
        self._main_font_size = 14
        self._small_font_size = 14

        self._update_job_id = None

        self.serial_port: SerialBase | None = None
        self.port_list = serial.tools.list_ports.comports()
        self.baudrate_list = ["75", "110", "300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]

        self.angle_label: ctk.CTkLabel | None = None
        self.angle_slider: ctk.CTkSlider | None = None
        self.start_btn: ctk.CTkButton | None = None
        self.stop_btn: ctk.CTkButton | None = None
        self.select_port_btn: ctk.CTkComboBox | None = None
        self.select_baudrate_btn: ctk.CTkComboBox | None = None
        self.clear_message_btn: ctk.CTkButton | None = None
        self.ping_btn: ctk.CTkButton | None = None
        self.message_box: ctk.CTkTextbox | None = None

        self.title("UI Arduino Servo Control")
        self.geometry("500x520")
        self.resizable(False, False)

        self.create_widgets()

        self.focus_set()
        self.focus()

    def lambda_send_serial_data_setter(self, value):
        return lambda: self.send_serial_angle_data(value)

    def sliding_callback(self, value):
        angle = int(value)
        self.angle_label.configure(text=f"Servo Angle: {angle} °")

        if self._update_job_id is not None:
            self.after_cancel(self._update_job_id)

        self._update_job_id = self.after(1000, self.lambda_send_serial_data_setter(angle))

    def port_callback(self, choice):
        self.select_port_btn.set(choice)
        print("port_callback:", choice)

    def baudrate_callback(self, choice):
        self.select_baudrate_btn.set(choice)
        print("baudrate_callback:", choice)

    def available_ports_callback(self):
        devices = []
        for port in self.port_list:
            device = port.device
            manufacturer = port.manufacturer if port.manufacturer else "empty"
            devices.append(f"{device}, {manufacturer}")
        return devices

    def set_default_arduino_port(self):
        result = "Select Port"
        for port in self.port_list:
            if port.manufacturer is not None and port.manufacturer.lower().__contains__("arduino"):
                device = port.device
                manufacturer = port.manufacturer if port.manufacturer else "empty"
                result = f"{device}, {manufacturer}"
        return result

    def open_port(self):
        port = str(self.select_port_btn.get().split(",")[0])
        baudrate = int(self.select_baudrate_btn.get())
        print(f"port: {port}, baudrate: {baudrate}")

        try:
            self.serial_port = serial.Serial(port, baudrate)
            self.print_message(f"Opened serial port {port} at {baudrate} baud.")
        except serial.SerialException as e:
            self.print_message(f"Failed to open serial port: {e}")

    def print_message(self, text):
        self.message_box.insert(0.0, "\n")
        self.message_box.insert(1.0, str(datetime.now()))
        self.message_box.insert(2.0, ">> " + text + "\n\n")

    def clear_message(self):
        self.message_box.delete(0.0, "end")

    def ping_serial(self):
        if self.serial_port and self.serial_port.is_open:
            tx = "PING"
            self.serial_port.write(tx.encode())
            rx = self.serial_port.readline()
            rxs = str(rx, encoding="utf-8").strip()
            print(rxs)
            self.print_message(f"Sent: {tx}, result: {rxs}")
        else:
            self.print_message("Serial port is not open.")

    def send_serial_angle_data(self, angle: int):
        angle_str = f"ANGL<{angle}>"
        if self.serial_port and self.serial_port.is_open:
            tx = angle_str.encode()
            self.serial_port.write(tx)
            rx = self.serial_port.readline()
            rxs = str(rx, encoding="utf-8").strip()
            print(rxs)
            self.print_message(f"Sent: {angle_str}, result: {rxs}")

    def close_port(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.print_message(f"Port closed.")

    def create_widgets(self):

        ctk.CTkLabel(
            master=self,
            height=30,
            text=f"Range of servo data [{self.min_angle} - {self.max_angle}] degree",
            font=("Helvetica", self._main_font_size, "normal")
        ).pack(pady=(10, 0), fill="x")

        # Angle label
        self.angle_label = ctk.CTkLabel(
            master=self,
            height=30,
            text="Servo Angle: 90 °",
            font=("Helvetica", self._label_font_size, "bold")
        )
        self.angle_label.pack(pady=0, fill="x")

        # Angle Slider
        self.angle_slider = ctk.CTkSlider(
            master=self,
            from_=self.min_angle,
            to=self.max_angle,
            height=20,
            progress_color="transparent",
            command=self.sliding_callback,
            orientation="horizontal")
        self.angle_slider.pack(pady=10, padx=20, fill="x")
        self.angle_slider.set(90)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=(10, 0), padx=20)

        # Select Communication Port
        self.select_port_btn = ctk.CTkComboBox(
            master=btn_frame,
            height=30,
            width=440,
            justify="center",
            values=self.available_ports_callback(),
            font=("Helvetica", 16),
            dropdown_font=("Helvetica", self._main_font_size),
            command=self.port_callback)
        self.select_port_btn.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="wens")
        self.select_port_btn.set(self.set_default_arduino_port())

        # Select Serial Speed btn
        self.select_baudrate_btn = ctk.CTkComboBox(
            master=btn_frame,
            height=30,
            values=self.baudrate_list,
            font=("Helvetica", self._main_font_size),
            justify="center",
            dropdown_font=("Helvetica", self._main_font_size),
            command=self.baudrate_callback)
        self.select_baudrate_btn.grid(row=1, column=0, columnspan=2, pady=(5, 0), padx=10, sticky="wens")
        self.select_baudrate_btn.set("9600")

        # Open Connection btn
        self.start_btn = ctk.CTkButton(
            master=btn_frame,
            height=30,
            text="Start",
            font=("Helvetica", self._main_font_size),
            command=self.open_port)
        self.start_btn.grid(row=2, column=0, pady=(5, 0), padx=(10, 5), sticky="wens")

        # Close Connection btn
        self.stop_btn = ctk.CTkButton(
            master=btn_frame,
            height=30,
            text="Stop",
            font=("Helvetica", self._main_font_size),
            command=self.close_port)
        self.stop_btn.grid(row=2, column=1, pady=(5, 0), padx=(5, 10), sticky="wens")

        ctk.CTkLabel(
            master=btn_frame,
            height=30,
            anchor="w",
            text="Communication Terminal",
            font=("Helvetica", self._main_font_size)
        ).grid(row=3, column=0, columnspan=2, pady=(20, 0), padx=(20, 0), sticky="wens")

        # Terminal message area
        self.message_box = ctk.CTkTextbox(
            master=btn_frame,
            height=150,
            font=("Helvetica", self._small_font_size))
        self.message_box.grid(row=4, column=0, columnspan=2, pady=0, padx=10, sticky="wens")

        # Ping Serial btn
        self.ping_btn = ctk.CTkButton(
            master=btn_frame,
            height=30,
            text="Ping",
            font=("Helvetica", self._main_font_size),
            command=self.ping_serial)
        self.ping_btn.grid(row=5, column=0, pady=(5, 10), padx=(10, 5), sticky="wens")

        # Clear terminal messages btn
        self.clear_message_btn = ctk.CTkButton(
            master=btn_frame,
            height=30,
            text="Clear",
            font=("Helvetica", self._main_font_size),
            command=self.clear_message)
        self.clear_message_btn.grid(row=5, column=1, pady=(5, 10), padx=(5, 10), sticky="wens")

        ctk.CTkLabel(
            master=self,
            height=30,
            text="Copyright © 2024 Designed by Artem Melnikov",
            font=("Helvetica", 12, "normal")
        ).pack(fill="x")


if __name__ == "__main__":
    app = App()
    app.mainloop()
