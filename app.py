import streamlit as st
import pandas as pd
import os
import subprocess

st.title("Công Cụ Tra Cứu Sinh Viên 🚀")

# Upload file danh sách MSSV
uploaded_file = st.file_uploader("Chọn file danh sách MSSV (Excel)", type=["xlsx"])

# Nhập thông tin đăng nhập
username = st.text_input("Tên đăng nhập")
password = st.text_input("Mật khẩu", type="password")

if st.button("Bắt đầu tra cứu"):
    if uploaded_file is not None and username and password:
        # Lưu file Excel tạm thời
        file_path = "danh_sach_mssv.xlsx"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.info("Đang tra cứu, vui lòng chờ...")

        # Chạy script tra cứu
        try:
            result = subprocess.run(["python", "tra_cuu_sinh_vien.py"], capture_output=True, text=True)
            st.success("Tra cứu hoàn tất! Tải file kết quả bên dưới.")
            
            # Hiển thị file kết quả
            if os.path.exists("ket_qua_tra_cuu.xlsx"):
                with open("ket_qua_tra_cuu.xlsx", "rb") as f:
                    st.download_button("📥 Tải xuống kết quả", f, file_name="ket_qua_tra_cuu.xlsx")
        except Exception as e:
            st.error(f"Lỗi trong quá trình tra cứu: {e}")
    else:
        st.warning("Vui lòng nhập đầy đủ thông tin và chọn file danh sách MSSV.")

