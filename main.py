import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# 1. إعداد قاموس الألوان وقيم HSV الخاصة بها
colors_config = {
    'الأسود': {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 30]), 'video': None, 'color_code': 'black'},
    'الأحمر': {'lower': np.array([0, 100, 100]), 'upper': np.array([10, 255, 255]), 'video': None, 'color_code': 'red'},
    'الأزرق': {'lower': np.array([100, 150, 0]), 'upper': np.array([140, 255, 255]), 'video': None, 'color_code': 'blue'},
    'الأخضر': {'lower': np.array([40, 40, 40]), 'upper': np.array([80, 255, 255]), 'video': None, 'color_code': 'green'},
    'البرتقالي': {'lower': np.array([11, 100, 100]), 'upper': np.array([25, 255, 255]), 'video': None, 'color_code': 'orange'}
}

# دالة لاختيار ملف الفيديو لكل لون
def select_video(color_name):
    file_path = filedialog.askopenfilename(
        title=f"اختر فيديو للون {color_name}",
        filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")]
    )
    if file_path:
        colors_config[color_name]['video'] = file_path
        labels[color_name].config(text=f"تم الاختيار: {os.path.basename(file_path)}", fg="green")

# دالة تشغيل الكاميرا والكشف عن الألوان
def start_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("خطأ", "تعذر فتح الكاميرا")
        return

    messagebox.showinfo("تشغيل", "الكاميرا تعمل الآن! اضغط 'q' لإغلاق الكاميرا.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # الفحص لكل لون تم تحديد فيديو له
        for color_name, data in colors_config.items():
            if data['video'] is not None:  # لو تم اختيار فيديو لهذا اللون
                mask = cv2.inRange(hsv, data['lower'], data['upper'])
                if cv2.countNonZero(mask) > 100000:  # اكتشاف اللون
                    print(f"تم اكتشاف اللون {color_name}! جاري فتح الفيديو...")
                    os.startfile(data['video'])
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        cv2.imshow('Camera Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- بناء الواجهة الرسومية (GUI) ---
root = tk.Tk()
root.title("برنامج كشف الألوان وتشغيل الفيديوهات")
root.geometry("450x550")

tk.Label(root, text="اختر فيديو لكل لون تريد تفعيله:", font=("Arial", 14, "bold")).pack(pady=10)

labels = {}

for color_name in colors_config.keys():
    frame = tk.Frame(root)
    frame.pack(pady=5, fill="x", padx=20)
    
    btn = tk.Button(frame, text=f"اختيار فيديو للون ({color_name})", 
                    font=("Arial", 11), 
                    command=lambda c=color_name: select_video(c))
    btn.pack(side="left")
    
    lbl = tk.Label(frame, text="لم يتم اختيار فيديو", fg="red", font=("Arial", 9))
    lbl.pack(side="right")
    labels[color_name] = lbl

tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=15)

start_btn = tk.Button(root, text="بدء تشغيل الكاميرا 🎥", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=start_camera)
start_btn.pack(pady=15)

root.mainloop()