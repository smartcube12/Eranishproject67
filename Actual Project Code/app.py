import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import re
import sys
import os
import threading

hasfile = False
model_path = None
dataset = "cifar10"
# def run_in_thread():
#  # Start the command in a separate thread so the UI stays responsive
#     thread = threading.Thread(
#         target=run_command_in_background,
#         args=(command, working_dir, deepz, output_box),
#         daemon=True,
#     )
#     thread.start()



WSL_DISTRO = "Ubuntu"          # name from `wsl -l -v`
WSL_PY = "/home/smart/ERAN/venv/bin/python"             # or "/home/smart/ERAN/venv/bin/python" if that venv exists
ERAN_WSL_DIR = "/home/smart/ERAN/tf_verify"

def run_eran(netname, dataset, domain, epsilon, timeout=600, num_tests=10, **extra):
    wsl_net = subprocess.run(
        ["wsl", "-d", WSL_DISTRO, "wslpath", "-a", netname],
        capture_output=True, text=True).stdout.strip()
    cmd = ["wsl", "-d", WSL_DISTRO, "--cd", ERAN_WSL_DIR,
           "env", "CUDA_VISIBLE_DEVICES=-1", WSL_PY, ".",
           "--netname", wsl_net, "--dataset", dataset,
           "--domain", domain, "--epsilon", str(epsilon), "--num_tests", str(num_tests)]
    for flag, val in extra.items():
        cmd += [f"--{flag}", str(val)]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,)

#r = run_eran("../nets/mynet.onnx", "mnist", "deepzono", 0.02, mean=0.1307, std=0.3081, num_tests=100)

def clean_output(text):
    # remove ERAN's printed config dict ({'...': ..., ... })
    return re.sub(r"^\{'.*?\}[ \t]*\n", "", text, flags=re.S | re.M)


def on_button_click(type):
    global hasfile
    global model_path
    global dataset
    if(hasfile):
       match type:
               case "all":
                 print("Running all")
                 #TODO insert threads to run that

               case "dz":
                 #ERAN_DIR = os.path.expanduser("~/ERAN/tf_verify")
                 print("Running DeepZono")
                 result = run_eran(model_path, dataset, "deepzono", "0.0002", timeout=180)
                 print(result.stdout)
                 open_new_window(clean_output(result.stdout))
                 if result.returncode != 0:
                    print(result.stderr)
                    open_new_window(result.stderr)

               case "dp":
                 print("Running DeepPoly")
                 result = run_eran(model_path, dataset, "deeppoly", "0.0002", timeout=180)
                 print(result.stdout)
                 open_new_window(clean_output(result.stdout))
                 if result.returncode != 0:
                    print(result.stderr)
                    open_new_window(result.stderr)

            #    case "gp":
            #     print("Running GPUPoly")
            #     result = run_eran(model_path, "cifar10", "refinezono", "0.0002", timeout=180)
            #     print(result.stdout)
            #open_new_window(clean_output(result.stdout))
            #     if result.returncode != 0:
            #         print(result.stderr)
            #open_new_window(result.stderr)

               case "rz":
                   print("Running RefineZono")
                   result = run_eran(model_path, dataset, "refinezono", "0.0002", timeout=180)
                   print(result.stdout)
                   open_new_window(clean_output(result.stdout))
                   if result.returncode != 0:
                      print(result.stderr)
                      open_new_window(result.stderr)

               case "rp":
                   print("Running RefinePoly")
                   result = run_eran(model_path, dataset, "refinepoly", "0.0002", timeout=180)
                   print(result.stdout)
                   open_new_window(clean_output(result.stdout))
                   if result.returncode != 0:
                        print(result.stderr)
                        open_new_window(result.stderr)

            #    case "rgp":
            #        print("Running RefineGPUZono")
            #        result = run_eran(model_path, "cifar10", "deeppoly", "0.0002", timeout=180)
            #        print(result.stdout)
            #open_new_window(clean_output(result.stdout))
            #        if result.returncode != 0:
            #             print(result.stderr)
            #open_new_window(result.stderr)
               case _:
                 print("Unknown action")
    else:
        fileupload.config(text="Upload a model here before running analysis")

def open_new_window(results):
    new_win = tk.Toplevel(root)
    new_win.title("Results")
    new_win.geometry("900x650")

    canvas = tk.Canvas(new_win, highlightthickness=0)
    scrollbar = ttk.Scrollbar(new_win, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # put the label INSIDE the scrollable frame
    ttk.Label(scrollable_frame, text=results, justify="left").pack(
        padx=20, pady=20, anchor="w")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # keep the inner frame as wide as the canvas
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfig(window_id, width=e.width))

    def _on_mousewheel(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        elif event.delta:
            canvas.yview_scroll(int(-event.delta / 120) or (-1 if event.delta > 0 else 1),
                                "units")

    def _bind_wheel(_event=None):
        new_win.bind_all("<MouseWheel>", _on_mousewheel)
        new_win.bind_all("<Button-4>", _on_mousewheel)
        new_win.bind_all("<Button-5>", _on_mousewheel)

    def _unbind_wheel(_event=None):
        new_win.unbind_all("<MouseWheel>")
        new_win.unbind_all("<Button-4>")
        new_win.unbind_all("<Button-5>")

    new_win.bind("<Enter>", _bind_wheel)
    new_win.bind("<Leave>", _unbind_wheel)
    new_win.bind("<Destroy>", _unbind_wheel)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)



def select_dataset():
    global dataset
    if (dataset == "cifar10"):
        dataset = "mnist"
        toggledata.config(text="Dataset:mnist")
    else:
        dataset = "cifar10"
        toggledata.config(text="Dataset:cifar10")
    

  

def upload_file():
    global hasfile
    global model_path
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[(" files", "*.*"), ("Text files", "*.txt")]
        #filetypes=[("ONNX", "*.onnx"), ("TensorFlow", "*.tf *.meta"), ("ERAN text", "*.pyt")]
    )
    if file_path:
        hasfile = True
        model_path = file_path
        # with open(file_path, "r", encoding="utf-8") as f:
        #     content = f.read()
        print("Uploaded:", file_path)
        #print(content)
        # update text box
        fileupload.config(text="Uploaded Successfully")
        

# 1. Create the main window
root = tk.Tk()
root.title("ERAN")
root.geometry("350x500")

# 2. Add widgets (Label, Text Entry, Button)
#TODO textbox for verifying model is uploaded

fileupload = tk.Button(root, text="Upload Model as (insert model type extension)", command=upload_file)
fileupload.pack(padx=10, pady=30)

toggledata = tk.Button(root, text="Dataset:cifar10", command=lambda: select_dataset())
toggledata.pack(pady=10)

runall = tk.Button(root, text="Run All Analyses", command=lambda: on_button_click("all"))
runall.pack(pady=20)

deepz = tk.Button(root, text="DeepZono", command=lambda: on_button_click("dz"))
deepz.pack(pady=10)

deeppoly = tk.Button(root, text="DeepPoly", command=lambda: on_button_click("dp"))
deeppoly.pack(pady=10)

gpupoly = tk.Button(root, text="GPUPoly", command=lambda: on_button_click("gp"))
gpupoly.pack(pady=10)

refinezono = tk.Button(root, text="RefineZono", command=lambda: on_button_click("rz"))
refinezono.pack(pady=10)

refinepoly = tk.Button(root, text="RefinePoly", command=lambda: on_button_click("rp"))
refinepoly.pack(pady=10)

refinegpupoly = tk.Button(root, text="RefineGPUPoly", command=lambda: on_button_click("rgp"))
refinegpupoly.pack(pady=10)


# 3. Start the application loop
root.mainloop()