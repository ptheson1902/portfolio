"""
Database seed script - migrates data from data_service.py to SQLite database.
Run with: python -m app.database.seed
"""
from sqlalchemy.orm import Session
from .connection import engine, SessionLocal
from ..models.db_models import Base, Profile, SkillCategory, Skill, Project, RoleEmphasis


def get_initial_data():
    """Return the initial data to seed (same structure as data_service.py)."""
    profile_data = {
        "name": "PHAM THE SON",
        "name_kana": "ファム テ ソン",
        "name_vi": "PHẠM THẾ SƠN",
        "gender": "male",
        "date_of_birth": "1997-02-19",
        "school": "ECCコンピュータ専門学校",
        "graduation_year": 2022,
        "field": "チームリーダー、WEB開発（フルスタック）、システム開発",
        "work_experience": {"ja": "5年", "vi": "5 năm", "en": "5 years"},
        "japan_residence": {"ja": "9年", "vi": "9 năm", "en": "9 years"},
        "japanese_level": "N2",
        "email": "ptheson1902@gmail.com",
        "phone": "080-8536-1866",
        "address": {
            "ja": "大阪府大阪市生野区新今里７－４－６",
            "vi": "Thành phố Osaka, Osaka",
            "en": "Osaka City, Osaka"
        },
        "social_links": {
            "facebook": "https://www.facebook.com/the.son.75",
            "messenger": "https://m.me/the.son.75",
            "github": "https://github.com/ptheson1902"
        },
        "self_pr": {
            "ja": """日本向け案件を中心に、BrSE・チームリーダー・フルスタックエンジニアとしての経験を有しています。
AIを活用した自動精算システムでは、5名チームのリーダーとして設計から運用まで担当。
9年間の日本在住経験と日本語N2により、日越間の円滑なコミュニケーションと品質向上に貢献してきました。""",
            "vi": """【Điểm mạnh】Team Leader × BrSE × Fullstack × AI Development
Kỹ sư IT có kinh nghiệm làm BrSE, team leader và full-stack cho các dự án thị trường Nhật.
Từng dẫn dắt nhóm 5 người phát triển hệ thống thanh toán tự động sử dụng AI, tham gia từ thiết kế đến vận hành.
Có 9 năm sống tại Nhật, giao tiếp tốt với khách hàng Nhật và team offshore Việt Nam.""",
            "en": """【Strengths】Team Leader × BrSE × Fullstack × AI Development
IT engineer with experience as BrSE, team leader, and full-stack developer for Japanese market projects.
Led a 5-member team to develop an AI-based automated checkout system, handling design through operation.
With 9 years of experience living in Japan and JLPT N2, I bridge Japanese clients and offshore teams effectively."""
        }
    }

    skills_data = {
        "programming_languages": [
            {"name": "C#", "level": 4, "experience": {"ja": "2年7ヶ月", "vi": "2 năm 7 tháng", "en": "2y 7m"}},
            {"name": "JavaScript", "level": 4, "experience": {"ja": "3年5ヶ月", "vi": "3 năm 5 tháng", "en": "3y 5m"}},
            {"name": "PHP", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "Python", "level": 3, "experience": {"ja": "1年", "vi": "1 năm", "en": "1y"}},
            {"name": "Java", "level": 3, "experience": {"ja": "8ヶ月", "vi": "8 tháng", "en": "8m"}},
            {"name": "VB.NET", "level": 3, "experience": {"ja": "8ヶ月", "vi": "8 tháng", "en": "8m"}},
        ],
        "frameworks": [
            {"name": "ASP.NET Core", "level": 4, "experience": {"ja": "1年1ヶ月", "vi": "1 năm 1 tháng", "en": "1y 1m"}},
            {"name": "VueJS", "level": 3, "experience": {"ja": "1年6ヶ月", "vi": "1 năm 6 tháng", "en": "1y 6m"}},
            {"name": "Laravel", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "ASP.NET MVC", "level": 3, "experience": {"ja": "7ヶ月", "vi": "7 tháng", "en": "7m"}},
            {"name": "NodeJS", "level": 2, "experience": {"ja": "6ヶ月", "vi": "6 tháng", "en": "6m"}},
            {"name": "ReactJS", "level": 2, "experience": {"ja": "6ヶ月", "vi": "6 tháng", "en": "6m"}},
            {"name": "Django", "level": 2, "experience": {"ja": "2ヶ月", "vi": "2 tháng", "en": "2m"}},
        ],
        "databases": [
            {"name": "MySQL", "level": 4, "experience": {"ja": "2年6ヶ月", "vi": "2 năm 6 tháng", "en": "2y 6m"}},
            {"name": "Oracle", "level": 4, "experience": {"ja": "2年5ヶ月", "vi": "2 năm 5 tháng", "en": "2y 5m"}},
            {"name": "SQL Server", "level": 3, "experience": {"ja": "10ヶ月", "vi": "10 tháng", "en": "10m"}},
            {"name": "PostgreSQL", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "MongoDB", "level": 1, "experience": {"ja": "6ヶ月", "vi": "6 tháng", "en": "6m"}},
        ],
        "cloud": [
            {"name": "Azure", "level": 2, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
        ],
        "ai_ml": [
            {"name": "PyTorch", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "YOLO", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "OpenCV", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "Qdrant", "level": 3, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
            {"name": "ONNX", "level": 2, "experience": {"ja": "9ヶ月", "vi": "9 tháng", "en": "9m"}},
        ]
    }

    projects_data = [
        {
            "id": 1,
            "name": {"ja": "研修", "vi": "Đào tạo", "en": "Training"},
            "role": "Developer",
            "team_size": "1",
            "technologies": ["Java", "HTML5/CSS3", "JavaScript/jQuery"],
            "environment": "Eclipse",
            "phases": ["製造", "単体テスト"],
            "start_date": "2021-06",
            "end_date": "2021-08",
            "description": {
                "ja": "・【Java】プログラム基礎の理解、課題アプリの作成\n・【Oracle】SQLの理解",
                "vi": "・【Java】Hiểu cơ bản về lập trình, tạo ứng dụng bài tập\n・【Oracle】Hiểu SQL",
                "en": "・[Java] Understanding programming basics, creating practice applications\n・[Oracle] Understanding SQL"
            },
            "highlights": {
                "ja": ["Javaプログラミングの基礎習得", "SQLの基本操作"],
                "vi": ["Nắm vững cơ bản Java", "Thao tác SQL cơ bản"],
                "en": ["Mastered Java programming basics", "Basic SQL operations"]
            },
            "relevance": {"leader": 1, "brse": 1, "fullstack": 2}
        },
        {
            "id": 2,
            "name": {
                "ja": "営業日報システム開発(WEB)",
                "vi": "Phát triển hệ thống báo cáo kinh doanh hàng ngày (WEB)",
                "en": "Sales Daily Report System Development (WEB)"
            },
            "role": "Developer",
            "team_size": "1",
            "technologies": ["Java", "HTML5/Bootstrap", "JavaScript/jQuery", "Servlet"],
            "environment": "Servlet",
            "phases": ["製造", "単体テスト"],
            "start_date": "2021-09",
            "end_date": "2022-01",
            "description": {
                "ja": "・入力画面の新規開発を担当しました。\n・新規登録、修正、削除、照会の画面を作成しました。\n・入力に必須なマスタメンテナンス画面についても対応しました。",
                "vi": "・Phụ trách phát triển mới màn hình nhập liệu. \n・Đã tạo các màn hình đăng ký mới, sửa đổi, xóa, và tra cứu. \n・Cũng đã xử lý màn hình bảo trì master cần thiết cho việc nhập liệu.",
                "en": "・Responsible for new development of input screens. \n・Created screens for new registration, modification, deletion, and inquiry. \n・Also handled master maintenance screens required for input."
            },
            "highlights": {
                "ja": ["CRUD機能の実装", "マスタメンテナンス画面の開発"],
                "vi": ["Triển khai chức năng CRUD", "Phát triển màn hình bảo trì master"],
                "en": ["CRUD functionality implementation", "Master maintenance screen development"]
            },
            "relevance": {"leader": 2, "brse": 2, "fullstack": 4}
        },
        {
            "id": 3,
            "name": {
                "ja": "勤怠（打刻）システム開発(WEB)",
                "vi": "Phát triển hệ thống chấm công (WEB)",
                "en": "Attendance System Development (WEB)"
            },
            "role": "Developer",
            "team_size": "2",
            "technologies": ["C#", "HTML5/Bootstrap", "JavaScript/jQuery", "ASP.NET"],
            "environment": "ASP.NET",
            "phases": ["製造", "単体テスト"],
            "start_date": "2022-01",
            "end_date": "2022-07",
            "description": {
                "ja": "・画面の新規開発を担当しました。\n・新規登録、編集、照会の画面の作成。\n・バッチの作成も担当しました。",
                "vi": "・Phụ trách phát triển mới màn hình. \n・Tạo màn hình đăng ký mới, chỉnh sửa, tra cứu.\n・Tạo batch cũng được phụ trách.",
                "en": "・Responsible for new screen development. \n・Creating new registration, edit, inquiry screens.\n・Also responsible for batch creation."
            },
            "highlights": {
                "ja": ["新規画面開発", "バッチ処理の実装"],
                "vi": ["Phát triển màn hình mới", "Triển khai xử lý batch"],
                "en": ["New screen development", "Batch processing implementation"]
            },
            "relevance": {"leader": 2, "brse": 2, "fullstack": 4}
        },
        {
            "id": 4,
            "name": {
                "ja": "案件・要員の管理システム(WEB)",
                "vi": "Hệ thống quản lý dự án và nhân sự (WEB)",
                "en": "Project & Resource Management System (WEB)"
            },
            "role": "Developer",
            "team_size": "2",
            "technologies": ["Python", "HTML5/Bootstrap", "JavaScript/jQuery", "ExcelVBA", "Django"],
            "environment": "Django",
            "phases": ["製造", "単体テスト", "詳細設計"],
            "start_date": "2022-06",
            "end_date": "2022-08",
            "description": {
                "ja": "・ゲスト利用画面の新規開発を担当しました。\n・新規登録、編集、照会、検索の画面の作成。\n・開発環境の構築も担当しました。",
                "vi": "・Phụ trách phát triển mới màn hình sử dụng cho khách. \n・Tạo màn hình đăng ký mới, chỉnh sửa, tra cứu, tìm kiếm.\n・Tạo môi trường phát triển",
                "en": "・Responsible for new development of guest usage screens. \n・Creating new registration, edit, inquiry, search screens.\n・Development environment setup"
            },
            "highlights": {
                "ja": ["詳細設計への参加", "開発環境構築"],
                "vi": ["Tham gia thiết kế chi tiết", "Xây dựng môi trường phát triển"],
                "en": ["Participated in detailed design", "Development environment setup"]
            },
            "relevance": {"leader": 3, "brse": 2, "fullstack": 4}
        },
        {
            "id": 5,
            "name": {
                "ja": "賃貸システム開発(Windows)",
                "vi": "Phát triển hệ thống cho thuê (Windows)",
                "en": "Rental System Development (Windows)"
            },
            "role": "Developer",
            "team_size": "10",
            "technologies": ["VB.NET", "List Creator", "INTARFRM"],
            "environment": "Windows (Fujitsu)",
            "phases": ["製造", "単体テスト", "詳細設計"],
            "start_date": "2022-08",
            "end_date": "2023-03",
            "description": {
                "ja": "不動産のシステム開発、案件対応",
                "vi": "Phát triển hệ thống bất động sản, xử lý các yêu cầu dự án",
                "en": "Real estate system development, handling project requirements"
            },
            "highlights": {
                "ja": ["大規模チームでの開発経験", "不動産ドメイン知識の習得"],
                "vi": ["Kinh nghiệm phát triển trong nhóm lớn", "Học hỏi kiến thức lĩnh vực bất động sản"],
                "en": ["Development experience in large team", "Acquired real estate domain knowledge"]
            },
            "relevance": {"leader": 3, "brse": 3, "fullstack": 3}
        },
        {
            "id": 6,
            "name": {
                "ja": "住宅管理システムのリプレース",
                "vi": "Thay thế hệ thống quản lý nhà ở",
                "en": "Housing Management System Replacement"
            },
            "role": "Developer",
            "team_size": "5",
            "technologies": ["VueJS"],
            "environment": "Visual Studio Code",
            "phases": ["デザイン", "製造"],
            "start_date": "2023-04",
            "end_date": "2023-05",
            "description": {
                "ja": "モックアップ作成を担当しました。",
                "vi": "Phụ trách tạo mockup.",
                "en": "Responsible for creating mockups."
            },
            "highlights": {
                "ja": ["UI/UXデザイン", "フロントエンド設計"],
                "vi": ["Thiết kế UI/UX", "Thiết kế frontend"],
                "en": ["UI/UX design", "Frontend design"]
            },
            "relevance": {"leader": 2, "brse": 2, "fullstack": 4}
        },
        {
            "id": 7,
            "name": {
                "ja": "実習生＆特定技能管理システム",
                "vi": "Hệ thống quản lý thực tập sinh và kỹ năng đặc định",
                "en": "Trainee & Specified Skilled Worker Management System"
            },
            "role": "Sub-BrSE",
            "team_size": "7",
            "technologies": ["C#", "JavaScript", "ASP.NET MVC", "VueJS"],
            "environment": "ASP.NET MVC, VueJS",
            "phases": ["結合テスト", "Q&A対応", "詳細設計"],
            "start_date": "2023-06",
            "end_date": "2023-11",
            "description": {
                "ja": "・帳票作成、更新、出力（Excel, PDF）。\n・データ登録：CSVインポート、マスター登録、一括登録、複製登録、母国語対応",
                "vi": "・Tạo, cập nhật, xuất báo cáo (Excel, PDF). \n・Đăng ký dữ liệu: Import CSV, đăng ký master, đăng ký hàng loạt, đăng ký sao chép, hỗ trợ ngôn ngữ mẹ đẻ",
                "en": "・Report creation, update, output (Excel, PDF). \n・Data registration: CSV import, master registration, bulk registration, copy registration, native language support"
            },
            "highlights": {
                "ja": ["Sub-BrSEとしての初めての経験", "帳票機能の実装", "多言語対応"],
                "vi": ["Kinh nghiệm đầu tiên với vai trò Sub-BrSE", "Triển khai chức năng báo cáo", "Hỗ trợ đa ngôn ngữ"],
                "en": ["First experience as Sub-BrSE", "Report functionality implementation", "Multi-language support"]
            },
            "relevance": {"leader": 3, "brse": 5, "fullstack": 4}
        },
        {
            "id": 8,
            "name": {
                "ja": "高速道路情報管理システム",
                "vi": "Hệ thống quản lý thông tin đường cao tốc",
                "en": "Highway Information Management System"
            },
            "role": "Developer",
            "team_size": "6",
            "technologies": ["C#", "JavaScript", "ASP.NET Core", "Oracle", "SQL Server"],
            "environment": "ASP.NET Core, Oracle, SQL Server",
            "phases": ["詳細設計", "コーディング", "製造", "単体テスト", "結合テスト", "総合試験", "現地試験", "運用・保守"],
            "start_date": "2023-12",
            "end_date": "2024-12",
            "description": {
                "ja": "・交通管制データの連携及び活用：データ管理、帳票やCSVやPDFなど出力。\n・データ統計：データ管理、帳票やCSVやPDFなど出力。道路状況：地図上のストリームカメラの管理。\n・無線局管理：XMLファイル作成、申請履歴の管理、納付情報の管理、ユーザ情報の管理。\n・バッチ改善を担当しました。",
                "vi": "・Liên kết và sử dụng dữ liệu điều khiển giao thông: Quản lý dữ liệu, xuất báo cáo/CSV/PDF. \n・Thống kê dữ liệu. \n・Tình trạng đường: Quản lý camera stream trên bản đồ. \n・Quản lý trạm vô tuyến: Tạo file XML, quản lý lịch sử đăng ký, quản lý thông tin thanh toán, quản lý thông tin người dùng. \n・Cải thiện batch.",
                "en": "・Traffic control data integration and utilization: Data management, report/CSV/PDF output. \n・Data statistics. \n・Road conditions: Stream camera management on maps. \n・Radio station management: XML file creation, application history management, payment info management, user info management. \n・Batch improvement."
            },
            "highlights": {
                "ja": ["フルスタック開発", "現地試験対応", "運用保守経験", "大規模システム"],
                "vi": ["Phát triển fullstack", "Đối ứng thử nghiệm tại chỗ", "Kinh nghiệm vận hành bảo trì", "Hệ thống quy mô lớn"],
                "en": ["Fullstack development", "On-site testing", "Operation & maintenance experience", "Large-scale system"]
            },
            "relevance": {"leader": 4, "brse": 3, "fullstack": 5}
        },
        {
            "id": 9,
            "name": {
                "ja": "人物・人事管理システム",
                "vi": "Hệ thống quản lý nhân sự",
                "en": "Personnel & HR Management System"
            },
            "role": "BrSE",
            "team_size": "6",
            "technologies": ["C#", "JavaScript", ".NET MVC", "Oracle"],
            "environment": ".NET MVC, Oracle",
            "phases": ["コーディング", "単体テスト", "製造", "Q&A対応"],
            "start_date": "2025-01",
            "end_date": "2025-06",
            "description": {
                "ja": "日本の顧客とオフショア開発チームのブリッジとして\n・要件定義、技術的な伝達、品質管理、日越間のコミュニケーションを担当。\n・人物調査管理画面を担当。人事評価管理画面を担当。\n・調査評価基準設定管理を担当。",
                "vi": "Là cầu nối giữa khách hàng Nhật Bản và đội phát triển offshore\n・Phụ trách định nghĩa yêu cầu, truyền đạt kỹ thuật, quản lý chất lượng, giao tiếp Nhật-Việt.\n・Phụ trách màn hình quản lý điều tra nhân vật.\n・Phụ trách màn hình quản lý đánh giá nhân sự. Phụ trách quản lý cài đặt tiêu chí đánh giá điều tra.",
                "en": "As a bridge between Japanese clients and offshore development team\n・Responsible for requirements definition, technical communication, quality management, Japan-Vietnam communication. \n・Responsible for personnel investigation management screen. \n・HR evaluation management screen. \n・Investigation evaluation criteria setting management."
            },
            "highlights": {
                "ja": ["BrSEとしての本格的な経験", "要件定義", "日越間コミュニケーション", "品質管理"],
                "vi": ["Kinh nghiệm chính thức với vai trò BrSE", "Định nghĩa yêu cầu", "Giao tiếp Nhật-Việt", "Quản lý chất lượng"],
                "en": ["Full BrSE experience", "Requirements definition", "Japan-Vietnam communication", "Quality management"]
            },
            "relevance": {"leader": 4, "brse": 5, "fullstack": 3}
        },
        {
            "id": 10,
            "name": {
                "ja": "AIを活用した自動レジ精算システム",
                "vi": "Hệ thống thanh toán tự động sử dụng AI",
                "en": "AI-Powered Automatic Checkout System"
            },
            "role": "Team Leader",
            "team_size": "5",
            "technologies": ["PHP", "VueJS", "Python", "Laravel", "PyTorch", "ONNX", "YOLO", "Qdrant", "OpenCV", "WebSockets", "MySQL"],
            "environment": "Laravel, PyTorch, ONNX, YOLO, Qdrant, OpenCV, WebSockets, MySQL",
            "phases": ["基本設計", "詳細設計", "コーディング", "単体テスト", "結合テスト", "運用・保守"],
            "start_date": "2025-06",
            "end_date": "2026-02",
            "description": {
                "ja": "USBカメラで撮影した商品画像をリアルタイムで認識・分類し、レジ精算を自動化するエッジAIシステム。\n主な機能：\n・YOLOベースのリアルタイム商品検出。\n・ベクトル埋め込みによる商品分類（Qdrant Vector DB）。\n・ByteTrackによるマルチオブジェクトトラッキング。\n・WebRTCによるリアルタイム映像配信。\n・クラウド同期機能（商品データベース同期）。\n・商品登録機能（新商品の画像登録・学習）",
                "vi": "Hệ thống Edge AI nhận dạng và phân loại hình ảnh sản phẩm quay bằng camera USB theo thời gian thực, tự động hóa thanh toán. \nChức năng chính: \n・Phát hiện sản phẩm thời gian thực dựa trên YOLO.\n・Phân loại sản phẩm bằng vector embedding (Qdrant Vector DB).\n・Theo dõi đa đối tượng bằng ByteTrack.\n・Phát video thời gian thực bằng WebRTC.\n・Đồng bộ cloud.\n・Đăng ký sản phẩm mới.",
                "en": "Edge AI system that recognizes and classifies product images captured by USB camera in real-time, automating checkout.\nMain features: \n・YOLO-based real-time product detection.\n・Product classification by vector embedding (Qdrant Vector DB).\n・Multi-object tracking with ByteTrack.\n・Real-time video streaming via WebRTC.\n・Cloud sync functionality.\n・New product registration and training"
            },
            "highlights": {
                "ja": ["チームリーダーとしての経験", "AI/ML技術の実践", "システム設計", "フルスタック開発"],
                "vi": ["Kinh nghiệm làm Team Leader", "Thực hành công nghệ AI/ML", "Thiết kế hệ thống", "Phát triển fullstack"],
                "en": ["Team Leader experience", "AI/ML technology practice", "System design", "Fullstack development"]
            },
            "relevance": {"leader": 5, "brse": 3, "fullstack": 5}
        }
    ]

    role_emphasis = {
        "leader": {
            "ja": ["システム設計・アーキテクチャ", "チームマネジメント", "技術的意思決定", "コードレビュー・メンタリング", "品質・納期管理"],
            "vi": ["Thiết kế hệ thống & kiến trúc", "Quản lý nhóm", "Ra quyết định kỹ thuật", "Code review & hướng dẫn", "Quản lý chất lượng & tiến độ"],
            "en": ["System design & architecture", "Team management", "Technical decision making", "Code review & mentoring", "Quality & delivery management"]
        },
        "brse": {
            "ja": ["日本語コミュニケーション", "要件定義・仕様策定", "顧客対応", "ドキュメント作成", "日越間の調整"],
            "vi": ["Giao tiếp tiếng Nhật", "Định nghĩa yêu cầu & đặc tả", "Đối ứng khách hàng", "Tạo tài liệu", "Điều phối Nhật-Việt"],
            "en": ["Japanese communication", "Requirements definition", "Customer interaction", "Documentation", "Japan-Vietnam coordination"]
        },
        "fullstack": {
            "ja": ["フロントエンド開発", "バックエンド開発", "API設計", "データベース設計", "クラウド・DevOps"],
            "vi": ["Phát triển Frontend", "Phát triển Backend", "Thiết kế API", "Thiết kế Database", "Cloud & DevOps"],
            "en": ["Frontend development", "Backend development", "API design", "Database design", "Cloud & DevOps"]
        }
    }

    return profile_data, skills_data, projects_data, role_emphasis


def seed_database():
    """Seed the database with initial data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    profile_data, skills_data, projects_data, role_emphasis_data = get_initial_data()

    try:
        # 1. Seed Profile (only if not exists)
        if not db.query(Profile).first():
            profile = Profile(
                id=1,
                name=profile_data["name"],
                name_kana=profile_data["name_kana"],
                name_vi=profile_data["name_vi"],
                gender=profile_data["gender"],
                date_of_birth=profile_data["date_of_birth"],
                school=profile_data["school"],
                graduation_year=profile_data["graduation_year"],
                field=profile_data["field"],
                work_experience=profile_data["work_experience"],
                japan_residence=profile_data["japan_residence"],
                japanese_level=profile_data["japanese_level"],
                email=profile_data["email"],
                phone=profile_data["phone"],
                address=profile_data["address"],
                social_links=profile_data["social_links"],
                self_pr=profile_data["self_pr"]
            )
            db.add(profile)
            print("✓ Profile seeded")

        # 2. Seed Skill Categories and Skills
        category_order = {
            "programming_languages": 1,
            "frameworks": 2,
            "databases": 3,
            "cloud": 4,
            "ai_ml": 5
        }

        for cat_key, order in category_order.items():
            existing_cat = db.query(SkillCategory).filter(SkillCategory.key == cat_key).first()
            if not existing_cat:
                category = SkillCategory(key=cat_key, display_order=order)
                db.add(category)
                db.flush()  # Get the category ID

                for i, skill_data in enumerate(skills_data.get(cat_key, [])):
                    skill = Skill(
                        name=skill_data["name"],
                        level=skill_data["level"],
                        experience=skill_data["experience"],
                        category_id=category.id,
                        category_key=cat_key,
                        display_order=i
                    )
                    db.add(skill)
                print(f"✓ {cat_key} skills seeded")

        # 3. Seed Projects
        for proj_data in projects_data:
            existing_proj = db.query(Project).filter(Project.id == proj_data["id"]).first()
            if not existing_proj:
                project = Project(
                    id=proj_data["id"],
                    name=proj_data["name"],
                    description=proj_data["description"],
                    highlights=proj_data["highlights"],
                    role=proj_data["role"],
                    team_size=proj_data["team_size"],
                    technologies=proj_data["technologies"],
                    environment=proj_data["environment"],
                    phases=proj_data["phases"],
                    start_date=proj_data["start_date"],
                    end_date=proj_data.get("end_date"),
                    # duration is auto-calculated from start_date and end_date
                    relevance_leader=proj_data["relevance"]["leader"],
                    relevance_brse=proj_data["relevance"]["brse"],
                    relevance_fullstack=proj_data["relevance"]["fullstack"],
                    display_order=proj_data["id"]
                )
                db.add(project)
        print("✓ Projects seeded")

        # 4. Seed Role Emphasis
        for role_key, keywords in role_emphasis_data.items():
            existing_emphasis = db.query(RoleEmphasis).filter(RoleEmphasis.role == role_key).first()
            if not existing_emphasis:
                emphasis = RoleEmphasis(role=role_key, keywords=keywords)
                db.add(emphasis)
        print("✓ Role emphasis seeded")

        db.commit()
        print("\n✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


def reset_database():
    """Drop all tables and recreate them."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset complete")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
        seed_database()
    else:
        seed_database()
