# Hướng dẫn thiết lập dự án

## 1. Thiết lập môi trường ảo với `uv`

Cài đặt [uv](https://github.com/astral-sh/uv) nếu bạn chưa có:
```bash
# On Windows.
curl -LsSf https://astral.sh/uv/install.sh | sh


# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```

Tải dependencies và tạo môi trường ảo với `uv`:
```bash
uv sync & uv pip freeze > requirements.txt
```

## 2. Kiểm tra code với Makefile
Dự án đã có sẵn Makefile để chạy các công cụ kiểm tra chất lượng mã nguồn:
- **pylint**: Kiểm tra style và lỗi tiềm ẩn.
- **ruff**: Kiểm tra và tự động sửa style code.
- **mypy**: Kiểm tra type hint.

Chạy tất cả các công cụ kiểm tra:
```bash
make lint
```

Chạy từng công cụ riêng lẻ:
```bash
uvx pylint ./ --ignore=.venv
uvx ruff check --fix
uvx mypy ./
```

## 3. Khắc phục lỗi khi push lên GitHub

Nếu gặp lỗi:
```
error: src refspec master does not match any
error: failed to push some refs to 'https://github.com/gechym/python-setup-project.git'
```
**Nguyên nhân:**  
- Bạn chưa tạo commit nào trong repository.
- Nhánh mặc định của bạn là `main` chứ không phải `master`.

**Cách khắc phục:**
1. Kiểm tra tên nhánh hiện tại:
   ```bash
   git branch
   ```
2. Nếu nhánh là `main`, hãy push với:
   ```bash
   git push origin main
   ```
3. Nếu chưa có commit nào, hãy tạo commit đầu tiên:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main  # hoặc master tùy tên nhánh
   ```
