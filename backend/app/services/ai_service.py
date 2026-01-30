"""AI service for chat functionality using OpenAI."""
from typing import Optional, List
from sqlalchemy.orm import Session
from openai import OpenAI

from ..config import get_settings
from ..models.schemas import Role, Language, AnswerMode, ChatResponse
from ..repositories.profile_repository import ProfileRepository
from ..repositories.skill_repository import SkillRepository
from ..repositories.project_repository import ProjectRepository


class AIService:
    """AI service that reads from database for context."""

    def __init__(self, db: Session):
        self.db = db
        self.profile_repo = ProfileRepository(db)
        self.skill_repo = SkillRepository(db)
        self.project_repo = ProjectRepository(db)

        settings = get_settings()
        self.client = None
        if settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def _get_context_from_db(self, lang: Language, role: Role) -> str:
        """Build context string from database."""
        context_parts = []

        # Get profile
        profile_data = self.profile_repo.get_profile_for_display(lang, role)
        if profile_data:
            context_parts.append("=== Profile ===")
            context_parts.append(f"Name: {profile_data['name']} ({profile_data['name_kana']})")
            context_parts.append(f"Age: {profile_data['age']}")
            context_parts.append(f"School: {profile_data['school']} (Graduated {profile_data['graduation_year']})")
            context_parts.append(f"Work Experience: {profile_data['work_experience']}")
            context_parts.append(f"Japan Residence: {profile_data['japan_residence']}")
            context_parts.append(f"Japanese Level: {profile_data['japanese_level']}")
            context_parts.append(f"Field: {profile_data['field']}")
            context_parts.append(f"\nSelf PR:\n{profile_data['self_pr']}")

        # Get skills
        skills = self.skill_repo.get_skills_grouped_by_category(lang, role)
        context_parts.append("\n=== Skills ===")
        for category, skill_list in skills.items():
            context_parts.append(f"\n{category.upper()}:")
            for s in skill_list:
                level_stars = "★" * s["level"] + "☆" * (5 - s["level"])
                context_parts.append(f"  - {s['name']}: {level_stars} ({s['experience']})")

        # Get projects
        projects_data = self.project_repo.get_projects_for_display(lang, role)
        context_parts.append("\n=== Projects ===")
        for p in projects_data["projects"]:
            context_parts.append(f"\n[Project {p['id']}] {p['name']}")
            context_parts.append(f"  Role: {p['role']}")
            context_parts.append(f"  Team Size: {p['team_size']}")
            context_parts.append(f"  Duration: {p['duration']} ({p['start_date']} - {p.get('end_date', 'Present')})")
            context_parts.append(f"  Technologies: {', '.join(p['technologies'])}")
            context_parts.append(f"  Phases: {', '.join(p['phases'])}")
            context_parts.append(f"  Description: {p['description']}")
            context_parts.append(f"  Highlights: {', '.join(p['highlights'])}")

        return "\n".join(context_parts)

    def _get_system_prompt(self, role: Role, lang: Language, mode: AnswerMode) -> str:
        """Build system prompt for AI."""
        role_context = {
            Role.LEADER: {
                "ja": "あなたはチームリーダー・テックリードの視点で回答するアシスタントです。システム設計、チームマネジメント、技術的意思決定、メンタリングの経験を強調してください。",
                "vi": "Bạn là trợ lý trả lời từ góc nhìn Engineering Leader / Tech Lead. Hãy nhấn mạnh kinh nghiệm về thiết kế hệ thống, quản lý nhóm, ra quyết định kỹ thuật, và hướng dẫn.",
                "en": "You are an assistant answering from the perspective of an Engineering Leader / Tech Lead. Emphasize experience in system design, team management, technical decision making, and mentoring."
            },
            Role.BRSE: {
                "ja": "あなたはBrSE（ブリッジSE）の視点で回答するアシスタントです。日本語コミュニケーション、要件定義、顧客対応、日越間の調整経験を強調してください。",
                "vi": "Bạn là trợ lý trả lời từ góc nhìn BrSE (Bridge SE). Hãy nhấn mạnh kinh nghiệm giao tiếp tiếng Nhật, định nghĩa yêu cầu, đối ứng khách hàng, điều phối Nhật-Việt.",
                "en": "You are an assistant answering from the perspective of a BrSE (Bridge SE). Emphasize Japanese communication, requirements definition, customer interaction, and Japan-Vietnam coordination experience."
            },
            Role.FULLSTACK: {
                "ja": "あなたはフルスタックエンジニアの視点で回答するアシスタントです。フロントエンド・バックエンド開発、API設計、データベース、クラウド・DevOpsの経験を強調してください。",
                "vi": "Bạn là trợ lý trả lời từ góc nhìn Fullstack Engineer. Hãy nhấn mạnh kinh nghiệm phát triển Frontend/Backend, thiết kế API, Database, Cloud & DevOps.",
                "en": "You are an assistant answering from the perspective of a Fullstack Engineer. Emphasize Frontend/Backend development, API design, Database, Cloud & DevOps experience."
            }
        }

        not_found_msg = {
            "ja": "その内容はスキルシートに記載されていません。",
            "vi": "Nội dung này không có trong skill sheet.",
            "en": "This content is not available in the skill sheet."
        }

        base_instructions = {
            "ja": """重要なルール:
1. スキルシートに記載されている情報のみを使用して回答してください
2. 記載されていない情報については推測や一般的なアドバイスを行わないでください
3. 回答は簡潔でプロフェッショナルに、採用担当者に適した形式で行ってください
4. どのスキル・経験を参照したか明示してください
5. 情報がない場合は「{not_found}」と回答してください""",
            "vi": """Quy tắc quan trọng:
1. Chỉ sử dụng thông tin có trong skill sheet để trả lời
2. Không suy đoán hoặc đưa ra lời khuyên chung cho thông tin không có
3. Trả lời ngắn gọn, chuyên nghiệp, phù hợp với nhà tuyển dụng
4. Nêu rõ skill/kinh nghiệm nào được tham chiếu
5. Nếu không có thông tin, trả lời "{not_found}" """,
            "en": """Important rules:
1. Only use information from the skill sheet to answer
2. Do not speculate or give general advice for missing information
3. Answer concisely and professionally, suitable for recruiters
4. Clearly reference which skill/experience was used
5. If information is not available, respond with "{not_found}" """
        }

        # Get context from database
        skillsheet_data = self._get_context_from_db(lang, role)

        prompt = f"""{role_context[role][lang.value]}

{base_instructions[lang.value].format(not_found=not_found_msg[lang.value])}

=== Skill Sheet Data ===
{skillsheet_data}
"""

        if mode == AnswerMode.BILINGUAL:
            prompt += """

For BILINGUAL mode: Provide your answer in both Japanese and Vietnamese.
Format:
[Japanese Answer]
---
[Vietnamese Answer]
"""

        return prompt

    def chat(self, question: str, lang: Language, role: Role, mode: AnswerMode) -> ChatResponse:
        """Process a chat question and return response."""
        if not self.client:
            return self._fallback_response(question, lang, role, mode)

        system_prompt = self._get_system_prompt(role, lang, mode)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            answer = response.choices[0].message.content
            answer_secondary = None

            if mode == AnswerMode.BILINGUAL and "---" in answer:
                parts = answer.split("---")
                answer = parts[0].strip()
                answer_secondary = parts[1].strip() if len(parts) > 1 else None

            return ChatResponse(
                answer=answer,
                answer_secondary=answer_secondary,
                sources=self._extract_sources(answer, lang, role)
            )

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_response(question, lang, role, mode)

    def _fallback_response(self, question: str, lang: Language, role: Role, mode: AnswerMode) -> ChatResponse:
        """Fallback response when OpenAI is not available."""
        question_lower = question.lower()

        keywords_map = {
            "leader": [
                "リーダー", "leader", "チーム", "team", "設計", "design", "マネジメント", "management",
                "lãnh đạo", "quản lý", "nhóm", "thiết kế", "dẫn dắt", "team leader"
            ],
            "brse": [
                "brse", "ブリッジ", "bridge", "日本語", "japanese", "要件", "requirements", "顧客", "customer",
                "cầu nối", "tiếng nhật", "yêu cầu", "khách hàng", "giao tiếp", "điều phối"
            ],
            "fullstack": [
                "フロントエンド", "frontend", "バックエンド", "backend", "api", "データベース", "database",
                "fullstack", "full stack", "full-stack"
            ],
            "skill": [
                "スキル", "skill", "技術", "technology", "言語", "language", "経験", "experience",
                "kỹ năng", "công nghệ", "ngôn ngữ", "kinh nghiệm", "trình độ"
            ],
            "project": [
                "プロジェクト", "project", "案件", "開発", "development",
                "dự án", "tham gia", "làm việc", "phát triển",
                "du an", "phat trien"
            ],
            "ai": [
                "ai", "機械学習", "machine learning", "yolo", "pytorch",
                "trí tuệ nhân tạo", "học máy", "nhận diện", "camera",
                "tri tue nhan tao", "hoc may", "nhan dien"
            ],
            "recent_project": [
                "最新", "最近", "直近", "latest", "recent", "last",
                "gần nhất", "gần đây", "mới nhất", "cuối cùng",
                "gan nhat", "gan day", "moi nhat", "cuoi cung"
            ]
        }

        responses = {
            "ja": {
                "leader": "チームリーダーとして、AIを活用した自動レジ精算システムのプロジェクトでは、5名のチームを率いて、基本設計から運用保守まで一貫して担当しました。技術的な意思決定やコードレビュー、メンバーのメンタリングを行いながら、品質と納期を管理しました。",
                "brse": "BrSEとして、人物・人事管理システムのプロジェクトでは、日本の顧客とオフショア開発チームのブリッジとして、要件定義、技術的な伝達、品質管理、日越間のコミュニケーションを担当しました。日本語レベルはN2で、9年間の日本在住経験があります。",
                "fullstack": "フルスタック開発では、フロントエンド（VueJS、ReactJS）とバックエンド（ASP.NET Core、Laravel、Django）の両方を経験しております。高速道路情報管理システムでは、詳細設計から現地試験、運用保守まで、一連の開発プロセスを担当しました。",
                "skill": "主なスキル：C#（2年7ヶ月）、JavaScript（3年5ヶ月）、Python（1年）、VueJS（1年6ヶ月）、ASP.NET Core（1年1ヶ月）、MySQL（2年6ヶ月）、Oracle（2年5ヶ月）",
                "project": "10件のプロジェクト経験があります。特に注目すべきは、AIを活用した自動レジ精算システム（チームリーダー）、人物・人事管理システム（BrSE）、高速道路情報管理システム（フルスタック開発）です。",
                "recent_project": "【最新プロジェクト】AIを活用した自動レジ精算システム（2025年6月〜2026年2月）\n役割：チームリーダー（5名チーム）\n技術：PHP, VueJS, Python, Laravel, PyTorch, YOLO, Qdrant, OpenCV, WebSockets\n内容：USBカメラで商品をリアルタイム認識・分類し、レジ精算を自動化するエッジAIシステムを開発。YOLOベースの商品検出、ベクトル埋め込みによる商品分類、WebRTCによるリアルタイム映像配信を実装しました。",
                "ai": "AIを活用した自動レジ精算システムでは、YOLOベースのリアルタイム商品検出、Qdrant Vector DBによるベクトル埋め込み、ByteTrackによるマルチオブジェクトトラッキング、WebRTCによるリアルタイム映像配信を実装しました。",
                "default": "ご質問ありがとうございます。スキルシートに基づいて、4年のWeb開発経験、9年の日本在住経験、N2の日本語レベルを持つフルスタックエンジニアです。詳細な情報については、プロフィールやスキルセクションをご覧ください。"
            },
            "vi": {
                "leader": "Với vai trò Team Leader, trong dự án Hệ thống thanh toán tự động sử dụng AI, tôi đã dẫn dắt nhóm 5 người, phụ trách từ thiết kế cơ bản đến vận hành bảo trì. Tôi đã thực hiện quyết định kỹ thuật, code review, hướng dẫn thành viên, đồng thời quản lý chất lượng và tiến độ.",
                "brse": "Với vai trò BrSE, trong dự án Hệ thống quản lý nhân sự, tôi là cầu nối giữa khách hàng Nhật và đội offshore, phụ trách định nghĩa yêu cầu, truyền đạt kỹ thuật, quản lý chất lượng, giao tiếp Nhật-Việt. Trình độ tiếng Nhật N2, 9 năm sống tại Nhật.",
                "fullstack": "Về phát triển fullstack, tôi có kinh nghiệm cả Frontend (VueJS, ReactJS) và Backend (ASP.NET Core, Laravel, Django). Trong dự án Hệ thống quản lý thông tin đường cao tốc, tôi đã phụ trách từ thiết kế chi tiết đến thử nghiệm và vận hành bảo trì.",
                "skill": "Kỹ năng chính: C# (2 năm 7 tháng), JavaScript (3 năm 5 tháng), Python (1 năm), VueJS (1 năm 6 tháng), ASP.NET Core (1 năm 1 tháng), MySQL (2 năm 6 tháng), Oracle (2 năm 5 tháng)",
                "project": "Có kinh nghiệm 10 dự án. Đáng chú ý: Hệ thống thanh toán tự động AI (Team Leader), Hệ thống quản lý nhân sự (BrSE), Hệ thống quản lý thông tin đường cao tốc (Fullstack).",
                "recent_project": "【Dự án gần nhất】Hệ thống thanh toán tự động sử dụng AI (06/2025 - 02/2026)\nVai trò: Team Leader (nhóm 5 người)\nCông nghệ: PHP, VueJS, Python, Laravel, PyTorch, YOLO, Qdrant, OpenCV, WebSockets\nMô tả: Phát triển hệ thống Edge AI nhận diện và phân loại sản phẩm real-time từ camera USB, tự động hóa thanh toán. Triển khai: phát hiện sản phẩm bằng YOLO, phân loại bằng vector embedding (Qdrant), streaming video real-time bằng WebRTC.",
                "ai": "Trong dự án Hệ thống thanh toán tự động AI, tôi đã triển khai: phát hiện sản phẩm real-time bằng YOLO, vector embedding với Qdrant Vector DB, multi-object tracking với ByteTrack, streaming video real-time với WebRTC.",
                "default": "Cảm ơn câu hỏi của bạn. Dựa trên skill sheet, tôi là Fullstack Engineer với 4 năm kinh nghiệm phát triển web, 9 năm sống tại Nhật, trình độ tiếng Nhật N2. Vui lòng xem phần Profile và Skills để biết thêm chi tiết."
            },
            "en": {
                "leader": "As Team Leader in the AI-Powered Automatic Checkout System project, I led a team of 5, handling everything from basic design to operation and maintenance. I made technical decisions, conducted code reviews, mentored team members, and managed quality and delivery.",
                "brse": "As BrSE in the Personnel & HR Management System project, I served as a bridge between Japanese clients and the offshore development team, handling requirements definition, technical communication, quality management, and Japan-Vietnam coordination. Japanese level N2, 9 years in Japan.",
                "fullstack": "For fullstack development, I have experience in both Frontend (VueJS, ReactJS) and Backend (ASP.NET Core, Laravel, Django). In the Highway Information Management System, I handled everything from detailed design to on-site testing and operation maintenance.",
                "skill": "Main skills: C# (2y 7m), JavaScript (3y 5m), Python (1y), VueJS (1y 6m), ASP.NET Core (1y 1m), MySQL (2y 6m), Oracle (2y 5m)",
                "project": "10 project experiences. Notable: AI-Powered Automatic Checkout System (Team Leader), Personnel & HR Management System (BrSE), Highway Information Management System (Fullstack).",
                "recent_project": "[Latest Project] AI-Powered Automatic Checkout System (Jun 2025 - Feb 2026)\nRole: Team Leader (5-person team)\nTech: PHP, VueJS, Python, Laravel, PyTorch, YOLO, Qdrant, OpenCV, WebSockets\nDescription: Developed an Edge AI system that recognizes and classifies products in real-time from USB camera to automate checkout. Implemented: YOLO-based product detection, vector embedding classification (Qdrant), real-time video streaming via WebRTC.",
                "ai": "In the AI-Powered Automatic Checkout System, I implemented: YOLO-based real-time product detection, vector embedding with Qdrant Vector DB, multi-object tracking with ByteTrack, real-time video streaming with WebRTC.",
                "default": "Thank you for your question. Based on the skill sheet, I am a Fullstack Engineer with 4 years of web development experience, 9 years in Japan, and N2 Japanese level. Please see the Profile and Skills sections for more details."
            }
        }

        lang_responses = responses.get(lang.value, responses["ja"])
        answer = lang_responses["default"]

        # Priority order for matching (more specific first)
        priority_keys = ["recent_project", "ai", "leader", "brse", "fullstack", "skill", "project"]

        for key in priority_keys:
            if key in keywords_map:
                if any(kw in question_lower for kw in keywords_map[key]):
                    if key in lang_responses:
                        answer = lang_responses[key]
                        break

        answer_secondary = None
        if mode == AnswerMode.BILINGUAL:
            secondary_lang = "vi" if lang.value == "ja" else "ja"
            secondary_responses = responses.get(secondary_lang, responses["ja"])
            for key in priority_keys:
                if key in keywords_map:
                    if any(kw in question_lower for kw in keywords_map[key]):
                        if key in secondary_responses:
                            answer_secondary = secondary_responses[key]
                            break
            if not answer_secondary:
                answer_secondary = secondary_responses["default"]

        return ChatResponse(
            answer=answer,
            answer_secondary=answer_secondary,
            sources=[]
        )

    def _extract_sources(self, answer: str, lang: Language, role: Role) -> List[str]:
        """Extract referenced sources from the answer."""
        sources = []
        projects_data = self.project_repo.get_projects_for_display(lang, role)

        for p in projects_data["projects"]:
            if p["name"].lower() in answer.lower():
                sources.append(f"Project: {p['name']}")

        skills = self.skill_repo.get_skills_grouped_by_category(lang, role)
        for category, skill_list in skills.items():
            for s in skill_list:
                if s["name"].lower() in answer.lower():
                    sources.append(f"Skill: {s['name']}")

        return list(set(sources))[:5]
