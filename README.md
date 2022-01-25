# cloud-image-viewer
viewer for images in aws s3, azure blob

# 참고
.ui -> .py 변환
```
python -m PyQt5.uic.pyuic -x resources/main_view.ui -o views/main_view_ui.py
python -m PyQt5.uic.pyuic -x resources/settings_cloud_account_dialog.ui -o views/settings_cloud_account_dialog_ui.py
python -m PyQt5.uic.pyuic -x resources/file_upload_dialog.ui -o views/file_upload_dialog_ui.py
```