# 🎨 Re-Colorizer: AI Grayscale to Color Image Converter

An end-to-end Computer Vision & Deep Learning web application that transforms black & white photos into realistic, vibrant colored images using deep convolutional neural networks in the **CIE LAB** color space.

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live_Web_App-black?logo=vercel)](https://re-colorizer.vercel.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![Deep Learning](https://img.shields.io/badge/Deep_Learning-CNN-orange)](https://github.com/Amarjit0300/Re-colourizer)

🔗 **Live Public Demo**: [https://re-colorizer.vercel.app](https://re-colorizer.vercel.app)

---

## 🌟 Key Features

- **Interactive Before & After Split Slider**: Slide seamlessly between authentic historical grayscale and predicted full-color chrominance.
- **CIE LAB Color Space Pipeline**:
  - Keeps luminance ($L$) uncompressed and pristine from original input photography.
  - Predicts $(a, b)$ color channels using pre-trained convolutional neural networks with 313 quantized color cluster centroids (`pts_in_hull.npy`).
- **In-Browser Interactive Studio**: Test sample vintage photography or upload custom images with instant client-side tone mapping and download capabilities.
- **RESTful Flask Backend**: Endpoints for full-resolution server-side deep learning inference using OpenCV DNN.

---

## 🛠️ Tech Stack

- **Computer Vision & ML**: Python, OpenCV (`cv2.dnn`), NumPy
- **Deep Learning Model**: Zhang et al. Colorful Image Colorization Caffe Architecture
- **Web Frontend**: Modern HTML5, Tailwind CSS, Interactive Canvas & Slider
- **Backend**: Flask, Python

---

## 🚀 Getting Started Locally

```bash
git clone https://github.com/Amarjit0300/Re-colourizer.git
cd Re-colourizer
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` to run the Flask application.

---

## 📄 License
MIT License &copy; Amarjit Singh
