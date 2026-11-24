import tkinter as tk
from tkinter import filedialog
import subprocess
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
                 if result.returncode != 0:
                    print(result.stderr)

               case "dp":
                 print("Running DeepPoly")
                 result = run_eran(model_path, dataset, "deeppoly", "0.0002", timeout=180)
                 print(result.stdout)
                 if result.returncode != 0:
                    print(result.stderr)

            #    case "gp":
            #     print("Running GPUPoly")
            #     result = run_eran(model_path, "cifar10", "refinezono", "0.0002", timeout=180)
            #     print(result.stdout)
            #     if result.returncode != 0:
            #         print(result.stderr)

               case "rz":
                   print("Running RefineZono")
                   result = run_eran(model_path, dataset, "refinezono", "0.0002", timeout=180)
                   print(result.stdout)
                   if result.returncode != 0:
                      print(result.stderr)

               case "rp":
                   print("Running RefinePoly")
                   result = run_eran(model_path, dataset, "refinepoly", "0.0002", timeout=180)
                   print(result.stdout)
                   if result.returncode != 0:
                        print(result.stderr)

            #    case "rgp":
            #        print("Running RefineGPUZono")
            #        result = run_eran(model_path, "cifar10", "deeppoly", "0.0002", timeout=180)
            #        print(result.stdout)
            #        if result.returncode != 0:
            #             print(result.stderr)
               case _:
                 print("Unknown action")
    else:
        fileupload.config(text="Upload a model here before running analysis")


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
root.geometry("700x500")

# 2. Add widgets (Label, Text Entry, Button)
#TODO textbox for verifying model is uploaded

fileupload = tk.Button(root, text="Upload Model as (insert model type extension)", command=upload_file)
fileupload.pack(padx=30, pady=30)

toggledata = tk.Button(root, text="Dataset:cifar10", command=lambda: select_dataset())
toggledata.pack(pady=10)

runall = tk.Button(root, text="Run All Analyses", command=lambda: on_button_click("all"))
runall.pack(pady=10)

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