#!/usr/bin/env python3
"""
HEIC Converter GUI
A lightweight Python GUI for converting HEIC images to JPEG/PNG format
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import zipfile
from pathlib import Path
import time
from datetime import datetime
import sys

try:
    from pillow_heif import register_heif_opener
    from PIL import Image, ImageTk
    register_heif_opener()
    PILLOW_HEIF_AVAILABLE = True
except ImportError:
    PILLOW_HEIF_AVAILABLE = False

class HEICConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_format = tk.StringVar(value="JPEG")
        self.quality = tk.IntVar(value=92)
        self.create_zip = tk.BooleanVar(value=True)
        self.conversion_running = False
        
        # Check dependencies
        self.check_dependencies()
        
        # Create GUI
        self.create_widgets()
        
        # Set default output path
        self.output_path.set(os.path.expanduser("~/Desktop/converted_images"))
        
    def check_dependencies(self):
        """Check if required dependencies are available"""
        if not PILLOW_HEIF_AVAILABLE:
            messagebox.showerror(
                "Missing Dependencies",
                "Required library 'pillow-heif' is not installed.\n\n"
                "Install it with: pip install pillow-heif\n\n"
                "The application will now exit."
            )
            sys.exit(1)
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input section
        ttk.Label(main_frame, text="Input Path:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse Files", command=self.browse_files).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(input_frame, text="Browse Folder", command=self.browse_folder).grid(row=0, column=2)
        
        # Output section
        ttk.Label(main_frame, text="Output Path:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=1)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Conversion Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Format selection
        ttk.Label(settings_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        format_frame = ttk.Frame(settings_frame)
        format_frame.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.output_format, value="JPEG").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(format_frame, text="PNG", variable=self.output_format, value="PNG").pack(side=tk.LEFT)
        
        # Quality setting
        ttk.Label(settings_frame, text="JPEG Quality:").grid(row=1, column=0, sticky=tk.W, pady=(5, 5))
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 5))
        
        quality_scale = ttk.Scale(quality_frame, from_=1, to=100, variable=self.quality, orient=tk.HORIZONTAL)
        quality_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        quality_label = ttk.Label(quality_frame, text="92%")
        quality_label.pack(side=tk.LEFT)
        
        # Update quality label when scale changes
        def update_quality_label(val):
            quality_label.config(text=f"{int(float(val))}%")
        quality_scale.config(command=update_quality_label)
        
        # Zip option
        ttk.Checkbutton(settings_frame, text="Create ZIP file", variable=self.create_zip).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(20, 10))
        
        self.scan_button = ttk.Button(button_frame, text="Scan for HEIC Files", command=self.scan_files)
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.convert_button = ttk.Button(button_frame, text="Convert Images", command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_conversion, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main_frame row weights
        main_frame.rowconfigure(6, weight=1)
        
    def browse_files(self):
        """Browse for individual HEIC files"""
        files = filedialog.askopenfilenames(
            title="Select HEIC Files",
            filetypes=[("HEIC files", "*.heic *.HEIC *.heif *.HEIF"), ("All files", "*.*")]
        )
        if files:
            self.input_path.set(";".join(files))
    
    def browse_folder(self):
        """Browse for folder containing HEIC files"""
        folder = filedialog.askdirectory(title="Select Folder with HEIC Files")
        if folder:
            self.input_path.set(folder)
    
    def browse_output(self):
        """Browse for output directory"""
        folder = filedialog.askdirectory(title="Select Output Directory")
        if folder:
            self.output_path.set(folder)
    
    def log_message(self, message):
        """Add message to log area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def scan_files(self):
        """Scan for HEIC files in the input path"""
        input_path = self.input_path.get().strip()
        if not input_path:
            messagebox.showerror("Error", "Please select an input path")
            return
        
        heic_files = self.find_heic_files(input_path)
        
        if heic_files:
            self.log_message(f"Found {len(heic_files)} HEIC files:")
            for file in heic_files:
                self.log_message(f"  - {os.path.basename(file)}")
        else:
            self.log_message("No HEIC files found in the specified path")
    
    def find_heic_files(self, input_path):
        """Find all HEIC files in the input path"""
        heic_files = []
        
        if ";" in input_path:
            # Multiple files selected
            files = input_path.split(";")
            for file in files:
                if file.lower().endswith(('.heic', '.heif')):
                    heic_files.append(file)
        elif os.path.isfile(input_path):
            # Single file
            if input_path.lower().endswith(('.heic', '.heif')):
                heic_files.append(input_path)
        elif os.path.isdir(input_path):
            # Directory
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(('.heic', '.heif')):
                        heic_files.append(os.path.join(root, file))
        
        return heic_files
    
    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        if self.conversion_running:
            return
        
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input path")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please select an output path")
            return
        
        # Find HEIC files
        heic_files = self.find_heic_files(input_path)
        
        if not heic_files:
            messagebox.showerror("Error", "No HEIC files found in the specified path")
            return
        
        # Start conversion in separate thread
        self.conversion_running = True
        self.convert_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.conversion_thread = threading.Thread(
            target=self.convert_images,
            args=(heic_files, output_path)
        )
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
    
    def stop_conversion(self):
        """Stop the conversion process"""
        self.conversion_running = False
        self.log_message("Conversion stopped by user")
    
    def convert_images(self, heic_files, output_path):
        """Convert HEIC images to the specified format"""
        try:
            # Create output directory
            os.makedirs(output_path, exist_ok=True)
            
            converted_files = []
            total_files = len(heic_files)
            
            self.progress.config(maximum=total_files)
            self.log_message(f"Starting conversion of {total_files} files...")
            
            for i, heic_file in enumerate(heic_files):
                if not self.conversion_running:
                    break
                
                try:
                    # Update status
                    self.status_label.config(text=f"Converting {os.path.basename(heic_file)}...")
                    
                    # Load and convert image
                    with Image.open(heic_file) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'LA', 'P'):
                            if self.output_format.get() == 'JPEG':
                                # Create white background for JPEG
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'P':
                                    img = img.convert('RGBA')
                                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                                img = background
                            else:
                                img = img.convert('RGBA')
                        elif img.mode != 'RGB' and self.output_format.get() == 'JPEG':
                            img = img.convert('RGB')
                        
                        # Generate output filename
                        base_name = os.path.splitext(os.path.basename(heic_file))[0]
                        ext = '.jpg' if self.output_format.get() == 'JPEG' else '.png'
                        output_file = os.path.join(output_path, f"{base_name}{ext}")
                        
                        # Save image
                        save_kwargs = {}
                        if self.output_format.get() == 'JPEG':
                            save_kwargs['quality'] = self.quality.get()
                            save_kwargs['optimize'] = True
                        
                        img.save(output_file, format=self.output_format.get(), **save_kwargs)
                        converted_files.append(output_file)
                        
                        self.log_message(f"Converted: {os.path.basename(heic_file)} -> {os.path.basename(output_file)}")
                
                except Exception as e:
                    self.log_message(f"Error converting {os.path.basename(heic_file)}: {str(e)}")
                
                # Update progress
                self.progress.config(value=i + 1)
                self.root.update_idletasks()
            
            # Create ZIP file if requested
            if self.create_zip.get() and converted_files and self.conversion_running:
                self.status_label.config(text="Creating ZIP file...")
                zip_filename = f"converted_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                zip_path = os.path.join(output_path, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in converted_files:
                        zipf.write(file, os.path.basename(file))
                
                self.log_message(f"ZIP file created: {zip_filename}")
            
            # Final status
            if self.conversion_running:
                self.status_label.config(text=f"Conversion complete! {len(converted_files)} files converted.")
                self.log_message(f"Conversion completed successfully! {len(converted_files)} files converted.")
                messagebox.showinfo("Success", f"Conversion completed!\n{len(converted_files)} files converted to {output_path}")
            else:
                self.status_label.config(text="Conversion stopped")
        
        except Exception as e:
            self.log_message(f"Error during conversion: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")
        
        finally:
            # Reset UI
            self.conversion_running = False
            self.convert_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress.config(value=0)
            if hasattr(self, 'conversion_thread'):
                self.conversion_thread = None

def main():
    root = tk.Tk()
    app = HEICConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()