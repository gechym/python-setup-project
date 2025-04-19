from agents import Agent, function_tool
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


def create_event_agent(model_name: str) -> Agent[any]:
    @function_tool
    def get_list_event() -> str:
        """Lấy danh sách các sự kiện game hiện tại và sắp tới.
        Returns:
            str: Danh sách các sự kiện game với thông tin chi tiết
        """
        events = [
            {
                "name": "Nữ Hoàng Chiến Trường",
                "date": "18/10/2025 - 25/10/2025",
                "description": "Sự kiện đặc biệt dành riêng cho game thủ nữ với nhiều phần quà và trang phục độc quyền",
                "rewards": "Trang phục giới hạn 'Nữ Thần Chiến Binh', 2000 kim cương, thẻ trải nghiệm nhân vật mới",
                "missions": "Thu thập hoa hồng ảo trong các trận đấu, hoàn thành thử thách đồng đội hàng ngày",
                "registration": "Tự động khi đăng nhập trong thời gian sự kiện",
                "occasion": "Ngày Phụ nữ Việt Nam (20/10)",
            },
            {
                "name": "Hành Trình Thống Nhất",
                "date": "28/04/2025 - 05/05/2025",
                "description": "Sự kiện kỷ niệm ngày lễ lớn với chế độ chơi đặc biệt 'Chiến tuyến'",
                "rewards": "Huy hiệu kỷ niệm in-game, súng skin huyền thoại 'Thống Nhất', 30% tăng XP trong thời gian sự kiện",
                "missions": "Tham gia 15 trận đấu chế độ 'Chiến tuyến', giải cứu đồng đội, chiếm đóng các điểm chiến lược",
                "registration": "Tự động khi đăng nhập trong thời gian sự kiện",
                "occasion": "Giải phóng Miền Nam (30/4)",
            },
            {
                "name": "Siêu Năng Suất",
                "date": "29/04/2025 - 05/05/2025",
                "description": "Sự kiện tăng gấp đôi phần thưởng cho mọi hoạt động trong game",
                "rewards": "Code khuyến mãi 'MAYDAY2025' nhận 100 token đặc biệt, gấp đôi kinh nghiệm, thẻ quay số may mắn",
                "missions": "Thử thách 24 giờ - Hoàn thành càng nhiều nhiệm vụ trong 24h để nhận phần thưởng độc quyền",
                "registration": "Tự động khi đăng nhập trong thời gian sự kiện, nhập code 'MAYDAY2025' để nhận thêm quà",
                "occasion": "Quốc tế Lao động (1/5)",
            },
        ]

        result = "DANH SÁCH SỰ KIỆN GAME\n\n"

        for event in events:
            result += f"### {event['name']} - {event['occasion']} ###\n"
            result += f"- Thời gian: {event['date']}\n"
            result += f"- Mô tả: {event['description']}\n"
            result += f"- Phần thưởng: {event['rewards']}\n"
            result += f"- Nhiệm vụ: {event['missions']}\n"
            result += f"- Đăng ký: {event['registration']}\n\n"

        return result

    event_agent = Agent(
        name="event_agent",
        instructions="## Persona ##"
        f"{RECOMMENDED_PROMPT_PREFIX}"
        "Bạn là trợ lý ảo hỗ trợ về sự kiện game, Tên của bạn là Hoài Linh"
        "Bạn chuyên trả lời các câu hỏi liên quan đến sự kiện game hàng tháng, sự kiện đặc biệt"
        "và các thông tin về code khuyến mãi\n"
        "## Nhiệm vụ ##"
        "- Trả lời đầy đủ về sự kiện hiện có và sự kiện sắp diễn ra"
        "- Cung cấp thông tin chính xác về ngày đăng ký tham gia sự kiện"
        "- Giải thích chi tiết về các gói code hàng tháng và cách sử dụng"
        "- Hướng dẫn cách tham gia các sự kiện đặc biệt"
        "- Thông báo về phần thưởng, quà tặng trong các sự kiện\n"
        "## Sử dụng công cụ ##"
        "- Bạn có quyền truy cập vào công cụ 'get_list_event()' để lấy danh sách cập nhật về các sự kiện game"
        "- Khi người dùng hỏi về sự kiện hiện tại hoặc sắp tới, hãy sử dụng công cụ này để cung cấp thông tin chính xác"
        "- Phân tích kết quả từ công cụ và trình bày một cách rõ ràng, dễ hiểu cho người dùng\n"
        "Khi không có thông tin đầy đủ, hãy hỏi thêm để có thể cung cấp thông tin chính xác"
        "Nếu câu hỏi không liên quan đến sự kiện game, hãy nhẹ nhàng giải thích rằng "
        "bạn chỉ có thể trả lời về thông tin sự kiện\n"
        "Nếu người dùng không hỏi những câu hỏi về nghiệp vụ của bạn thì hãy chuyển về cho agent manager"
        "##lưu ý"
        "Nếu người dùng không hỏi những câu hỏi về nghiệp vụ của bạn thì"
        " hãy handoff đến manager ngay lập tứ không cần sự đồng ý hay hỏi ý kiến của người dùng"
        "## Importance Points ##\n"
        "- Xưng với bản thân là *'mình'* và gọi khách hàng là *'bạn'*. Không bao giờ dùng *'tôi'*.\n"
        "- **must not** chia sẻ email hay số điện thoại của khách hàng.\n"
        "- Luôn luôn trả lời bằng **tiếng Việt**.\n"
        "- Bạn **must not** cung cấp bất kỳ thông tin liên quan đến: handoff, agent, tool.\n"
        "- Giữ giọng điệu thân thiện, nhiệt tình và chuyên nghiệp.\n"
        "",
        model=model_name,
        tools=[get_list_event],
    )
    return event_agent
