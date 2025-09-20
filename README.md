# thiennguyenvu.github.io
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue?logo=github)](https://thiennguyenvu.github.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Create quickly beauty template CV. 

**Live demo:** [thiennguyenvu.github.io](https://thiennguyenvu.github.io/)

## 🚀 User guidle
- Download source code.
- Open `index.html` and edit any content.

### 1. Change primary color:
- Change `hsl` color in `static/css/main.css` at line `2` to any color you want. Or change with `Inspect` of browser then click button `Print CV`.
```
:root {
  --primary-h: 164; /* Change Hue value at here */
  --primary-s: 49%; /* Change Saturation value at here */
  --primary-l: 49%; /* Change Lightness value at here */
}
```

### 2. If you want to change a background of CV:
- Change `header background picture`: 
class `.block-background-image` in `static/css/main.css` at line `32`

- Change `footer background picture`: class `.footer-img` in `static/css/main.css` at line `249`

### 3. Easy get PDF file:

- Click button `Print CV` on top website and wait a dialog open.

- At `Printer`, select `Save as PDF`.
![alt text](image2.png)

- At `Options`, select `Background graphics`.
![alt text](image.png)

- Click `Save` and enjoy your CV.

## 📄 License
This project is licensed under the [MIT License](LICENSE).