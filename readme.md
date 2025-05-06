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

## 2. Thiết lập pre-commit

Dự án đã cấu hình sẵn pre-commit để kiểm tra code tự động trước khi commit.
Cài đặt và kích hoạt pre-commit như sau:

```bash
uvx pip install pre-commit
uvx pre-commit install
```

Chạy toàn bộ các hook pre-commit thủ công (nên chạy lần đầu):

```bash
uvx pre-commit run --all-files
```

Nếu muốn kiểm tra lại code và chạy pre-commit, dùng lệnh:

```bash
make precommit
```

## 3. Kiểm tra code với Makefile
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
uvx ruff check
uvx ruff check --fix
uvx ruff format
uvx mypy ./
```
