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
