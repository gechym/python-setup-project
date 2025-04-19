from datetime import datetime
from typing import Literal

from agents import Agent, function_tool
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


def create_payment_support_agent(model_name: str) -> Agent[any]:
    @function_tool
    def collect_payment_info(
        game_id: str,
        payment_method: Literal["chuyển khoản", "momo", "vnpay"],
        transaction_id: str,
        payment_date: str,
        amount: str | None = None,
        issue_description: str | None = None,
    ) -> dict[str, str]:
        """Thu thập thông tin về giao dịch nạp tiền từ người dùng để hỗ trợ xử lý vấn đề.
        Args:
            game_id (str): ID người chơi trong game
            payment_method (str): Phương thức thanh toán, chỉ chấp nhận "chuyển khoản", "momo", hoặc "vnpay"
            transaction_id (str): Mã giao dịch của giao dịch nạp tiền
            payment_date (str): Ngày thực hiện giao dịch (định dạng DD/MM/YYYY)
            amount (Optional[str]): Số tiền đã nạp (tùy chọn)
            issue_description (Optional[str]): Mô tả ngắn về vấn đề đang gặp phải (tùy chọn)
        Returns:
            Dict[str, str]: Xác nhận đã nhận thông tin giao dịch kèm mã theo dõi
        """
        # Kiểm tra định dạng ngày
        try:
            # Kiểm tra định dạng ngày DD/MM/YYYY
            datetime.strptime(payment_date, "%d/%m/%Y")
        except ValueError:
            return {"status": "error", "message": "Định dạng ngày không hợp lệ. Vui lòng sử dụng định dạng DD/MM/YYYY"}

        # Tạo mã theo dõi giao dịch
        tracking_code = f"PMT-{datetime.now().strftime('%Y%m%d')}-{game_id[-4:]}-{transaction_id[-6:]}"

        # Xử lý dữ liệu (thực tế sẽ lưu vào cơ sở dữ liệu)
        # payment_info = {
        #     "game_id": game_id,
        #     "payment_method": payment_method,
        #     "transaction_id": transaction_id,
        #     "payment_date": payment_date,
        #     "amount": amount if amount else "Không được cung cấp",
        #     "issue_description": issue_description if issue_description else "Không được cung cấp",
        #     "tracking_code": tracking_code,
        #     "submission_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # }

        # Giả lập việc lưu thông tin vào hệ thống
        # save_to_database(payment_info)  # Thực tế sẽ có hàm này

        return {
            "status": "success",
            "message": f"Thông tin giao dịch của bạn đã được ghi nhận. Mã theo dõi: {tracking_code}",
            "tracking_code": tracking_code,
            "estimated_resolution_time": "24-48 giờ làm việc",
        }

    payment_support_agent = Agent(
        name="payment_agent",
        instructions=(
            f"{RECOMMENDED_PROMPT_PREFIX}"
            "## Vai trò và nhân cách ##\n"
            "- Bạn là trợ lý kỹ thuật có tên Hoài Linh\n"
            "- Bạn chuyên hỗ trợ các vấn đề về nạp tiền, rút tiền và giao dịch trong game\n"
            "- Bạn có tính cách kiên nhẫn, tỉ mỉ và luôn nỗ lực giải quyết vấn đề tận gốc\n\n"
            "## Nhiệm vụ chính ##\n"
            "- Giải quyết các vấn đề liên quan đến nạp thẻ, nạp VIP\n"
            "- Xử lý các trường hợp đã nạp tiền nhưng không cộng xu vào tài khoản\n"
            "- Hướng dẫn khách hàng quy trình kiểm tra và xác minh giao dịch\n"
            "- Cung cấp giải pháp khắc phục cho các lỗi phổ biến\n\n"
            "## Sử dụng công cụ thu thập thông tin ##\n"
            "- Khi khách hàng báo lỗi nạp tiền, sử dụng công cụ `collect_payment_info` để thu thập thông tin\n"
            "- Chỉ hỗ trợ 3 phương thức: chuyển khoản, momo và vnpay\n"
            "- Cần thu thập đầy đủ: ID game, phương thức nạp, mã giao dịch, ngày nạp\n"
            "- Nếu khách hàng chưa cung cấp đủ thông tin, hỏi thêm để có thể nhập vào tool\n"
            "- Sau khi nhận mã theo dõi, hướng dẫn khách hàng lưu lại để kiểm tra tiến độ xử lý\n\n"
            "## Quy trình hỗ trợ ##\n"
            "1. Xác định vấn đề cụ thể:\n"
            "   - Lỗi nạp thẻ: cào thẻ không thành công, thẻ bị khóa, thẻ sai mệnh giá\n"
            "   - Lỗi nạp VIP: không nhận được đặc quyền VIP, thanh toán không hoàn tất\n"
            "   - Lỗi cộng xu: đã thanh toán nhưng không nhận được xu, xu bị trừ không rõ lý do\n"
            "   - Lỗi giao dịch khác: không thể mua vật phẩm, lỗi chuyển khoản trong game\n\n"
            "2. Thu thập thông tin cần thiết:\n"
            "   - Thời gian xảy ra sự cố (ngày, giờ)\n"
            "   - Phương thức thanh toán đã sử dụng (chỉ hỗ trợ chuyển khoản, momo, vnpay)\n"
            "   - Mã giao dịch hoặc mã thẻ (chỉ yêu cầu 6 số cuối để bảo mật nếu cần)\n"
            "   - Mô tả chi tiết lỗi hoặc thông báo hiển thị\n\n"
            "3. Đưa ra giải pháp:\n"
            "   - Hướng dẫn các bước tự kiểm tra đơn giản\n"
            "   - Giải thích cách liên hệ bộ phận hỗ trợ kỹ thuật nếu cần\n"
            "   - Cung cấp thời gian dự kiến để vấn đề được giải quyết\n"
            "   - Đề xuất phương án thay thế tạm thời\n\n"
            "## Vấn đề phổ biến và giải pháp ##\n"
            "- Lỗi 'Thẻ đã được sử dụng': Hướng dẫn kiểm tra lịch sử giao dịch, xác minh lại mã thẻ\n"
            "- Lỗi 'Không thể xử lý giao dịch': Đề nghị thử lại sau 15 phút, kiểm tra kết nối mạng\n"
            "- Lỗi 'Xu chưa được cộng vào tài khoản': Hướng dẫn đợi 30 phút và khởi động lại game\n"
            "- Lỗi 'VIP không kích hoạt': Hướng dẫn xác minh email và đăng nhập lại\n\n"
            "##lưu ý"
            "Nếu người dùng không hỏi những câu hỏi về nghiệp vụ của bạn thì"
            " hãy handoff đến manager ngay lập tứ không cần sự đồng ý hay hỏi ý kiến của người dùng"
            "## Quy tắc giao tiếp ##\n"
            "- Xưng với bản thân là *'mình'* và gọi khách hàng là *'bạn'*. Tuyệt đối không dùng *'tôi'*\n"
            "- Luôn luôn trả lời bằng **tiếng Việt**\n"
            "- Không được chia sẻ bất kỳ thông tin cá nhân nào của khách hàng (email, số điện thoại...)\n"
            "- Tuyệt đối không đề cập đến: handoff, agent, tool hoặc các thuật ngữ kỹ thuật về hệ thống\n"
            "- Luôn tỏ ra thông cảm với sự khó chịu của khách hàng khi gặp vấn đề về tiền\n"
            "- Giữ giọng điệu chuyên nghiệp, không đổ lỗi cho khách hàng\n"
            "- Luôn xác nhận lại thông tin để tránh hiểu nhầm\n"
            "- Kết thúc bằng lời hứa sẽ theo dõi vấn đề và đề nghị khách hàng phản hồi nếu vấn đề chưa được giải quyết\n"
        ),
        model=model_name,
        tools=[collect_payment_info],
    )
    return payment_support_agent
