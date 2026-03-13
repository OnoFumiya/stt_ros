import os
import sys
os.environ["HF_HOME"] = os.path.expanduser("~/.sobits_speech_recognition/whisper_models")
import threading
import requests
import whisper
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from faster_whisper.utils import _MODELS as FASTER_MODELS

class WhisperModelManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Model Manager")
        self.root.geometry("900x750")
        self.base_dir = os.path.expanduser("~/.sobits_speech_recognition/whisper_models")
        os.makedirs(self.base_dir, exist_ok=True)
        self.create_widgets()
        self.refresh_list()
        self.log(f"Initialized. Models will be saved to: {self.base_dir}")

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(main_frame, text="Whisper ASR Models", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        tk.Label(main_frame, text=f"Storage: {self.base_dir}", fg="gray").pack(anchor=tk.W, pady=(0, 5))
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.tab_orig = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_orig, text="Open AI Whisper (.pt)")
        self.tree = self.create_treeview(self.tab_orig)
        
        self.tab_faster = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_faster, text="Faster Whisper (CTranslate2)")
        self.tree_faster = self.create_treeview(self.tab_faster)

        btn_frame = tk.Frame(main_frame, pady=10)
        btn_frame.pack(fill=tk.X)

        self.btn_download = tk.Button(btn_frame, text="Download Selected", command=self.start_download, 
                                      state=tk.DISABLED, bg="#e3f2fd", width=20)
        self.btn_download.pack(side=tk.LEFT, padx=5)

        self.btn_delete = tk.Button(btn_frame, text="Delete Selected", command=self.delete_model, 
                                    state=tk.DISABLED, bg="#ffebee", width=20)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.RIGHT, padx=5)

        self.log_area = scrolledtext.ScrolledText(main_frame, height=8, state='disabled', bg="#f8f9fa")
        self.log_area.pack(fill=tk.X, pady=10)

        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="Ready", fg="blue")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

    def create_treeview(self, parent):
        columns = ("name", "size", "status")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        tree.heading("name", text="Model Name")
        tree.heading("size", text="Estimated Size")
        tree.heading("status", text="Status")
        tree.column("name", width=300)
        tree.column("size", width=150, anchor="center")
        tree.column("status", width=150, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        tree.bind("<<TreeviewSelect>>", self.on_select)
        return tree

    def get_current_tab_info(self):
        idx = self.notebook.index(self.notebook.select())
        if idx == 0:
            return self.tree, False
        else:
            return self.tree_faster, True

    def log(self, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, f"[{now}] {msg}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def refresh_list(self):
        self.base_dir = os.path.expanduser("~/.sobits_speech_recognition/whisper_models")

        self.tree.delete(*self.tree.get_children())
        for name in whisper.available_models():
            file_path = os.path.join(self.base_dir, f"{name}.pt")
            is_installed = os.path.exists(file_path) and os.path.getsize(file_path) > 1024*1024
            size_str = f"{os.path.getsize(file_path)/(1024*1024):.1f} MB" if is_installed else "Fetching..."
            item_id = self.tree.insert("", tk.END, values=(name, size_str, "Installed" if is_installed else "Missing"))
            if not is_installed:
                threading.Thread(target=self.update_size_info, args=(item_id, name, False), daemon=True).start()

        self.tree_faster.delete(*self.tree_faster.get_children())
        for name in list(FASTER_MODELS):
            if "distil" in name:
                folder_suffix = name.replace("distil-", "distil-whisper-")
                dir_name = f"models--Systran--faster-{folder_suffix}"
            else:
                dir_name = f"models--Systran--faster-whisper-{name}"
            
            possible_paths = [
                os.path.join(self.base_dir, "hub", dir_name), 
                os.path.join(self.base_dir, dir_name)         
            ]
            
            total_size = 0
            is_installed = False
            
            search_pattern = name.replace("distil-", "distil-whisper-") if "distil" in name else name
            
            for root, dirs, _ in os.walk(self.base_dir):
                for d in dirs:
                    if search_pattern in d and "models--" in d:
                        target_dir = os.path.join(root, d)
                        for r, _, files in os.walk(target_dir):
                            for f in files:
                                fp = os.path.join(r, f)
                                if not os.path.islink(fp):
                                    total_size += os.path.getsize(fp)
            
            if total_size > 1024 * 1024:
                is_installed = True
            status_str = "Installed" if is_installed else "Missing"
            if is_installed:
                size_str = f"{total_size/(1024*1024):.1f} MB"
            else:
                size_str = "Fetching..." 

            item_id = self.tree_faster.insert("", tk.END, values=(name, size_str, status_str))
            
            if not is_installed:
                threading.Thread(target=self.update_size_info, args=(item_id, name, True), daemon=True).start()

        self.log("Refreshed: Strict size and naming check applied.")

    def update_size_info(self, item_id, model_name, is_faster):
        try:
            target_tree = self.tree_faster if is_faster else self.tree
            
            if is_faster:
                if "distil" in model_name:
                    repo_suffix = model_name.replace("distil-", "distil-whisper-")
                    url = f"https://huggingface.co/Systran/faster-{repo_suffix}/resolve/main/model.bin"
                else:
                    url = f"https://huggingface.co/Systran/faster-whisper-{model_name}/resolve/main/model.bin"
            else:
                url = whisper._MODELS.get(model_name)
            
            size_text = "N/A"
            if url:
                try:
                    resp = requests.head(url, allow_redirects=True, timeout=10)
                    if resp.status_code == 200:
                        size_mb = int(resp.headers.get('Content-Length', 0)) / (1024*1024)
                        size_text = f"{size_mb:.1f} MB"
                    else:
                        size_text = "Unknown"
                except:
                    size_text = "Error"

            def safe_set():
                try:
                    if self.root.winfo_exists() and target_tree.exists(item_id):
                        target_tree.set(item_id, column="size", value=size_text)
                except tk.TclError:
                    pass
            self.root.after(0, safe_set)

        except Exception as e:
            print(f"Update size error for {model_name}: {e}")
    def on_select(self, event):
        tree, _ = self.get_current_tab_info()
        sel = tree.selection()
        if not sel: return
        
        item = tree.item(sel[0])
        _, _, status = item['values']

        if status == "Installed":
            self.btn_download.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.NORMAL)
        else:
            self.btn_download.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.DISABLED)

    def start_download(self):
        tree, is_faster = self.get_current_tab_info()
        sel = tree.selection()
        if not sel: return
        model_name = tree.item(sel[0])['values'][0]
        
        self.btn_download.config(state=tk.DISABLED)
        self.status_label.config(text=f"Downloading {model_name}...")
        threading.Thread(target=self.download_worker, args=(model_name, is_faster), daemon=True).start()

    def download_worker(self, model_name, is_faster):
        try:
            if is_faster:
                from faster_whisper import download_model
                self.log(f"Starting Faster-Whisper download: {model_name}")
                self.root.after(0, lambda: self.progress.configure(mode='indeterminate'))
                self.progress.start()
                
                repo_id = model_name
                if "distil" in model_name:
                    repo_id = f"Systran/faster-distil-whisper-{model_name.replace('distil-', '')}"
                elif "/" not in model_name:
                    repo_id = f"Systran/faster-whisper-{model_name}"

                download_model(repo_id) 
                
                self.progress.stop()
                self.root.after(0, lambda: self.progress.configure(mode='determinate', value=100))
            else:
                url = whisper._MODELS.get(model_name)
                target_path = os.path.join(self.base_dir, f"{model_name}.pt")
                resp = requests.get(url, stream=True, timeout=15)
                total_size = int(resp.headers.get('content-length', 0))
                
                with open(target_path, 'wb') as f:
                    downloaded = 0
                    for chunk in resp.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = (downloaded / total_size) * 100
                            self.root.after(0, lambda p=percent: self.progress.configure(value=p))

            self.log(f"Successfully finished: {model_name}")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.root.after(0, self.finish_download)

    def finish_download(self):
        self.progress.configure(value=0)
        self.status_label.config(text="Ready", fg="blue")
        self.refresh_list()

    def delete_model(self):
        tree, is_faster = self.get_current_tab_info()
        sel = tree.selection()
        if not sel: return
        model_name = tree.item(sel[0])['values'][0]
        
        if not messagebox.askyesno("Confirm Delete", f"Delete {model_name}?"):
            return

        try:
            deleted_any = False
            if is_faster:
                search_pattern = model_name.replace("distil-", "distil-whisper-") if "distil" in model_name else model_name
                
                for root, dirs, _ in os.walk(self.base_dir):
                    for d in dirs:
                        if search_pattern in d and "models--" in d:
                            target_path = os.path.join(root, d)
                            shutil.rmtree(target_path)
                            self.log(f"Deleted folder: {target_path}")
                            deleted_any = True
            else:
                target_path = os.path.join(self.base_dir, f"{model_name}.pt")
                if os.path.exists(target_path):
                    os.remove(target_path)
                    self.log(f"Deleted file: {target_path}")
                    deleted_any = True

            if deleted_any:
                self.refresh_list()
            else:
                messagebox.showinfo("Info", "No files found to delete.")

        except Exception as e:
            messagebox.showerror("Delete Error", str(e))

def main():
    try:
        root = tk.Tk()
        app = WhisperModelManager(root)
        root.mainloop()
    except KeyboardInterrupt: pass    

if __name__ == "__main__":
    main()