import streamlit as st
import pandas as pd
import os
import subprocess

st.title("Công Cụ Tra Cứu Sinh Viên 🚀")

# Upload file danh sách MSSV
uploaded_file = st.file_uploader("Chọn file danh sách MSSV (Excel)", type=["xlsx"])

if uploaded_file is not None:
    # Lưu file Excel tạm thời
    file_path = "danh_sach_mssv.xlsx"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File đã được tải lên thành công! Vui lòng đăng nhập vào IAPS9.")
    st.info("1. Truy cập https://iaps9.poly.edu.vn/\n2. Đăng nhập và chọn cơ sở PTCĐ Cần Thơ\n3. Nhấn Enter để tiếp tục")

    if st.button("Bắt đầu tra cứu"):
        st.info("Đang tra cứu, vui lòng chờ...")
        try:
            result = subprocess.run(["python", "tra_cuu_sinh_vien.py"], capture_output=True, text=True)
            st.success("Tra cứu hoàn tất! Tải file kết quả bên dưới.")
            
            if os.path.exists("ket_qua_tra_cuu.xlsx"):
                with open("ket_qua_tra_cuu.xlsx", "rb") as f:
                    st.download_button("📥 Tải xuống kết quả", f, file_name="ket_qua_tra_cuu.xlsx")
        except Exception as e:
            st.error(f"Lỗi trong quá trình tra cứu: {e}")
