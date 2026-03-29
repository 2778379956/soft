"""
悬浮摄像头 - Floating Camera
Windows 7 悬浮摄像头窗口，置顶显示，可拖动，可调节透明度/大小
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os

# For Windows, use SetWindowPos to keep window on top
try:
    import ctypes
    from ctypes import windll, wintypes
except ImportError:
    pass


class FloatingCamera:
    def __init__(self):
        self.running = True
        
        # Camera index - try 0 first
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("ERROR: Cannot open camera")
            sys.exit(1)
        
        # Default settings
        self.opacity = 0.95
        self.scale = 0.5  # 缩放比例
        self.always_on_top = True
        self.flipped = False  # 水平翻转
        
        # Window settings
        self.window_w = 640
        self.window_h = 480
        
        # Create tkinter window
        self.root = tk.Tk()
        self.root.title("悬浮摄像头")
        self.root.overrideredirect(True)  # 无边框
        self.root.attributes('-topmost', self.always_on_top)
        self.root.attributes('-alpha', self.opacity)
        self.root.configure(bg='gray')
        
        # Make window draggable
        self._drag_data = {"x": 0, "y": 0}
        
        # Canvas for camera feed
        self.canvas = tk.Canvas(
            self.root,
            width=self.window_w,
            height=self.window_h,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Control panel (bottom bar)
        self.control_frame = tk.Frame(self.root, bg='#2d2d2d', height=40)
        self.control_frame.pack(side='bottom', fill='x')
        self.control_frame.pack_propagate(False)
        
        # Control buttons
        btn_style = {
            'bg': '#4a4a4a',
            'fg': 'white',
            'activebackground': '#6a6a6a',
            'relief': 'flat',
            'cursor': 'hand2',
            'font': ('Arial', 9)
        }
        
        tk.Button(
            self.control_frame,
            text='置顶',
            command=self.toggle_top,
            width=5,
            **btn_style
        ).pack(side='left', padx=2, pady=4)
        
        tk.Button(
            self.control_frame,
            text='翻转',
            command=self.toggle_flip,
            width=5,
            **btn_style
        ).pack(side='left', padx=2, pady=4)
        
        tk.Button(
            self.control_frame,
            text='关闭',
            command=self.close,
            width=5,
            **btn_style
        ).pack(side='right', padx=2, pady=4)
        
        # Opacity slider
        tk.Label(
            self.control_frame,
            text='透明度',
            bg='#2d2d2d',
            fg='white',
            font=('Arial', 8)
        ).pack(side='left', padx=(5, 2))
        
        self.opacity_slider = ttk.Scale(
            self.control_frame,
            from_=0.3,
            to=1.0,
            value=self.opacity,
            command=self.on_opacity_change,
            length=80
        )
        self.opacity_slider.pack(side='left', padx=2)
        
        # Scale slider
        tk.Label(
            self.control_frame,
            text='大小',
            bg='#2d2d2d',
            fg='white',
            font=('Arial', 8)
        ).pack(side='left', padx=(5, 2))
        
        self.scale_slider = ttk.Scale(
            self.control_frame,
            from_=0.2,
            to=1.0,
            value=self.scale,
            command=self.on_scale_change,
            length=80
        )
        self.scale_slider.pack(side='left', padx=2)
        
        # Bind drag events
        self.canvas.bind('<Button-1>', self.on_drag_start)
        self.canvas.bind('<B1-Motion>', self.on_drag_motion)
        self.control_frame.bind('<Button-1>', self.on_drag_start)
        self.control_frame.bind('<B1-Motion>', self.on_drag_motion)
        
        # Photo image for canvas
        self.photo = None
        
        # Camera thread
        self.thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.thread.start()
        
        # Update loop
        self.update_frame()
        
        # Center window
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - self.window_w - 20
        y = screen_h - self.window_h - 60
        self.root.geometry(f'{self.window_w}x{self.window_h}+{x}+{y}')
        
        self.root.mainloop()
    
    def camera_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = frame
            else:
                time.sleep(0.01)
    
    def update_frame(self):
        if not self.running:
            return
            
        if hasattr(self, 'latest_frame'):
            frame = self.latest_frame.copy()
            
            # Flip horizontally
            if self.flipped:
                frame = cv2.flip(frame, 1)
            
            # Resize
            new_w = int(frame.shape[1] * self.scale)
            new_h = int(frame.shape[0] * self.scale)
            if new_w > 0 and new_h > 0:
                frame = cv2.resize(frame, (new_w, new_h))
            
            # Convert to RGB for tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Update window size if scale changed
            if new_w != self.window_w or new_h != self.window_h - 40:
                self.window_w = max(200, new_w)
                self.window_h = max(100, new_h + 40)
                self.canvas.configure(width=self.window_w, height=new_h)
                self.root.geometry(f'{self.window_w}x{self.window_h}')
            
            # Convert to PhotoImage
            from PIL import Image, ImageTk
            img = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(img)
            
            # Update canvas
            self.canvas.delete('all')
            self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        
        self.root.after(30, self.update_frame)
    
    def on_drag_start(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y
    
    def on_drag_motion(self, event):
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        x = self.root.winfo_x() + delta_x
        y = self.root.winfo_y() + delta_y
        self.root.geometry(f'+{x}+{y}')
    
    def toggle_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes('-topmost', self.always_on_top)
    
    def toggle_flip(self):
        self.flipped = not self.flipped
    
    def on_opacity_change(self, value):
        self.opacity = float(value)
        self.root.attributes('-alpha', self.opacity)
    
    def on_scale_change(self, value):
        self.scale = float(value)
    
    def close(self):
        self.running = False
        self.cap.release()
        self.root.destroy()
        sys.exit(0)


if __name__ == '__main__':
    FloatingCamera()
